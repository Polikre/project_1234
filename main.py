import pygame
import sys
import os
import random


def load_and_processingLVL(name_lvl=None, kol_enemies=5, spawn_boss=False, percent_spawnTRAPS=50, coins=5,
                           add_bafs=True):
    if not name_lvl:
        print("Error - no name of file with lvl")
    else:
        with open(name_lvl, "r") as read_file:
            with open("data/levels/tmp.txt", "w") as output_file:
                strings = read_file.read()
                output_file.truncate(0)
                while kol_enemies or coins:
                    for i in strings:
                        skip_string = random.randint(0, 100) % 10
                        i_copy = i
                        if not skip_string:
                            output_file.write(i_copy)
                        else:
                            for symb in range(len(i)):
                                spawn_random = random.randint(0, 100)
                                if i[symb] == "." and spawn_random % 3 == 0 and kol_enemies:
                                    i_copy = i[:symb] + "+" + i[symb + 1:]
                                    kol_enemies -= 1
                                elif spawn_random % 17 == 0 and coins:
                                    i_copy = i[:symb] + "0" + i[symb + 1:]
                                    coins -= 1
                                on_this_string = random.randint(0, 100)
                                if on_this_string % 13 != 0:
                                    break
                            output_file.write(i_copy)


def generate_lvls_v2(name_lvl_udate):
    # задаем необходимые переменные
    name_lvl_udate_2 = name_lvl_udate.split("/")[-1]
    if "_0" in name_lvl_udate_2 and "1_0" not in name_lvl_udate_2 and "0_0" not in name_lvl_udate_2:  # боссы спавнятся каждые 10 лвлов, уровень с боссом имеет тип 2_0, 3_0
        spawn_boss = True
    else:
        spawn_boss = False
    with open(name_lvl_udate, "r") as input_file:
        lvl_startV = input_file.readlines()
    kol_enemies = len(lvl_startV) // 2
    kol_coins = (int(name_lvl_udate_2.split(".")[0].split("_")[0])
                 + int(name_lvl_udate_2.split(".")[0].split("_")[1])) \
                // int(name_lvl_udate_2.split(".")[0].split("_")[0])
    kol_traps = int(name_lvl_udate_2.split(".")[0].split("_")[0]) * 2

    spawn_str_enemy = kol_enemies // len(lvl_startV) + 1
    spawn_str_coins = kol_enemies // len(lvl_startV) + 1

    '''
    spawn_boss      - переменная спавна боссов, спавнятся каждые 10 лвлов тип 2_0, 3_0, 4_0 и т.д.
    lvl_startV      - поступающий на вход лвл в виде списка строк из файла
    kol_enemies     - количество врагов, зависит от размера лвла
    kol_coins       - количество монеток, зависит от уровня
    kol_traps       - количество ловушек, зависит от уровня
    spawn_str_enemy - количество врагов на одной строчке
    spawn_str_coins - колиество монеток на одной строчке
    '''

    with open("tmp.txt", "w") as work_file:
        work_file.truncate(0)
        for strings_lvl in lvl_startV:
            copy_spawn1 = spawn_str_enemy
            copy_spawn2 = spawn_str_coins
            string_refacting = strings_lvl
            for kl in range(len(strings_lvl)):
                if string_refacting[kl] == "." and copy_spawn1 >= 1 and kol_enemies >= 1:
                    copy_spawn1 -= 1
                    kol_enemies -= 1
                    string_refacting = string_refacting[:kl] + "+" + string_refacting[kl + 1:]
                if string_refacting[kl] == "." and copy_spawn2 >= 1 and kol_coins >= 1:
                    copy_spawn2 -= 1
                    kol_coins -= 1
                    string_refacting = string_refacting[:kl] + "!" + string_refacting[kl + 1:]
                if spawn_boss and string_refacting[kl] == ".":
                    spawn_boss = False
                    string_refacting = string_refacting[:kl] + "$" + string_refacting[kl + 1:]
            work_file.write(string_refacting)


def load_image(name, colorkey=None):
    # fullname = os.path.join('data', name)
    fullname = name
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", fullname)
        print(str(message))
        raise SystemExit(message)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


col = 0
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
tile_width = tile_height = 64
FPS = 50
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
corob_group = pygame.sprite.Group()
group_pyls = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
group_rewards = pygame.sprite.Group()
group_items = pygame.sprite.Group()
SHIELD_TIMER = 50
HERO_SIZE = 40, 40
BLOCK_SIZE = 68, 68


