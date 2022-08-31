import os
import time
import pickle

from functools import wraps, update_wrapper


def parameterized(decorator):
    @wraps(decorator)
    def wrapper(*args, **kwargs):
        def _decorator(decorated):
            return decorator(decorated, *args, **kwargs)

        return _decorator

    return wrapper


def file_cache(cachename, recompute=False):
    """File-based cache decorator.

    Parameters
    ----------
    cachename : str, or None
        The name of the file to use for cache storage. Caching
        is disabled if this is set to `None`.

    recompute : bool, default=False
        Whether to update the cache on every call.

    Details
    -------
    Arguments (keyworded and positional) to the cached function must
    be hashable, because they are used for lookup. In essence, the
    arguments are serialized and the resulting binary string is used
    as key.
    """
    assert cachename is None or isinstance(cachename, str)

    if not isinstance(cachename, str):
        # no filename given : decorator just passes function through
        def decorator(user_function):
            return user_function

        return decorator

    # initialize an empty cache
    if not os.path.exists(cachename):
        with open(cachename, "wb") as fout:
            pickle.dump({}, fout)

    def decorator(user_function):
        with open(cachename, "rb") as fin:
            cache = pickle.load(fin)

        def wrapper(*args, **kwargs):
            # dumb stategy: pickle the args and use it as a binary key
            key = pickle.dumps((args, kwargs), protocol=3)

            # no key: call the wrapped function
            if key not in cache or recompute:
                cache[key] = user_function(*args, **kwargs)

                with open(cachename, "wb") as fout:
                    pickle.dump(cache, fout)

            return cache[key]

        return update_wrapper(wrapper, user_function)

    return decorator


@parameterized
def retry_on(fn_call, exception, tries=10, delay=2, growth=1.5, verbose=False):
    @wraps(fn_call)
    def wrapper(*args, **kwargs):
        n_tries, f_delay = tries, delay
        while n_tries > 1:
            try:
                return fn_call(*args, **kwargs)

            except Exception:
                if verbose:
                    print(f"Retry in {f_delay} sec.")

                time.sleep(f_delay)
                n_tries, f_delay = n_tries - 1, f_delay * growth

        return fn_call(*args, **kwargs)

    return wrapper
