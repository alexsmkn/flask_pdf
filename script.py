import time


def factorial(n):
    count = 1
    fact = 1
    while count <= n:
        yield fact
        count = count + 1
        fact = fact * count


c = factorial(10)
print(next(c))
print(next(c))

x = [1, 3, 3, 4, 45, 6, 7, 78, 8, 22]

i = iter(x)

print(next(i))

print(next(i))
print(next(i))
print(next(i))
print(next(i))


def fibonacci(n):
    """ A generator for creating the Fibonacci numbers """
    a, b, counter = 0, 1, 0
    while True:
        if counter > n:
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)
print(next(f))  # 0


def grep(pattern):
    while True:
        line = (yield)
        if pattern in line:
            print('Coool yeah->')
        else:
            print('no(')


coro = grep('p')
next(coro)
coro.send('asd')
coro.send('axd')
coro.send('apd')


def coroutine(func):
    def start_firstly(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start_firstly


@coroutine
def grep_new(pattern):
    while True:
        line = (yield)
        if pattern in line:
            print('Coool yeah->')
        else:
            print('no(')


new_coro = grep_new('qwe')

new_coro.send('wew')
new_coro.send('qweqweqwe')


def countdown(n):
    while n >= 0:
        newvalue = (yield n)
        # If a new value got sent in, reset n with it
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1


c = countdown(10)
next(c)
print(next(c))


def deco(func, *args):
    def func_new(*args, **kwargs):
        time1 = time.time()
        func(*args, **kwargs)
        time2 = time.time()
        print('Calling {} takes {}'.format(func.__name__, str(time2 - time1)))

    return func_new


@deco
def sum(a, d):
    time.sleep(2)
    print(a + d)


sum(2, 3)


def outer_func(x):
    def inner_func(y):
        return y + x
    return inner_func
