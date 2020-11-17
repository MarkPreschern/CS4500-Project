from func_timeout import func_timeout


def timed_call(timeout: int, obj: object, method_name: str, args: tuple):
    """
    Attempts to call given method on a given object and return its return value. If a timeout
    or exception occurs, None is returned instead.

    :param timeout: seconds(int) to wait for call to execute
    :param obj: object to run method on
    :param method_name: str name of the method to call on IPlayer obj
    :param args: tuple containing the arguments to pass to method to be called
    :return: return call result or None on failure
    """
    # Validate params
    if not isinstance(timeout, int):
        raise TypeError('Expected int for timeout!')

    if not isinstance(obj, object):
        raise TypeError('Expected object for obj!')

    if not isinstance(method_name, str):
        raise TypeError('Expected str for method_name!')

    if not isinstance(args, tuple):
        raise TypeError('Expected tuple for args!')

    try:
        return func_timeout(timeout, getattr(obj, method_name), args)
    except:
        return None
