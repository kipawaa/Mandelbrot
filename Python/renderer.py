from tkinter import *
from PIL import Image, ImageTk

class Renderer:
    def __init__(self, title, image_generator, rrange, irange):
        self.image_generator = image_generator  # function that generates image
        self.rrange = rrange    # range on real axis
        self.irange = irange    # range on imaginary axis

        # ask for resolution
        print("recommendend dimensions are 3:2 width:height, consider 1200 x 800, or 1920 x 1080 for better resolution but slower performance")
        print("press enter for default dimensions (600 x 400)")
        user = input("input 'width height' dimensions: ")
        if (user == ''):
            self.width = 600
            self.height = 400
        else:
            user = user.split()
            print(user)
            self.width = int(user[0])
            self.height = int(user[1])

        # current zoom level and scaling factor
        self.scaleFactor = 0.05
        self.scale = 1.0

        # image variable to prevent garbage collection
        self.image = None

        # create tkinter canvas etc
        self.root = Tk()
        self.root.title = title
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        # bind keys/mouse buttons
        self.root.bind('<Up>', self.zoomIn)
        self.root.bind('<Down>', self.zoomOut)
        self.root.bind('<1>', self.zoomIn)
        self.root.bind('<3>', self.zoomOut)

    def zoomIn(self, event):
        # adjust scale
        self.scale -= self.scaleFactor

        xLength = self.rrange[1] - self.rrange[0]
        yLength = self.irange[1] - self.irange[0]

        # get mouse position as coords in mandelbrot
        center = ((event.x / self.width) * xLength + self.rrange[0], (event.y / self.height) * yLength + self.irange[0])

        # update ranges
        self.rrange = (center[0] - xLength / 2 * self.scale, center[0] + xLength / 2 * self.scale)
        self.irange = (center[1] - yLength / 2 * self.scale, center[1] + yLength / 2 * self.scale)

        # draw the image
        self.draw()

    def zoomOut(self, event):
        # adjust scale
        self.scale += self.scaleFactor

        xLength = self.rrange[1] - self.rrange[0]
        yLength = self.irange[1] - self.irange[0]

        # get mouse position as coords in mandelbrot
        center = ((event.x / self.width) * xLength + self.rrange[0], (event.y / self.height) * yLength + self.irange[0])

        # update ranges
        self.rrange = (center[0] - xLength / 2 * self.scale, center[0] + xLength / 2 * self.scale)
        self.irange = (center[1] - yLength / 2 * self.scale, center[1] + yLength / 2 * self.scale)

        # draw the image
        self.draw()

    def draw(self):
        print("drawing")
        # get new data
        self.image = ImageTk.PhotoImage(self.image_generator(self.width, self.height, self.rrange, self.irange))

        # draw data to canvas
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def run(self):
        # draw on startup
        self.draw()
        self.root.mainloop()
