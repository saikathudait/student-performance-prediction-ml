import time

from django.core.cache import cache


def is_rate_limited(request, action, limit=5, window=300):
    """
    Simple rate limiter using cache. Returns True if limit exceeded.
    """
    identifier = None
    if request.user.is_authenticated:
        identifier = f"user:{request.user.id}"
    else:
        identifier = request.META.get("REMOTE_ADDR", "anon")

    cache_key = f"rl:{action}:{identifier}"
    data = cache.get(cache_key)
    now = time.time()

    if not data or now > data["reset"]:
        data = {"count": 0, "reset": now + window}

    data["count"] += 1
    cache.set(cache_key, data, timeout=window)

    return data["count"] > limit
