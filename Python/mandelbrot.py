# creates a map of the mandelbrot set and saves it as an image

from PIL import Image
import numpy as np
import tkinter as tk
from renderer import Renderer


def mandelbrot(c, convergence_limit):
    ''' returns the number of iterations for a point to be classified as con/di-vergent '''

    # skip points inside main bulb (from wikipedia
    # https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set#Cardioid_/_bulb_checking)
    q = (c.real - 0.5) * c.real + 0.125 + c.imag * c.imag
    if q * (q + c.real - 0.25) <= 0.25 * c.imag * c.imag:
        return convergence_limit

    # representing the squares of x and y, where z = x + iy
    x2 = 0
    y2 = 0
    x = 0
    y = 0

    # number of iterations
    n = 0

    # generate new values until point can be said to be con/di-vergent
    while x2 + y2 < 4 and n < convergence_limit:
        # determining next value (this method reduces the number of
        # multiplications)
        y = (x + x) * y + c.imag
        x = x2 - y2 + c.real
        x2 = x * x
        y2 = y * y

        # incrementing number of iterations
        n += 1

    # return the number of iterations
    return n


def generate_mandelbrot(width, height, rrange=[-2, 1], irange=[-1, 1]):
    ''' outputs an image of the mandelbrot set, rrange determines the range of values used on the real axis, irange determines the range of values used on the imaginary axis'''
    # frame buffer
    plot = np.zeros((height, width))

    # define convergence limit
    convergence_limit = 80

    # cache the size of the render region to avoid re-computing in the loop
    Ilength = irange[1] - irange[0]
    Rlength = rrange[1] - rrange[0]

    # compute values for each pixel in the window
    for y in range(height):

        # invert height so that 0,0 in the frame buffer aligns with 0,0 in the
        # window (notice that this is not 0,0 in the render region)
        imag = (y / height) * Ilength + irange[0]

        # TODO mandelbrot is symmetric across x axis so if we have seen the
        # opposite of this row we can simply copy it over

        zero_mapped = -irange[0] / Ilength * height
        upper_reflected = 2 * zero_mapped
        
        if zero_mapped < y < min(upper_reflected, height):
            plot[y, :] = plot[int(2 * zero_mapped - y), :]
        else:
            for x in range(width):
                # determining complex number for calculations
                c = complex(rrange[0] + (x / width) * Rlength, imag)

                # determining mandelbrot value at point
                m = mandelbrot(c, convergence_limit)

                # assigning colour value to point based on number of iterations
                # required to determine con/di-vergence
                color = 255 - int(m * 255 / convergence_limit)

                # adding point to stored points
                plot[y, x] = color

    # generate an image from the frame buffer
    image = Image.fromarray(plot)
    return image


if __name__ == '__main__':
    renderer = Renderer(
        "Mandelbrot", generate_mandelbrot, (-2, 1), (-1, 1))
    renderer.run()
