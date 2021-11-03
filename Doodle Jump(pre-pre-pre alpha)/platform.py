from MODULES import *

from game_object import GameObject


class Platform(GameObject):
    def __init__(self, x, y):
        self.texture = pygame.image.load("textures/platform_basic.png").convert_alpha()
        rect = self.texture.get_rect()
        rect = rect.move(x, y)
        GameObject.__init__(self, rectangle=rect)

    def draw(self, surface):
        surface.blit(self.texture, self.bounds)

    def __del__(self):
        print("ID ", self.ID, " deleted platform")


class MovingPlatform(GameObject):
    def __init__(self, x, y, speed):
        self.texture = pygame.image.load("textures/platform_basic.png").convert_alpha()
        rect = self.texture.get_rect()
        rect = rect.move(x, y)
        GameObject.__init__(self, rectangle=rect)
        self.time = 0

        # random direction
        self.moving_left = random.choice([True, False])
        self.moving_right = not self.moving_left

        # values
        self.DUR = c.duration_moving_platforms()
        self.speed = speed

    def offset_fun(self):
        return self.speed

    def move_horizontal(self):
        if self.time >= self.DUR and self.moving_left:
            self.moving_left = False
            self.moving_right = True
            self.time = 0
        if self.time >= self.DUR and self.moving_right:
            self.moving_left = True
            self.moving_right = False
            self.time = 0

        dx = abs(self.offset_fun())
        if self.moving_left:
            dx = -min(dx, self.left)
        else:
            dx = min(dx, c.win_width - self.right)

        self.move(dx, 0)

    def draw(self, surface):
        surface.blit(self.texture, self.bounds)

    def update(self):
        self.time += 1/c.framerate

        self.move_horizontal()

    def __del__(self):
        print("ID ", self.ID, " deleted platform(m)")


class FakePlatform(GameObject):
    def __init__(self, x, y):
        self.texture = pygame.image.load("textures/platform_basic.png").convert_alpha()
        rect = self.texture.get_rect()
        rect = rect.move(x, y)
        GameObject.__init__(self, rectangle=rect)

    def __del__(self):
        print("ID ", self.ID, " deleted platform(m)")

    def draw(self, surface):
        surface.blit(self.texture, self.bounds)


def random_platform(x, y, chances_list):
    # 1. DEFAULT PLATFORM, 2. MOVING PLATFORM 3. FAKE PLATFORM
    chances_sum = 0
    for i in chances_list:
        chances_sum += i
    if chances_sum != 100:
        raise NameError("chances_list EXCEPTION, INVALID CHANCES.")
    loto = []
    for i in range(len(chances_list)):
        for j in range(0, chances_list[i]):
            loto.append(i)
    res = loto[random.randint(0, 99)]
    if res == 0:
        return Platform(x, y)
    elif res == 1:
        speed = 6
        return MovingPlatform(x, y, speed)
    elif res == 2:
        return FakePlatform(x, y)
