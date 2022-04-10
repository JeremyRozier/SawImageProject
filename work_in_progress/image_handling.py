import pyglet
from pyglet.window import key
import cv2
import numpy as np
from SAWgenerator import WithPicture


class PicturePreparation(pyglet.window.Window):
    def __init__(self):
        super().__init__(600, 50, "Prepare your picture", resizable=False)
        self.picture_name = ""
        self.typing = True
        self.background = pyglet.shapes.Rectangle(0, 0, 2000, 2000, color=(0, 30, 50))
        self.text_name_color = (255, 255, 255, 255)
        self.label1 = pyglet.text.Label("Picture name:", x=20, y=20, font_size=14)
        self.label2 = pyglet.text.Label("{}".format(self.picture_name), x=160, y=20, font_size=14)
        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.line4 = None
        self.picture = None
        self.picture_print = None
        self.output_print = None
        self.pic_width = None
        self.pic_height = None
        self.mousex = None
        self.mousey = None
        self.actualx = None
        self.actualy = None
        self.clicked = False
        self.mousex2 = None
        self.mousey2 = None
        self.rectx = 1
        self.recty = 1
        self.rectdx = None
        self.rectdy = None
        self.new_input = None
        self.phase2 = False
        self.generating = False
        self.done = False
        self.launched = False
        self.cycle = 0
        self.label3 = pyglet.text.Label("Generating ...", x=185, y=210, font_size=14)
        self.result = None
        self.sprite = None
        self.density_map = None
        pyglet.clock.schedule_interval(self.update, 0.016)

    def on_key_press(self, symbol, modifiers):
        if not self.done:
            if self.typing:
                if symbol == key.BACKSPACE:
                    if len(self.picture_name) > 0:
                        self.picture_name = self.picture_name[:-1]
                elif symbol == 45:
                    self.picture_name = self.picture_name + "-"
                elif symbol == 46:
                    self.picture_name = self.picture_name + "."
                elif symbol == 95:
                    self.picture_name = self.picture_name + "_"
                elif symbol == key.ENTER:
                    self.typing = False
                    self.picture = cv2.imread("pictures/{}".format(self.picture_name))
                    if self.picture is None:
                        self.typing = True
                        self.picture_name = ""
                    else:
                        self.picture_print = pyglet.resource.image("pictures/{}".format(self.picture_name))
                        self.pic_width = self.picture_print.width
                        self.pic_height = self.picture_print.height
                        self.set_size(self.pic_width * 2 + 60, self.pic_height + 70)
                        self.pic_transformation(self.picture)
                        self.output_print = pyglet.resource.image("pictures/output.jpg")
                        self.text_name_color = (0, 200, 0, 255)
                        self.phase2 = True
                else:
                    character = key.symbol_string(symbol)
                    if modifiers != 1:
                        character = character.lower()
                    if len(character) == 1:
                        self.picture_name = self.picture_name + character
            elif self.phase2:
                if symbol == key.ENTER:
                    self.generating = True
                    self.set_size(500, 500)
                    self.done = True

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.label1.draw()
        self.label2.draw()
        if not self.generating:
            if self.picture is not None:
                self.picture_print.blit(20, 50)
                if self.output_print is not None:
                    self.output_print.blit(40 + self.pic_width, 50)
            if self.line1 is not None:
                self.line1.draw()
                self.line2.draw()
                self.line3.draw()
                self.line4.draw()
        else:
            if not self.launched:
                self.label3.draw()
            else:
                self.set_size(680, 550)
                self.sprite.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.clicked:
            if 20 < x < self.pic_width + 20 and 50 < y < self.pic_height + 50:
                self.mousex = x
                self.mousey = y
                self.clicked = True
        else:
            if 20 < x < self.pic_width + 20 and 50 < y < self.pic_height + 50:
                self.mousex2 = x
                self.mousey2 = y
                self.clicked = False
                self.rectx = max(self.mousex - 20, self.mousex2 - 20)
                self.recty = max(self.mousey - 50, self.mousey2 - 50)
                self.rectdx = abs(self.mousex - self.mousex2)
                self.rectdy = abs(self.mousey - self.mousey2)
                self.new_input = self.picture[self.pic_height - self.recty:self.pic_height - self.recty + self.rectdy]
                _, _,self.new_input = np.hsplit(self.new_input, np.array([0, self.rectx - self.rectdx]))
                _, self.new_input, _ = np.hsplit(self.new_input, np.array([0, self.rectdx]))
                self.pic_transformation(self.new_input)
                self.output_print = None
                self.output_print = pyglet.resource.image("pictures/output.jpg")

    def on_mouse_motion(self, x, y, dx, dy):
        self.actualx = x
        self.actualy = y

    def update(self, dt):
        self.label1 = pyglet.text.Label("Picture name:", x=20, y=20, font_size=14)
        self.label2 = pyglet.text.Label("{}".format(self.picture_name), x=160, y=20, font_size=14)
        self.label1.color = self.text_name_color
        self.label2.color = self.text_name_color
        if self.clicked and self.phase2 and not self.generating:
            self.line1 = pyglet.shapes.Line(self.mousex, self.mousey, self.actualx, self.mousey, width=1, color=(255, 255, 255))
            self.line2 = pyglet.shapes.Line(self.mousex, self.mousey, self.mousex, self.actualy, width=1, color=(255, 255, 255))
            self.line3 = pyglet.shapes.Line(self.actualx, self.mousey, self.actualx, self.actualy,
                                            width=1, color=(255, 255, 255))
            self.line4 = pyglet.shapes.Line(self.mousex, self.actualy, self.actualx, self.actualy,
                                            width=1, color=(255, 255, 255))
        if not self.launched and self.generating:
            self.cycle += 1
            if self.cycle == 10:
                SAW = WithPicture(self.density_map, True, False)
                SAW.run()
                SAW.display_saw()
                self.launched = True
                self.result = pyglet.resource.animation("pictures/saw_animation.gif")
                self.sprite = pyglet.sprite.Sprite(self.result, x=20, y=50)

    def pic_transformation(self, image):
        mask = np.zeros(image.shape[:2], np.uint8)

        bgd = np.zeros((1, 65), np.float64)
        fgd = np.zeros((1, 65), np.float64)

        rect = (1, 1, np.shape(image)[1] - 1, np.shape(image)[0] - 1)

        cv2.grabCut(image, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        picture = image * mask2[:, :, np.newaxis]
        fgbg = cv2.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(picture)
        picture = picture * fgmask[:, :, np.newaxis]

        height, width, _ = picture.shape

        for i in range(0, height - 1):
            for j in range(0, width - 1):
                pixel = picture[i, j]
                pixel[0] = 255 - pixel[0]
                pixel[1] = 255 - pixel[1]
                pixel[2] = 255 - pixel[2]
                picture[i, j] = pixel

        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
        inverter = 255 * np.ones(np.shape(picture))
        cv2.imwrite("pictures/output.jpg", picture)
        self.density_map = inverter - picture


window = PicturePreparation()

pyglet.app.run()
