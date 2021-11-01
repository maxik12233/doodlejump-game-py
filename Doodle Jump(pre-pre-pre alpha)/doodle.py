import pygame
import weakref
import colors

from delete import *
import config as c
from game import Game
from jumper import Jumper
from platform import Platform, MovingPlatform, random_platform
from text_object import TextObject
from button import Button
from statistic import Statistic

# commited lol
class Doodle(Game):
    def __init__(self):
        Game.__init__(self, 'Doodle Jump', c.win_width, c.win_height, "images/background.jpg", c.framerate)

        self.jumper = Jumper()

        # Time trackers(for any events)
        self.time = 0  # Main time tracker
        self.game_lost_time = -1

        # platforms creation
        self.last_platform_height = 0
        self.tracking_platform = None

        # Game states
        self.game_over = False
        self.game_state = 'Menu'
        self.create_menu()

        # Game statistic
        self.points_text = None
        self.jumped_platforms_count_text = None
        self.max_height_text = None

    def create_menu(self):
        main_menu_buttons = list()
        main_menu_buttons.append(Button(c.win_width / 2 - 160 / 2, 150, 160, 60, "ИГРАТЬ", paddingX=16, paddingY=6))
        main_menu_buttons.append(Button(c.win_width / 2 - 235 / 2, 250, 235, 60, "НАСТРОЙКИ", paddingX=16, paddingY=6))
        main_menu_buttons.append(Button(c.win_width / 2 - 155 / 2, 350, 155, 60, "ВЫХОД", paddingX=16, paddingY=6))
        for button in main_menu_buttons:
            self.mouse_handlers.append(button.handle_mouse_event)
            self.objects.append(button)
            self.buttons.append(button)

    def create_jumper(self):
        jumper = Jumper(c.win_width / 2, c.win_height / 2 - 15, 20, 30, c.jumper_speedX)
        self.keydown_handlers[pygame.K_LEFT].append(jumper.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(jumper.handle)
        self.keyup_handlers[pygame.K_LEFT].append(jumper.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(jumper.handle)
        self.jumper = jumper

        self.objects.append(self.jumper)

        del jumper

    def first_platforms_layer(self):
        max_platform_distance = 0
        if self.jumper.JUMP_DURATION * c.framerate * self.jumper.offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper.JUMP_HEIGHT + 0
        else:
            pass

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(0, max_platform_distance))
        heights.append(random.randint(c.win_height, c.win_height+100))
        maximum_height = max(heights)

        width = 40
        long = 5
        platforms = []
        heights.sort()
        for h in heights:
            platform = random_platform(random.randint(0, c.win_width - width),
                                       c.win_height - h, width, long, [0, 100])
            platforms.append(platform)
            heights.remove(h)

        self.tracking_platform = platforms[-1]
        for platform in platforms:
            self.platforms.append(platform)
            self.objects.append(platform)

        self.last_platform_height = maximum_height

    def another_platforms(self):
        max_platform_distance = 0
        if self.jumper.JUMP_DURATION * c.framerate * self.jumper.offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper.JUMP_HEIGHT + 0
        else:
            pass

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(c.win_height, c.win_height + max_platform_distance))
        maximum_height = max(heights)

        width = 40
        long = 5
        platforms = []
        heights.sort()
        for h in heights:
            platform = random_platform(random.randint(0, c.win_width - width),
                                       c.win_height - h, width, long, [90, 10])
            platforms.append(platform)
            heights.remove(h)

        self.tracking_platform = platforms[-1]
        for platform in platforms:
            self.platforms.append(platform)
            self.objects.append(platform)

        self.last_platform_height = maximum_height

    def create_plato(self):
        for i in range(0, c.win_width // 40):
            platform = random_platform(i * 40, c.win_height - 5, 40, 5, [100, 0])
            self.platforms.append(platform)
            self.objects.append(platform)

    def create_stats_trackers(self):
        self.max_height_text = Statistic(3, 0, lambda: "height", colors.BLUE, c.font_name, c.font_size_trackers)
        self.points_text = Statistic(3, 30, lambda: "points", colors.BLUE, c.font_name, c.font_size_trackers)
        self.jumped_platforms_count_text = Statistic(3, 60, lambda: "jumped", colors.BLUE, c.font_name,
                                                     c.font_size_trackers)
        self.objects.append(self.max_height_text)
        self.objects.append(self.points_text)
        self.objects.append(self.jumped_platforms_count_text)

    def game_lost(self):
        # create basic TextObject to display "GAME LOST!"
        text = TextObject(c.win_width / 2 - 110, c.win_height / 2 - 60, lambda: "GAME LOST!", colors.RED1, c.font_name,
                          50)
        # save params
        height = self.max_height_text.param+0
        points = self.points_text.param+0
        platforms = self.jumped_platforms_count_text.param+0
        # remove and delete old statistic
        self.objects.remove(self.jumped_platforms_count_text)
        self.objects.remove(self.points_text)
        self.objects.remove(self.max_height_text)
        delete_trackers([self.points_text, self.jumped_platforms_count_text, self.max_height_text], self.errors_log)
        self.jumped_platforms_count_text = None
        self.points_text = None
        self.max_height_text = None
        # create new statistic
        self.max_height_text = Statistic(c.win_width / 2 - 50, c.win_height / 2 - 15, lambda: "height", colors.ORANGE, c.font_name,
                           30)
        self.points_text = Statistic(c.win_width / 2 - 50, c.win_height / 2 + 20, lambda: "points", colors.ORANGE, c.font_name,
                           30)
        self.jumped_platforms_count_text = Statistic(c.win_width / 2 - 50, c.win_height / 2 + 55, lambda: "jumped", colors.ORANGE, c.font_name,
                              30)
        # set old saved params to the new statistic
        self.max_height_text.param = height
        self.points_text.param = points
        self.jumped_platforms_count_text.param = platforms
        # add to multi coloring
        self.multicolor.add_object(weakref.ref(text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.max_height_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.points_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.jumped_platforms_count_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        # add them to the objects
        self.objects.append(text)  # basic TextObject
        self.objects.append(self.jumped_platforms_count_text)
        self.objects.append(self.points_text)
        self.objects.append(self.max_height_text)

    def game_lost_pause(self):
        if self.game_lost_time < 0:
            return
        time_elapsed = self.time - self.game_lost_time
        if time_elapsed >= c.after_lost_pause:
            self.delete_objects()
            self.create_menu()
            self.game_state = "Menu"
            self.game_lost_time = -1

    def camera_chasing(self):
        if self.jumper.centery < c.win_height / 2 and self.jumper.last_dy < 0:
            for o in self.objects:
                o.move(0, -self.jumper.last_dy)
            self.last_platform_height -= self.jumper.last_dy
            return -self.jumper.last_dy  # returns height change (high)
        return 0

    def update_points(self, height_delta, jumped_plat):
        self.max_height_text.param += height_delta
        self.jumped_platforms_count_text.param += jumped_plat
        self.points_text.param += height_delta / 10 + jumped_plat * 100

    def delete_objects(self):
        # delete platforms
        self.tracking_platform = None
        for o in self.platforms:
            del o
        # delete buttons
        for o in self.buttons:
            self.mouse_handlers.remove(o.handle_mouse_event)
            del o
        # delete all objects
        for o in self.objects:
            del o
        # to default lists
        self.objects = []
        self.platforms = []
        self.buttons = []
        # delete all jumper handlers and jumper
        delete_jumper(self.keyup_handlers, self.keydown_handlers, self.jumper, self.errors_log)
        self.jumper = None
        # delete all statistic trackers
        delete_trackers([self.points_text, self.max_height_text, self.jumped_platforms_count_text], self.errors_log)
        self.points_text = None
        self.jumped_platforms_count_text = None
        self.max_height_text = None

    def clean_garbage(self):
        for o in self.objects_to_remove:
            self.objects.remove(o)
        self.objects_to_remove = []

    def update(self):
        self.time += 1 / c.framerate

        # Start playing
        if self.game_state == "Menu":
            if self.buttons[0].state == "pressed":
                self.delete_objects()
                self.last_platform_height = 0

                self.create_jumper()
                self.create_plato()
                self.first_platforms_layer()
                self.create_stats_trackers()

                self.game_over = False
                self.game_state = "Play"
                return

            # Settings
            if self.buttons[1].state == "pressed":
                pass

            # Exit
            if self.buttons[2].state == "pressed":
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

        if self.game_state == "Play":
            if self.jumper.game_over:
                self.jumper.game_over = False
                # action
                self.game_lost()
                self.game_lost_time = self.time + 0
                self.game_over = True

            if not self.game_over:
                plat_was_jumped = 0
                plat = self.jumper.collision_check(self.platforms)
                if plat is not None:
                    plat.color = colors.RED1
                    plat_was_jumped = 1
                height_dif = self.camera_chasing()

                self.update_points(height_dif, plat_was_jumped)

                if self.tracking_platform.top >= 0:
                    self.another_platforms()
            else:
                self.game_lost_pause()

        # other objects manipulations
        self.multicolor.update()
        # generic objects manipulation
        for o in self.objects:
            o.update()

            # delete movable object, IF HE IS LOWER THAT c.win_height + 10
            if self.game_state == "Play":
                try:
                    # No exception if object is movable
                    if o.top > c.win_height + 10:
                        # it will be deleted at the end of a tick
                        self.objects_to_remove.append(o)
                        # The list of objects collections that you want to delete here (START)
                        try_delete_object_by_id(self.platforms, o.ID)  # try to delete platform
                        # (END)
                        del o
                except AttributeError:
                    self.errors_log[AttributeError] += "doodle.py: update(): for o in self.objects:...\n"
                except BaseException:
                    raise RuntimeError("UNKNOWN UNHANDLED ERROR: doodle.py: for o in self.objects:...\n")
        # Cleaning deleted objects from self.objects
        self.clean_garbage()


def main():
    Doodle().run()


if __name__ == '__main__':
    main()