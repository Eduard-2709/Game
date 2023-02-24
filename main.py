import pygame

clock = pygame.time.Clock()
pygame.init()
w = 1600
h = 800
screen = pygame.display.set_mode((w, h)) # flags = pygame.NOFRAME - це щоб не було верхньої рамки
pygame.display.set_caption("Snake")
# Іконка гри
icon = pygame.image.load("images/snake.png").convert_alpha() # Заргружаємо фотку іконки нашої гри !
pygame.display.set_icon(icon)

#square = pygame.Surface((50, 170)) # Surface - це поверхність | (ширина, висота)
#square.fill("blue") # Малюємо наш об'єкт
#myfont = pygame.font.Font("Roboto/Roboto-Black.ttf", 40) # (назва шрифта, розмір шрифта)
# Рендеримо наш текст
#text_surface = myfont.render("Edik Bodnar", True, "red") # (самий текст, сглаживание, колір тексту)


bg_fon = pygame.image.load("images/fon.png").convert_alpha() # Для "png" - convert_alpha, а для інших розширень - convert
# Анімація
walk_left_player = [
    pygame.image.load("left/left1.png").convert_alpha(),
    pygame.image.load("left/left2.png").convert_alpha(),
    pygame.image.load("left/left3.png").convert_alpha(),
    pygame.image.load("left/left4.png").convert_alpha(),
]

walk_right_player = [
    pygame.image.load("right/right1.png").convert_alpha(),
    pygame.image.load("right/right2.png").convert_alpha(),
    pygame.image.load("right/right3.png").convert_alpha(),
    pygame.image.load("right/right4.png").convert_alpha(),
]

# Вороги
ghost = pygame.image.load("images/ghost.png").convert_alpha()
ghost_x = 1602 # Привид буде появлятися за межами екрану по x
ghost_y = 550
ghost_list = []

# Звук
bg_sound = pygame.mixer.Sound("sounds/overworld.ogg")
jump_sound = pygame.mixer.Sound("sounds/jump.ogg")
bg_sound.play() # Звук на фоні

player_anim_count = 0
bg_x = 0

# Параметри ігрока
player_speed = 15
player_x = 200 # Координати ігрока
player_y = 600
is_jump = False
jump_count = 11 # Сила прижка

# Таймер для привидів
ghost_timer = pygame.USEREVENT + 1 # "+ 1" має бути завжди !
pygame.time.set_timer(ghost_timer, 2000) # Запускаємо наш таймер, (який таймер, час). 2000 - це 2 секунда

gameplay = True # Ігра запущена

# Текст після завершення ігри
label = pygame.font.Font("Roboto/Roboto-Black.ttf", 40)
lose_label = label.render("Кінець гри, Ви програли !", True, "red")
restart_label = label.render("Грати заново", False, (193, 196, 199))
restart_label_rect = restart_label.get_rect(topleft = (670, 550))

# Рахунок і рекорд
score_stats = 0
with open("text.txt", "r") as f:
    result = f.readline()
height_score_stats = int(result)

# Життя
hearths = 3

# Пулі
bullet = pygame.image.load("images/bullet.png").convert_alpha()
bullets = [] # Список з пулями
bullets_left = 5 # Скільки пуль ми можемо випустити


running = True
while running:

    #screen.blit(square, (10, 0)) # Малюємо наш об'єкт "square" на екрані | (що малюємо, (координати де будемо малювати)) !!!
    #pygame.draw.circle(screen, "red", (250, 150), 30) # Другий спосіб як малювати об'єкти на екрані !!! | (де малюємо, колір, (координати), радіус круга)
    #screen.blit(text_surface, (300, 100))

    screen.blit(bg_fon, (bg_x, 0))
    screen.blit(bg_fon, (bg_x + w, 0))

    if gameplay:
        # Показ рекорду:
        score = label.render("Рахунок: " + str(score_stats), True, "blue")
        score_record = label.render("Рекорд: " + str(height_score_stats), True, "red")
        hearth = label.render("Життя: " + str(hearths), True, "green")
        screen.blit(score, (0, 0))
        screen.blit(score_record, (1390, 0))
        screen.blit(hearth, (700, 0))
        player_rect = walk_left_player[0].get_rect(topleft = (player_x, player_y)) # Малюємо квадрат навкруг нашого ігрока !
        if ghost_list: # Якщо є привиди в нашому списку
            for (i, el) in enumerate(ghost_list): # то ми їх перебираємо в циклі
                screen.blit(ghost, el) # і кожного привида малюємо на екрані
                el.x -= 10 # Рухаємо нашого привида по x
                if el.x < -10:
                    ghost_list.pop(i) # Видаляємо привида, коли він чучуть починати виходити за екран
                    score_stats += 1
                    if score_stats > height_score_stats:
                        height_score_stats = score_stats
                    with open("text.txt", "w") as f:
                        f.write(str(height_score_stats))
                if player_rect.colliderect(el): # Якщо квадрат нашого ігрока перетнеться з квадратом нашого пришельца
                    hearths -= 1
                    bg_sound.stop()  # Зупиняємо звук на фоні
                    if hearths > 0:
                        bullets_left = 5
                        ghost_list.clear()
                        bullets.clear()
                        running = True
                        gameplay = True
                        bg_sound.play()
                    else:
                        hearths = 3
                        ghost_list.clear()
                        bullets.clear()
                        score_stats = 0
                        gameplay = False

        keys = pygame.key.get_pressed()  # Кнопка на яку натискає користувач
        if keys[pygame.K_a]:
            screen.blit(walk_left_player[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right_player[player_anim_count], (player_x, player_y))

        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 1525:
            player_x += player_speed

        # Прижок
        if not is_jump:
            if keys[pygame.K_SPACE]:
                jump_sound.play() # Звук прижка
                is_jump = True
        else:
            if jump_count >= -11:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 11

        # Анімація
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1 # Щоб мінялися картинки коли ми ходимо !

        bg_x -= 2 # Робимо так щоб була анімація в фона !
        if bg_x == -1600:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 5
                if el.x > 1602:
                    bullets.pop(i)
                if ghost_list:
                    for (index, el_ghost) in enumerate(ghost_list):
                        if el.colliderect(el_ghost): # Якщо пуля залетіла в привида
                            ghost_list.pop(index) # Ми вбиваємо привида
                            bullets.pop(i) # І в нас зникає пуля
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (550, h / 2))
        screen.blit(restart_label, restart_label_rect) # (425, 600) - координати
        mouse = pygame.mouse.get_pos() # Дізнаємося координати мишки
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]: # Чи пересікається квадрат "Грати заново" з координатами мишки(коли ми мишку нажали)
            # pygame.mouse.get_pressed() - має три параметра. Нульовий це чи нажата ліва кнопка миші, перший це чи зажата права кнопка миші і третій це чи крутиться колеско. Ми взяли нульовий !
            gameplay = True
            bg_sound.play()  # Звук на фоні
            player_x = 200

    pygame.display.update()  # Завжди обновляє наш екран і його об'єкти

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == ghost_timer: # Якщо наш таймер привидів працює
            ghost_list.append(ghost.get_rect(topleft = (ghost_x, ghost_y))) # То ми будемо створювати тут нового привида
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft = (player_x + 30, player_y - 15)))
            bullets_left -= 1

    clock.tick(60) # Це щоб зробити анімацію повільнішою коли ходиться персонаж !