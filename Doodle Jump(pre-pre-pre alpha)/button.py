from MODULES import *

from rectangle_object import RectObject
from text_object import TextObject


class Button(RectObject):
    def __init__(self, x=0, y=0, w=0, h=0, text="", padding_x=0, padding_y=0):
        RectObject.__init__(self, x, y, w, h)

        self.state = 'normal'
        self.clicked = False
        self.disabled = False

        self.text = TextObject(x + padding_x, y + padding_y, lambda: text, c.button_text_color,
                               c.font_name, c.font_size)

    @property
    def back_color(self):
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color)[self.state]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.rect)
        self.text.draw(surface)

    def reset(self):
        self.clicked = False

    def handle_mouse_event(self, etype, pos):
        if not self.disabled:
            if etype == pygame.MOUSEMOTION:
                self.handle_mouse_move(pos)
            elif etype == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(pos)
                self.handle_mouse_click(pos)
            elif etype == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up()
        else:
            self.state = "normal"

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            if self.state != "pressed":
                self.state = "hover"
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self):
        if self.state == 'pressed':
            self.state = 'hover'

    def handle_mouse_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True

    def reset_click(self):
        self.clicked = False

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def update(self):
        self.reset_click()

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted button")
