from tkinter import *
from PIL import Image, ImageTk


class Renderer:
    def __init__(self, title, image_generator, rrange, irange):
        self.image_generator = image_generator  # function that generates image
        self.initialrlength = rrange[1] - rrange[0]
        self.initialilength = irange[1] - irange[0]
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
        self.root.bind('<Key>', self.zoom)
        self.root.bind('<1>', self.zoom)
        self.root.bind('<3>', self.zoom)

    def zoom(self, event):
        print(event)
        # adjust scale
        if (event.keysym == "w" or event.keysym == 'Up' or event.num == 1):
            print("zoom in")
            self.scale -= self.scaleFactor
        elif (event.keysym == "s" or event.keysym == 'Down' or event.num == 3):
            print("zoom out")
            self.scale += self.scaleFactor
        else:
            return

        # get mouse position as coords in mandelbrot
        center = (
            (event.x / self.width) * (self.rrange[1] - self.rrange[0]) + self.rrange[0],
            (event.y / self.height) * (self.irange[1] - self.irange[0]) + self.irange[0])

        # update ranges
        self.rrange = (
                center[0] - self.initialrlength / 2 * self.scale,
                center[0] + self.initialrlength / 2 * self.scale
        )
        self.irange = (
            center[1] - self.initialilength / 2 * self.scale,
            center[1] + self.initialilength / 2 * self.scale
        )

        # draw the image
        self.draw()

    def draw(self):
        print("drawing")
        # get new data
        self.image = ImageTk.PhotoImage(
            self.image_generator(
                self.width,
                self.height,
                self.rrange,
                self.irange))

        # draw data to canvas
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def run(self):
        # draw on startup
        self.draw()
        self.root.mainloop()
