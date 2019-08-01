import pygame
import random
import sys

# Globals
w = 400
h = 400
size = 10
s = 1
speed = (s, 0)


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, sz):
        pygame.sprite.Sprite.__init__(self)
        self.size = sz
        self.image = pygame.Surface((self.size, self.size)).convert()
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(x, y, self.size, self.size)

    def update(self, r, b_pos=''):
        if b_pos == '':
            self.rect.x += speed[0]
            self.rect.y += speed[1]

            if r:
                if self.rect.x % self.size <= (self.size/2 - 1):
                    self.rect.x = self.rect.x = self.rect.x - self.rect.x % self.size
                elif self.rect.x % self.size >= self.size/2:
                    self.rect.x = self.rect.x = self.rect.x + (self.size - self.rect.x % self.size)
                if self.rect.y % self.size <= (self.size/2 - 1):
                    self.rect.y = self.rect.y = self.rect.y - self.rect.y % self.size
                elif self.rect.y % self.size >= self.size/2:
                    self.rect.y = self.rect.y = self.rect.y + (self.size - self.rect.y % self.size)

            if self.rect.right <= 0:
                self.rect.left = w - size
            elif self.rect.left >= w:
                self.rect.left = size
            if self.rect.bottom <= 0:
                self.rect.top = h - size
            elif self.rect.top >= h:
                self.rect.bottom = size

        elif b_pos != '':
            self.rect.x = b_pos[0]
            self.rect.y = b_pos[1]


class Dot(pygame.sprite.Sprite):
    def __init__(self, sz):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randrange(0, w + 1)
        self.x = self.x - self.x % 10
        self.y = random.randrange(0, h + 1)
        self.y = self.y - self.y % 10
        self.size = sz
        self.image = pygame.Surface((self.size, self.size)).convert()
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, rect):
        if self.rect.colliderect(rect):
            self.x = self.rect.x = random.randrange(0, w)
            self.y = self.rect.y = random.randrange(0, h)

            self.x = self.rect.x = self.x - self.x % 10
            self.y = self.rect.y = self.y - self.y % 10

            return True


class Text:
    def __init__(self, scale, text, xpos, ypos, color):
        self.font = pygame.font.SysFont("Britannic Bold", scale)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)


def main():
    # Init vars
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((w, h), pygame.SRCALPHA)
    global s, speed

    # Game setup
    fps = 60
    clock = pygame.time.Clock()
    play = True

    # Objects
    head = Snake(w/2, h/2, size)
    dot = Dot(size)

    while play:
        score = 0
        s = 1
        restart = dead = False
        pos = [[head.rect.x, head.rect.y]]

        s_group = pygame.sprite.Group()

        while restart is False:
            # In-game vars
            if score == 5:
                s = 2
            elif score == 10:
                s = 4
            elif score == 20:
                s = 10
            r = False

            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if len(pos) == 1:
                            speed = (-s, 0)
                            r = True
                        elif speed != (s, 0):
                            speed = (-s, 0)
                            r = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if len(pos) == 1:
                            speed = (s, 0)
                            r = True
                        elif speed != (-s, 0):
                            speed = (s, 0)
                            r = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if len(pos) == 1:
                            speed = (0, -s)
                            r = True
                        elif speed != (0, 1):
                            speed = (0, -s)
                            r = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if len(pos) == 1:
                            speed = (0, s)
                            r = True
                        elif speed != (0, -s):
                            speed = (0, s)
                            r = True
                    elif event.key == pygame.K_r:
                        restart = True

            # Update
            ts = Text(75, str(score), w / 2, h/4 - h/4/2, (255, 255, 255))
            ts.rect.center = (w / 2, h / 4 - h/4/2)

            if dead is False:
                px = head.rect.x
                py = head.rect.y
                if px % size == 0:
                    pos[0][0] = head.rect.x
                if py % size == 0:
                    pos[0][1] = head.rect.y
                head.update(r)

                p = 0
                if head.rect.x % size == 0 and head.rect.y % size == 0:
                    for i in s_group:
                        p += 1
                        if i.rect.x % size == 0:
                            pos[p][0] = i.rect.x
                        if i.rect.y % size == 0:
                            pos[p][1] = i.rect.y
                        i.update(r, pos[p - 1])

                        if head.rect.x == i.rect.x and head.rect.y == i.rect.y and p > 3:
                            i.image.fill((255, 0, 0))
                            dead = True

                if dot.update(head.rect):
                    score += 1
                    body = Snake(pos[0][0], pos[0][1], size)
                    s_group.add(body)
                    pos.append([pos[0][0], pos[0][1]])

                    body.update(r, pos[p - 1])

            # Blit
            if head.rect.x % size == 0 and head.rect.y % size == 0:
                screen.fill((0, 0, 0))
                screen.blit(head.image, head.rect)
                for i in s_group:
                    screen.blit(i.image, i.rect)
            screen.blit(dot.image, dot.rect)
            screen.blit(ts.image, ts.rect)

            # Fps limiter
            clock.tick(fps)
            # Writes to main surface
            pygame.display.flip()


if __name__ == '__main__':
    main()
