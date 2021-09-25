#Модули
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

#Классы
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, size_w, size_h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + "\\Sprite\\Bird1.jpg")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (size_w, size_h))
        self.rect = self.image.get_rect(topleft = (x, y))
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Truba_Big(pygame.sprite.Sprite):
    def __init__(self, x, y, size_w, size_h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_w, size_h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft = (x, y))
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Truba_Small(pygame.sprite.Sprite):
    def __init__(self, x, y, size_w, size_h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_w, size_h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft = (x, y))
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((115, 45))
        self.image.fill((0, 191, 255))
        self.rect = self.image.get_rect(center = (x, y))
        game = font.render("Play", True, (255, 255, 255), (0, 191, 255))
        self.image.blit(game, (5, -19))

    def Click(self, x, y):
        if x > self.rect.x and x < self.rect.x + self.rect.width and y > self.rect.y and y < self.rect.y + self.rect.height:
            play_snd.play()
            return False
        else:
            return True

#Инициализация
pygame.init()

#Пременные экрана
h_s = 600
w_s = 600
screen = pygame.display.set_mode((w_s, h_s))
pygame.display.set_caption("Flappy Bird")

#Переменные циклов
menu = True
run = True
dead = True

#Звуки
exp_snd = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + "\\Sound\\Exp.wav")
jump_snd = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + "\\Sound\\Jump.wav")
play_snd = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + "\\Sound\\Play.wav")

#Шрифт
font = pygame.font.Font(os.path.dirname(os.path.abspath(__file__)) + "\\Font\\font.ttf", 40)

#Переменные объектов
#Птица
x_b = 230
y_b = 200
w_b = 100
h_b = 100
speed_b = 0

#Труба-Большая
x_t = 700
y_t = 300
w_t = 100
h_t = 300
speed_t = 7

#Труба-Маленькая
x_t_s = 1200
y_t_s = 0
w_t_s = 100
h_t_s = 250
speed_t_s = 7

#Опыт
exp = 0

#Объекты
btn_play = Button(60, 130)
bird = Bird(x_b, y_b, w_b, h_b)
trb_big = Truba_Big(x_t, y_t, w_t, h_t)
trb_small = Truba_Big(x_t_s, y_t_s, w_t_s, h_t_s)

#Циклы
#Меню
while menu:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            menu = False
            run = False
            dead = False
        
        #Нажатие на кнопку
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                pos = pygame.mouse.get_pos()
                menu = btn_play.Click(pos[0], pos[1])

    #Заливка фона
    screen.fill((0, 191, 255))
    
    #Надпись с названием игры
    name_game = font.render("Flappy Bird", True, ((255, 255, 255)))
    screen.blit(name_game, (10, 0))

    #Надпись с автором
    a = font.render("Автор: DimaK", True, ((255, 255, 255)))
    screen.blit(a, (290, 530))

    #Кнопка играть
    screen.blit(btn_play.image, btn_play.rect)

    #Переворот экрана и установление кадров в секунду
    pygame.display.flip()
    pygame.time.delay(30)

#Игра
while run:

    #Update sprite
    bird.update(x_b, y_b)
    trb_big.update(x_t, y_t)
    trb_small.update(x_t_s, y_t_s)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            menu = False
            run = False
            dead = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                speed_b = -10
                y_b += speed_b
                jump_snd.play()

    #Заливка фона
    screen.fill((0, 191, 255))

    #Птица
    screen.blit(bird.image, bird.rect)

    #Трубы
    screen.blit(trb_big.image, trb_big.rect)
    screen.blit(trb_small.image, trb_small.rect)

    #Очки
    exp_name = font.render(str(exp), True, ((255, 255, 255)))
    screen.blit(exp_name, (10, 0))

    #Падение птицы
    if y_b + h_b >= 690:
        speed_b = 0
        y_b = 690 - h_b
    else:
        y_b += speed_b
        speed_b += 1
    
    #Движение труб
    if x_t + w_t <= -1 and x_t_s + w_t_s <= -1:
        x_t = 700
        x_t_s = 1200
        exp += 1
        exp_snd.play()
    else:
        x_t -= speed_t
        x_t_s -= speed_t_s  

    #Прикосновение к нижней и верхней части экранна
    if y_b <= -50:
        run = False

    if y_b + h_b >= 700:
        run = False

    #Прикосновение к трубе
    if x_t < x_b + w_b and x_t + w_t > x_b and y_t < y_b + h_b and y_t + h_t > y_b: 
        run = False
    else:
        pass

    if x_t_s < x_b + w_b and x_t_s + w_t_s > x_b and y_t_s < y_b + h_b and y_t_s + h_t_s > y_b: 
        run = False
    else:
        pass

    #Переворот экрана и установление кадров в секунду
    pygame.display.flip()
    pygame.time.delay(30)

#Смерть
while dead:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            menu = False
            run = False
            dead = False

    #Заливка фона
    screen.fill((0, 191, 255))

    #Текст о проигрыше
    dead_name = font.render("Вы проиграли!", True, ((255, 255, 255)))
    dead_name_2 = font.render("Ваш счёт: "+ str(exp), True, ((255, 255, 255)))
    screen.blit(dead_name, (150, 150))
    screen.blit(dead_name_2, (150, 200))

    #Переворот экрана и установление кадров в секунду
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()