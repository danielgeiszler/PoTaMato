# -*- coding: utf-8 -*-
import time


def pocketwatch(func):
    """
    use decorator @pocketatch on a function to time it

    Parameters
    ----------
    func : target function

    Returns
    -------
    wrapper : function

    """
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f"{func} took {t2} seconds.")
        
    return wrapper

        

