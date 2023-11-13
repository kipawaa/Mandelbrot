# creates a map of the burning ship set and saves it as an image

from PIL import Image
import numpy as np
from main import main


def burningShip(complex_constant, convergence_limit, divergence_limit):
    ''' returns the number of iterations for a point to be classified as con/di-vergent based on limits given '''
    # value
    z = 0

    # number of iterations
    n = 0

    # generate new values until point can be said to be con/di-vergent
    while n < convergence_limit and abs(z) < divergence_limit:
        # determining next value
        z = complex(abs(z.real), abs(z.imag)) ** 2 + complex_constant

        #incrementing number of iterations
        n += 1

    # return the number of iterations
    return n

def generate_burningShip(width, height, rrange=(-1.8, -1.7), irange=(-0.1, 0.02)):
    ''' outputs an image of the mandelbrot set, rrange determines the range of values used on the real axis, irange determines the range of values used on the imaginary axis'''
    # maximum number of iterations until a point is said to be convergent
    convergence_limit = 80

    # storing the points generated
    plot = np.zeros((width, height))

    for x in range(width):
        for y in range(height):
            # determining complex number for calculations
            c = complex(rrange[0] + (y / height) * (rrange[1] - rrange[0]),
                        irange[0] + (x / width) * (irange[1] - irange[0]))

            # determining mandelbrot value at point
            m = burningShip(c, convergence_limit, 2)

            # assigning colour value to point based on number of iterations required to determine con/di-vergence
            color = 255 - int(m * 255 / convergence_limit)

            # adding point to stored points
            plot[x, y] = color

    # displaying image
    image = Image.fromarray(plot)
    return image

if __name__ == '__main__':
    main(generate_burningShip)
