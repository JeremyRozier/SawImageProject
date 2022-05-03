import time

dic_function_time = {}


def store_time(function):
    def modified_function(*args, **kwargs):

        t1 = time.time()
        value_returned = function(*args, **kwargs)
        t2 = time.time()
        elapsed_time = t2 - t1

        if function not in dic_function_time:
            dic_function_time[function] = [elapsed_time]
        else:
            dic_function_time[function].append(elapsed_time)

        return value_returned

    return modified_function


def store_time2(min_time):
    def decorator(function):

        def modified_function(*args_function, **kwargs_function):
            t1 = time.time()
            value_returned = function(*args_function, **kwargs_function)
            t2 = time.time()
            elapsed_time = t2 - t1

            if elapsed_time >= min_time:
                if function not in dic_function_time:
                    dic_function_time[function] = [elapsed_time]
                else:
                    dic_function_time[function].append(elapsed_time)

            return value_returned

        return modified_function

    return decorator
