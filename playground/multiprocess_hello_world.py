"""

Some experimenting with multiprocessing.  Code from:
http://toastdriven.com/blog/2008/nov/11/brief-introduction-multiprocessing/
"""

import multiprocessing as mp

def say_hello(name='world'):
    print "Hello, %s" % name

if __name__ == '__main__':
    mp.freeze_support()
    p = mp.Process(target=say_hello)
    p.start()
    p.join()
