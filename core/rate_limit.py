import time
import functools
import random


def parse_rate_limit(limit_str, state_str):
    limits = [list(map(int, x.split(":"))) for x in limit_str.split(",")]
    states = [list(map(int, x.split(":"))) for x in state_str.split(",")]

    buckets = []
    for l, s in zip(limits, states):
        buckets.append({
            "limit": l[0],
            "window": l[1],
            "used": s[0],
        })
    return buckets


def format_bucket_log(buckets):
    return " | ".join(f"{b['used']}/{b['limit']}:{b['window']}" for b in buckets)


def compute_delay(buckets):
    danger_delays = []

    for b in buckets:
        remaining = b["limit"] - b["used"]

        # ⚠️ gần hoặc đã full
        if remaining <= 1:
            # giả định 1 request = 1s
            sleep = b["window"] - b["used"]

            # buffer nhẹ
            sleep *= 1.1

            if sleep > 0:
                danger_delays.append(sleep)

    if danger_delays:
        return max(danger_delays), True

    # bình thường
    return random.uniform(1.0, 2.0), False


def rate_limited():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            while True:
                resp = func(*args, **kwargs)

                # ===== 429 =====
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 5))
                    print(f"[RATE LIMIT] 429 → sleep {retry_after}s")
                    time.sleep(retry_after)
                    continue

                try:
                    limit_raw = resp.headers.get("X-Rate-Limit-Ip")
                    state_raw = resp.headers.get("X-Rate-Limit-Ip-State")

                    if limit_raw and state_raw:
                        buckets = parse_rate_limit(limit_raw, state_raw)
                        bucket_log = format_bucket_log(buckets)

                        delay, is_danger = compute_delay(buckets)

                        if is_danger:
                            print(f"[RATE LIMIT] {bucket_log} → DANGER sleep {delay:.2f}s")

                        time.sleep(delay)

                except Exception as e:
                    print(f"[RATE LIMIT ERROR] {e}")

                return resp

        return wrapper
    return decorator