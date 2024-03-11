import multiprocessing
import random as rd
import time

# creating trapezoid class
from concurrent.futures import ThreadPoolExecutor


class Trapezoid:

    def __init__(self, trap=None):
        if trap is None:
            trap = [0, 0, 0]
        self.a = trap[0]
        self.b = trap[1]
        self.h = trap[2]

    def __str__(self):
        return 'ტოლფერდა ტრაპეციის დიდი ფუძეა -> {}, პატარა ფუძეა -> {}, ხოლო სიმაღლეა ->{}'.format(self.b, self.a,
                                                                                                    self.h)

    def area(self):
        if isinstance(self.a, int) and isinstance(self.b, int) and isinstance(self.h, int):
            return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()

        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        return "Wrong input type!"

    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() - other.area()
        return "Wrong input type!"

    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() // other.area()
        return "Wrong input type!"


# creating rectangle class which is child of trapezoid
class Rectangle(Trapezoid):
    def __init__(self, re=None):
        if re is None:
            re = [0, 0]
        super().__init__([re[0], re[0], re[1]])

    def __str__(self):
        return "მართკუთხედის სიმაღლეა -> {}, ხოლო სიგანე -> {}".format(self.a, self.h)


# creating square class which is child of rectangle
class Square(Rectangle):
    def __init__(self, c):
        super().__init__([c, c, c])

    def __str__(self):
        return "კვადრატის გვერდია -> {}".format(self.a)


# functions to calculate generate areas
def trapezoid_area(arr):
    for i in arr:
        T = Trapezoid(i)
        T.area()


def rectangle_area(arr):
    for i in arr:
        R = Rectangle(i)
        R.area()


def square_area(arr):
    for i in arr:
        S = Square(i)
        S.area()


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square in general
# without threads or processes
def regular(arr):
    start = time.perf_counter()

    trapezoid_area(arr)
    rectangle_area(arr)
    square_area(arr)

    finish = time.perf_counter()

    print('in general Finished in: ', round(finish - start, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using threads


def threads(arr):
    start1 = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        fut1 = executor.submit(trapezoid_area, arr)
        fut2 = executor.submit(rectangle_area, arr)

        result1 = fut1.result()
        result2 = fut2.result()

    finish1 = time.perf_counter()
    return round(finish1 - start1, 2)


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using processes
def multiprocess(arr):
    start2 = time.perf_counter()

    # create a process pool with 2 worker processes
    with multiprocessing.Pool(2) as pool:
        pool.apply(trapezoid_area, args=(arr[:len(arr) // 2],))
        pool.apply(rectangle_area, args=(arr[len(arr) // 2:],))

    finish2 = time.perf_counter()
    print('with pools Finished in: ', round(finish2 - start2, 2), 'second(s)')


def multiprocess_with_threads(arr):
    start2 = time.perf_counter()

    # create 5 processes
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=threads, args=(arr,))
        p.start()
        processes.append(p)

    # wait for all processes to finish
    for p in processes:
        p.join()

    finish2 = time.perf_counter()
    print('with 5 processes and 20 threads in each Finished in: ', round(finish2 - start2, 2), 'second(s)')


if __name__ == "__main__":
    # Generating parameters for 10000 trapezoid: big base, small base and height
    trapecoids = [[rd.randint(1, 200), rd.randint(
        1, 200), rd.randint(1, 200)] for _ in range(100000)]

    # Generating parameters for 10000 rectangles: width and height
    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(100000)]

    # Generating parameters for 10000 squars
    squars = [rd.randint(1, 200) for _ in range(100000)]

    regular(trapecoids)  # 0.27 seconds
    print('with threads Finished in: ' + str(threads(trapecoids)) + 'second(s)')  # 0.17 seconds
    multiprocess(trapecoids)  # 0.48 seconds
    multiprocess_with_threads(trapecoids)  # 2.09 seconds