pygame.init()
player_image = load_image('data/heroes/boss2.jpg', colorkey=-1)
tile_images = {
    'wall': load_image('data/floors_walls/wall.jpg'),
    'empty': load_image('data/floors_walls/floor2.jpg'),
    'enemy_1': load_image('data/heroes/enemy_1.png', -1),
    'trap': load_image('data/floors_walls/trap_1_lava.jpg'),
    'chest': load_image('data/bafs&dops/reward.jpg'),
    'hp_baff': load_image('data/bafs&dops/hp_add.jpg', -1),
    'enemy_1_harted': load_image('data/heroes/enemy_1_harted.png', -1),
    'game_over': load_image('data/game_over/gameover.jpg'),
    'shield': load_image('data/heroes/shield_fon.jpg', -1),
    'potion': load_image('data/bafs&dops/potion.png', -1),
    'sword': load_image('data/bafs&dops/sword.png', -1),
    'money': load_image('data/bafs&dops/money.png', -1),
    'key': load_image('data/bafs&dops/key.png', -1),
    'enemy_2': load_image('data/heroes/enemy_2.jpg', -1),
    'enemy_2_harted': load_image('data/heroes/enemy_2_harted.png', -1),
}


def generate_level(level):
    new_player, x, y = (None, None), None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = (x, y)
            elif level[y][x] == '!':
                Trap('trap', x, y) # ловушка
            elif level[y][x] == '?':
                Tile('empty', x, y)
                Items('potion-', x, y) # замедление
            elif level[y][x] == '%':
                Tile('empty', x, y)
                Items('potion+', x, y)  # ускорение
            elif level[y][x] == '*':
                Chest('chest', x, y)  # сундук
            elif level[y][x] == '$':
                Tile('empty', x, y)
                Enemy(x, y, 3)
            elif level[y][x] == '1':
                Tile('empty', x, y)
                Enemy(x, y, 1)  # враг
            elif level[y][x] == '2':
                Tile('empty', x, y)
                Enemy(x, y, 2)  # враг
            elif level[y][x] == '0':
                Tile('empty', x, y)
                Items('money', x, y)  # монетки
            elif level[y][x] == '_':
                Tile('empty', x, y)
                Items('hp_baff', x, y)
            elif level[y][x] == '/':
                Tile('empty', x, y)
                Items('sword', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                Items('key', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Trap(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(trap_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[image], BLOCK_SIZE)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.attack = 1

    def return_coords(self):
        return [self.rect.x, self.rect.y]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(tiles_group, all_sprites, corob_group)
        else:
            super().__init__(tiles_group, all_sprites)

        self.image = pygame.transform.scale(tile_images[tile_type], BLOCK_SIZE)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, HERO_SIZE)

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update__(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, HERO_SIZE)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.animated_class = AnimatedSprite(load_image("data/heroes/dragon_sheet8x2.png"),
                                             8, 2)
        self.image = self.animated_class.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 5)
        self.health = 3
        self.score = 0
        self.vec = 5
        self.key = False
        self.napr = "up"
        self.napr_tmp = 0
        self.game_over = False
        self.walk = False
        self.x_shag = None
        self.y_shag = None
        self.shield = False
        self.shield_count = 0
        self.count_tmp = 0
        self.next_level = False
        self.attack = 1

    def update_animation(self):
        self.animated_class.update__()
        self.image = self.animated_class.image
        if self.napr == "right":
            self.napr_tmp = 1
        if self.napr == "left":
            self.napr_tmp = 0
        if self.shield:
            if self.shield_count == 0:
                self.image = tile_images['shield']
                self.image = pygame.transform.scale(self.image, HERO_SIZE)
            self.shield_count = (self.shield_count + 1) % 2
        self.image = pygame.transform.flip(self.image, self.napr_tmp, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def update_(self, coords):
        if not self.game_over:
            self.rect = self.rect.move(coords[0], coords[1])
            if pygame.sprite.spritecollideany(self, corob_group):
                self.rect = self.rect.move(-coords[0], -coords[1])
            if pygame.sprite.spritecollideany(self, enemy_group) and not self.shield:
                coords_p = self.return_coords()
                for i in enemy_group:
                    coords_e = i.return_coords()
                    if abs(coords_p[0] - coords_e[0]) <= 80:
                        if abs(coords_p[1] - coords_e[1]) <= 80:
                            i.update_health(-self.attack)
                            self.update_health(-i.attack)
                self.shield = True
                self.shield_count = 0
                self.count_tmp = 0
            if pygame.sprite.spritecollideany(self, trap_group) and not self.shield:
                coords_p = self.return_coords()
                for i in trap_group:
                    tmp_damage = i.attack
                self.update_health(-tmp_damage)
                self.shield = True
                self.shield_count = 0
                self.count_tmp = 0
            x_add = coords[0]
            y_add = coords[1]
            if x_add != 0 or y_add != 0:
                if x_add == self.vec:
                    self.napr = "right"
                elif x_add == -self.vec:
                    self.napr = "left"
                elif y_add == -self.vec:
                    self.napr = "up"
                else:
                    self.napr = "down"
            if pygame.sprite.spritecollideany(self, group_rewards) and self.key:
                self.next_level = True

    def update_health(self, wht):
        if type(wht) == int:
            self.health += wht
        if self.health > 3:
            self.health = 3
        elif self.health <= 0:
            self.game_over = True
            # КОНЕЦ ИГРЫ

    def return_napr(self):
        return self.napr

    def return_coords(self):
        return [self.rect.x, self.rect.y]

    def return_xp(self):
        return self.health

    def update_shield(self):
        if self.shield:
            self.count_tmp += 1
            if self.count_tmp == SHIELD_TIMER:
                self.shield = False

    def update_vec(self):
        if self.x_shag < 0:
            self.x_shag = -self.vec
        elif self.y_shag < 0:
            self.y_shag = -self.vec
        elif self.x_shag > 0:
            self.x_shag = self.vec
        elif self.y_shag > 0:
            self.y_shag = self.vec


class Items(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(group_items, all_sprites)
        self.type = type
        if type[:-1] == "potion":
            type = type[:-1]
        self.image = pygame.transform.scale(tile_images[type], BLOCK_SIZE)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update_(self):
        if pygame.sprite.spritecollideany(self, player_group):
            if self.type == "potion-":
                player.vec -= 2
                if player.vec <= 0:
                    player.vec = 1
                player.update_vec()
            if self.type == "potion+":
                player.vec += 2
                if player.vec > 9:
                    player.vec = 9
                player.update_vec()
            if self.type == "money":
                player.score += 1
            if self.type == "sword":
                player.attack = 2
            if self.type == "key":
                player.key = True
            if self.type == "hp_baff":
                player.update_health(1)
            self.kill()


class Chest(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(group_rewards, all_sprites)
        self.image = pygame.transform.scale(tile_images[image], BLOCK_SIZE)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y + 5)


'''    class Pyla(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, image_pyl, napr):
            super().__init__(group_pyls, all_sprites)
            self.image = pygame.transform.scale(load_image(image_pyl), (30, 30))
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.x = pos_x
            self.y = pos_y
            self.napr = napr
    
         def update_(self):
            if self.napr == "left":
                self.add = [-50, 0]
            elif self.napr == "right":
                self.add = [50, 0]
            elif self.napr == "down":
                self.add = [0, -50]
            else:
                self.add = [0, 50]'''


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type):
        super().__init__(enemy_group, all_sprites)
        self.type = f"enemy_{type}"
        self.type_h = f"{self.type}_harted"
        self.image = pygame.transform.scale(tile_images[self.type], BLOCK_SIZE)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if type == 1:
            self.health = 2
            self.attack = 1
        if type == 2:
            self.health = 5
            self.attack = 2
        if type == 3:
            self.health = 10
            self.attack = 3
        self.mask = pygame.mask.from_surface(self.image)

    # def update_(self, coords):
    #     self.rect = self.rect.move(coords[0], coords[1])
    #     if pygame.sprite.spritecollideany(self, corob_group):
    #         self.rect = self.rect.move(-coords[0], -coords[1])

    def update_health(self, wht):
        global screen
        if type(wht) == int:
            self.health += wht
        if wht < 0:
            self.image = pygame.transform.scale(tile_images[self.type_h], BLOCK_SIZE)
            screen.blit(self.image, self.return_coords())
            clock.tick(100)
            screen.blit(self.image, self.return_coords())
            enemy_group.draw(screen)
        if self.health <= 0:
            self.kill()

    def return_coords(self):
        return [self.rect.x, self.rect.y]


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception:
        print(f"Ошибка. Файла {filename} не существует в памяти")


def terminate():
    game_over()
    pygame.quit()


def start_screen():
    intro_text = ["                                          ТАЙНЫ ПОДЗЕМЕЛИЙ", "",
                  "Управление:",
                  "   стрелочки - движение",
                  "   R - атака (in develop)",
                  "   Esc - выход"]
    screen = pygame.display.set_mode((720, 439))
    fon = pygame.transform.scale(load_image('data/floors_walls/fon.jpg'), (720, 439))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.mixer.music.load("data/music/main_level.mp3")
        pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fl = 1
                return fl == 0
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                fl = 0
                return fl == 0
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    a_sprites = pygame.sprite.Group()
    arrow_image = tile_images["game_over"]
    arrow_image = pygame.transform.scale(arrow_image, (WIDTH, HEIGHT))
    sprite = pygame.sprite.Sprite(a_sprites)
    sprite.image = arrow_image
    sprite.rect = sprite.image.get_rect()
    x, y = -WIDTH, 0
    v = 200
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        x += int(v / fps)
        clock.tick(fps)
        sprite.rect.x = x
        sprite.rect.y = y
        a_sprites.draw(screen)
        pygame.display.flip()
        if x >= WIDTH - sprite.image.get_size()[0]:
            v = 0
    pygame.quit()


levels = [2, 2]
fl = start_screen()
fl_died = 0
SCORE = 0
if fl:
    for i in levels:
        if fl_died == 0:
            hp_1, hp_2, hp_3 = pygame.transform.scale(load_image("data/heroes/cerd.jpg", -1), (40, 40)), pygame.transform.scale(
                load_image("data/heroes/cerd.jpg", -1), (40, 40)), pygame.transform.scale(
                load_image("data/heroes/cerd.jpg", -1),
                (40, 40))
            hp_1r = hp_1.get_rect(center=(370, 20))
            hp_2r = hp_2.get_rect(center=(420, 20))
            hp_3r = hp_3.get_rect(center=(470, 20))

            sp_images_hp = [hp_3, hp_2, hp_1]
            sp_rects_hp = [hp_3r, hp_2r, hp_1r]
            name_lvl = f"levels/1_{i}.txt"
            camera = Camera()
            player0, level_x, level_y = generate_level(load_level(name_lvl))
            player = Player(player0[0], player0[1])
            screen = pygame.display.set_mode(size)
            fps = 100
            clock_fps = 30
            running = True
            pygameSurface = pygame.transform.scale(pygame.image.load('data/floors_walls/EEhho.png'), (500, 500))
            pygameSurface.set_alpha(190)
            sp_pyls = []
            pygame.mixer.music.load("data/music/main.mp3")
            pygame.mixer.music.play(-1)
            WALK = False
            while running:
                # внутри игрового цикла ещё один цикл
                # приема и обработки сообщений
                for event in pygame.event.get():
                    # при закрытии окна
                    if event.type == pygame.QUIT:
                        running = False
                        fl_died = 1
                        fl = False
                    elif event.type == pygame.KEYDOWN and not WALK:
                        if event.key == pygame.K_UP:
                            player.x_shag = 0
                            player.y_shag = -player.vec
                            WALK = True
                            player.walk = True
                        elif event.key == pygame.K_LEFT:
                            player.x_shag = -player.vec
                            player.y_shag = 0
                            WALK = True
                            player.walk = True
                        elif event.key == pygame.K_RIGHT:
                            player.x_shag = player.vec
                            player.y_shag = 0
                            WALK = True
                            player.walk = True
                        elif event.key == pygame.K_DOWN:
                            player.x_shag = 0
                            player.y_shag = player.vec
                            WALK = True
                            player.walk = True
                        elif event.key == pygame.K_r:
                            napr = player.return_napr()
                            coords_player = player.return_coords()
                            if napr == "down":
                                coords_player[1] += 50
                            elif napr == "up":
                                coords_player[1] -= 50
                            elif napr == "left":
                                coords_player[0] -= 50
                            elif napr == "right":
                                coords_player[0] += 50
                            coords_player[0] -= 10
                            coords_player[1] -= 5
                            for i in enemy_group:
                                if abs(coords_player[0] - i.return_coords()[0]) <= 30:
                                    if abs(coords_player[1] - i.return_coords()[1]) <= 30:
                                        i.update_health(-player.attack)
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.KEYUP and WALK:
                        WALK = False
                        player.walk = False
                        player.update_([0, 0])
                if player.next_level:
                    SCORE += player.score
                    break
                if player.game_over:
                    fl_died = 1
                    break
                if WALK:
                    player.update_([player.x_shag, player.y_shag])
                if player.game_over:
                    fl_died = 1
                    break
                camera.update(player)
                screen.fill((0, 0, 0))
                # screen.blit(picture, (0, 0), (0, 0, 500, 500))
                # screen.blit(world, pygame.rect.Rect(0, 0, 500, 500))
                # обновляем положение всех спрайтов
                for i in sp_pyls:
                    i.update_()
                for i in group_items:
                    i.update_()
                for sprite in all_sprites:
                    camera.apply(sprite)
                # print(player.rect)
                # отрисовка и изменение свойств объектов
                # screen.fill((139, 0, 0))
                all_sprites.update()
                all_sprites.draw(screen)
                # player_group.draw(screen)
                # обновление экрана
                # clock.tick(fps)
                screen.blit(pygameSurface, pygameSurface.get_rect(center=screen.get_rect().center))
                for i in range(player.return_xp()):
                    screen.blit(sp_images_hp[i], sp_rects_hp[i])
                player_group.draw(screen)
                if player.shield:
                    player.update_shield()
                clock.tick(fps)
                clock.tick(clock_fps)
                player.update_animation()
                pygame.display.flip()
            player = None
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            corob_group = pygame.sprite.Group()
            group_pyls = pygame.sprite.Group()
            trap_group = pygame.sprite.Group()
            group_rewards = pygame.sprite.Group()
            group_items = pygame.sprite.Group()
if fl:
    game_over()
    print(f"Your score: {SCORE}")
pygame.quit()