import time
import functools
import re


def rate_limited():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)

            try:
                state = list(map(int, re.split(":|,", resp.headers["X-Rate-Limit-Ip-State"])))
                limit = list(map(int, re.split(":|,", resp.headers["X-Rate-Limit-Ip"])))

                sleep_sec = 0

                # bucket 10s
                if state[0] >= limit[0]:
                    sleep_sec = max(sleep_sec, limit[1])

                # bucket 60s
                if state[3] >= limit[3]:
                    sleep_sec = max(sleep_sec, limit[4])

                # bucket 300s
                if state[6] >= limit[6]:
                    sleep_sec = max(sleep_sec, limit[7])

                if sleep_sec > 0:
                    print(f"[RATE LIMIT] proactive sleep {sleep_sec}s")
                    time.sleep(sleep_sec)

            except Exception:
                # header chưa có → ignore
                pass

            return resp

        return wrapper
    return decorator
