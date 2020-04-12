import pygame
import random
import math
from abc import ABC, abstractmethod

SCREEN_DIM = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Vec2d():
    def __init__(self, x_or_pair, y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
    
    def __add__(self, vec):
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            return self.x * k.x + self.y * k.y
        return Vec2d(self.x * k, self.y * k)

    def len(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def int_pair(self):
        return (int(self.x), int(self.y))

class Polyline(ABC):
    
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    @abstractmethod
    def draw_points(self, points, width=3, color=WHITE):
        pass

class Knot(Polyline):
    
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.get_knot()
    
    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res
    
    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                p.int_pair(), width)


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Space", "+1 curve"])
    data.append(["Left Arrow", "             Previous curve"])
    data.append(["Right Arrow", "            Next curve"])
    data.append(["Mouse right", "            Delete last point from curve"])
    data.append(["Q", "Decrease speed"])
    data.append(["E", "Increase speed"])
    data.append(["H", "Speed reverse"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    steps = 35
    working = True
    knots = []
    knots.append(Knot(steps))
    knot_number = 0
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_SPACE:
                    knot_number += 1
                    knots.append(Knot(steps))
                if event.key == pygame.K_RIGHT:
                    if knot_number < len(knots):
                        knot_number += 1
                    else:
                        knot_number = knot_number 
                if event.key == pygame.K_LEFT:
                    if knot_number > 0:
                        knot_number -= 1
                    else:
                        knot_number = knot_number
                if event.key == pygame.K_h:
                    for i in range(len(knots[knot_number].speeds)):
                        knots[knot_number].speeds[i] = Vec2d(-knots[knot_number].speeds[i].x, -knots[knot_number].speeds[i].y)
                if event.key == pygame.K_q:
                    for i in range(len(knots[knot_number].speeds)):
                        if knots[knot_number].speeds[i].x > 0 and knots[knot_number].speeds[i].y > 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x - 0.1, knots[knot_number].speeds[i].y - 0.1)
                        if knots[knot_number].speeds[i].x < 0 and knots[knot_number].speeds[i].y > 0:
                                knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x + 0.1, knots[knot_number].speeds[i].y - 0.1)
                        if knots[knot_number].speeds[i].x > 0 and knots[knot_number].speeds[i].y < 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x - 0.1, knots[knot_number].speeds[i].y + 0.1)
                        if knots[knot_number].speeds[i].x < 0 and knots[knot_number].speeds[i].y < 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x + 0.1, knots[knot_number].speeds[i].y + 0.1)
                if event.key == pygame.K_e:
                    for i in range(len(knots[knot_number].speeds)):
                        if knots[knot_number].speeds[i].x > 0 and knots[knot_number].speeds[i].y > 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x + 0.1, knots[knot_number].speeds[i].y + 0.1)
                        if knots[knot_number].speeds[i].x < 0 and knots[knot_number].speeds[i].y > 0:
                                knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x - 0.1, knots[knot_number].speeds[i].y + 0.1)
                        if knots[knot_number].speeds[i].x > 0 and knots[knot_number].speeds[i].y < 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x + 0.1, knots[knot_number].speeds[i].y - 0.1)
                        if knots[knot_number].speeds[i].x < 0 and knots[knot_number].speeds[i].y < 0:
                            knots[knot_number].speeds[i] = Vec2d(knots[knot_number].speeds[i].x - 0.1, knots[knot_number].speeds[i].y - 0.1)        
                if event.key == pygame.K_r:
                    knots = []
                    knots.append(Knot(steps))
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knots[knot_number].count += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knots[knot_number].count -= 1 if knots[knot_number].count > 1 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    knots[knot_number].add_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                elif event.button == 3:
                    if len(knots[knot_number].points) > 0:
                        knots[knot_number].points.pop()
                        knots[knot_number].speeds.pop()
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for knot in knots:
            knot.draw_points(knot.points)
            knot.draw_points(knot.get_knot(), "line", 3, color)
        if not pause:
            for knot in knots:
                knot.set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)