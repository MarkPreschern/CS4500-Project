class MockHelper:
    def __init__(self, obj, method, args=None, call_original=False):
        """
        Initializes mock helper with provided parameters.
        :param obj: object whose method is to be mocked
        :param method: method (string) to be mocked
        :param args: arguments to check (None if args are to be ignored)
        :param call_original: whether to call original function
        :return: None
        """
        # Set object
        self.__obj = obj
        # Set target method in the object
        self.__method = method
        # Set args
        self.__args = args
        # Set called flag
        self.__method_called = False
        # Set correct args flag
        self.__correct_args = False
        # Set call_original flag
        self.__call_original = call_original
        # Set pointer to method in object
        self.__method_ref = getattr(obj, method)

    def __enter__(self):
        # Unset called flag
        self.__method_called = False
        # Pipe method through run_method to mark it as having run
        setattr(self.__obj, self.__method, self.__pipe)

    def __pipe(self, *args, **kwargs):
        # Set flag
        self.__method_called = True

        if self.__args is not None:
            self.__correct_args = (self.__args == list(args))
        else:
            self.__correct_args = True

        if self.__call_original:
            # Call actual method
            self.__method_ref(*args, **kwargs)

    def __exit__(self, type, value, traceback):
        # Make sure method has been called
        assert self.__method_called, "Method was not called"

        # Make sure the method was called with the right args
        assert self.__correct_args, "Method was called with incorrect args"
