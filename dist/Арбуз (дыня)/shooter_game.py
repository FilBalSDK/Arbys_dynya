import pygame
import random
from os import path

WIDTH = 700
HEIGHT = 500
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арбуз (дыня)")
clock = pygame.time.Clock()
score = 0
fail_score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (200, 75))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if len(bullets.sprites()) < 5:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteor_img, (75, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(50, 650)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.y = random.randrange(-100, -40)
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(asteroid_img, (100, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(50, 650)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.y = random.randrange(-100, -40)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (100, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -3

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


# Загрузка всей игровой графики
background = pygame.transform.scale(pygame.image.load("kvas.jpg").convert(), (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load("rocket.png").convert()
meteor_img = pygame.image.load("pig.png").convert()
bullet_img = pygame.image.load("max.png").convert()
asteroid_img = pygame.image.load("amogus.jpg").convert()
pygame.mixer.music.load("cat.ogg")
pygame.mixer.music.play(loops = -1)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    a = Asteroid()
    all_sprites.add(a)
    asteroids.add(a)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.shoot()
                shoot = pygame.mixer.Sound("shoot.ogg")
                shoot.play()

    # Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score += 1
    if score >= 100:
        running = False
    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        fail_score += 1
    ahits = pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_circle)
    if ahits:
        a = Asteroid()
        all_sprites.add(a)
        asteroids.add(a)
        fail_score += 1
    if fail_score >= 3:
        running = False
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    f1 = pygame.font.SysFont("inkfree", 25)
    text1 = f1.render('Очки: запомни в уме (а на самом деле ' + str(score) + '/100)', True, (0, 0, 0))
    screen.blit(text1, (10, 10))
    text2 = f1.render('Очки проигрыша: тоже запомни (а на самом деле ' + str(fail_score) + '/3)', True, (0, 0, 0))
    screen.blit(text2, (10, 30))
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()
