# creates a map of the burning ship set and saves it as an image

from PIL import Image
import numpy as np
from renderer import Renderer


def burningShip(complex_constant, convergence_limit):
    ''' returns the number of iterations for a point to be classified as con/di-vergent based on limits given '''
    # value
    z = 0

    # number of iterations
    n = 0

    # generate new values until point can be said to be con/di-vergent
    while n < convergence_limit and abs(z) < 2:
        # determining next value
        z = complex(abs(z.real), abs(z.imag)) ** 2 + complex_constant

        #incrementing number of iterations
        n += 1

    # return the number of iterations
    return n

def generate_burningShip(width, height, rrange=(-2, -1), irange=(-0.33, 0.0), convergence_limit=60):
    ''' outputs an image of the mandelbrot set, rrange determines the range of values used on the real axis, irange determines the range of values used on the imaginary axis'''
    # frame buffer
    plot = np.zeros((height, width))

    # cache the size of the render region to avoid re-computing in the loop
    Ilength = irange[1] - irange[0]
    Rlength = rrange[1] - rrange[0]

    # compute values for each pixel in the window
    for y in range(height):
        imag = (y / height) * Ilength + irange[0]

        for x in range(width):
            # determining complex number for calculations
            c = complex(rrange[0] + (x / width) * Rlength, imag)

            # determining mandelbrot value at point
            m = burningShip(c, convergence_limit)

            # adding point to stored points
            plot[y, x] = m
    
    # generate an image from the frame buffer
    return plot

if __name__ == '__main__':
    renderer = Renderer("Burning Ship", generate_burningShip, (-2.25, 1.5), (-2, 0.5), 600, 400)
    renderer.run()
