import pygame, sys, random
from pygame.math import Vector2
from sys import exit

class Button:
    def __init__(self, pos, image, text_input, base_clr, hover_clr):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.image = image
        self.base_clr = base_clr
        self.hover_clr = hover_clr
        self.text_input = text_input
        self.text = game_font.render(self.text_input, True, "white")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos + 3, self.y_pos-3))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkClick(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = game_font.render(self.text_input, True, self.hover_clr)
        else:
            self.text = game_font.render(self.text_input, True, self.base_clr)

class FRUIT:
    def __init__(self, cell_number_x, cell_number_y):
        self.fruit_img = fruit_img
        self.cell_number_x = cell_number_x
        self.cell_number_y = cell_number_y
        self.randomize([])

    def draw_fruit(self, offset):
        fruit_x = offset.x + self.pos.x * cell_size
        fruit_y = offset.y + self.pos.y * cell_size
        screen.blit(self.fruit_img, (fruit_x, fruit_y))

    def randomize(self, snake_bodies):
        while True:
            self.x = random.randint(0, self.cell_number_x - 1)
            self.y = random.randint(0, self.cell_number_y - 1)
            self.pos = Vector2(self.x, self.y)
            
            if all(self.pos not in snake.body for snake in snake_bodies if snake):
                break

class SNAKE:
    def __init__(self, start_pos, direction, color):
        self.body = start_pos
        self.direction = direction
        self.growth = False
        self.color = color

    def draw_snake(self, offset):
        for block in self.body:
            block_rect = pygame.Rect(offset.x + block.x * cell_size, offset.y + block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, block_rect, border_radius=10)

    def move_snake(self):
        if self.growth:
            self.body.insert(0, self.body[0] + self.direction)
            self.growth = False
        else:
            self.body = [self.body[0] + self.direction] + self.body[:-1]

    def grow_snake(self):
        self.growth = True

class MGAME:
    def __init__(self, mode, level):
        self.mode = mode
        self.level = level
        global cell_size, score, score_1, score_2
        score = 0
        score_1 = 0
        score_2 = 0
        self.cell_number_x, self.cell_number_y, cell_size = get_board_config(mode, level)
        global cell_number_x, cell_number_y
        cell_number_x = self.cell_number_x
        cell_number_y = self.cell_number_y
        self.board_w = cell_number_x * cell_size
        self.board_h = cell_number_y * cell_size
        self.offset  = Vector2(
            (SCREEN_WIDTH  - self.board_w) // 2,
            (SCREEN_HEIGHT - self.board_h) // 2
        )
        
        self.fruit = FRUIT(self.cell_number_x, self.cell_number_y)

        if mode == "1P":
            start_x = self.cell_number_x // 4
            start_y = self.cell_number_y // 2
            self.snake1 = SNAKE([Vector2(start_x + 1, start_y), Vector2(start_x, start_y), Vector2(start_x - 1, start_y)], Vector2(1, 0), (74, 87, 34))
            self.snake2 = None

        elif mode == "2P":
            start_y = self.cell_number_y // 2
            self.snake1 = SNAKE([Vector2(self.cell_number_x // 6, start_y), Vector2(self.cell_number_x // 6 - 1, start_y), Vector2(self.cell_number_x // 6 - 2, start_y)], Vector2(1, 0), (74, 87, 34))
            self.snake2 = SNAKE([Vector2(self.cell_number_x * 5 // 6, start_y), Vector2(self.cell_number_x * 5 // 6 + 1, start_y), Vector2(self.cell_number_x * 5 // 6 + 2, start_y)], Vector2(-1, 0), (92, 150,50))

    def check_level_complete(self):
        total_cells = self.cell_number_x * self.cell_number_y
        snake_cells = score
        if snake_cells == total_cells - 1:
            return True
        return False

    def update(self):
        self.snake1.move_snake()
        if self.snake2:
            self.snake2.move_snake()

        self.check_collision(self.snake1)
        if self.snake2:
            self.check_collision(self.snake2)

        if self.snake2:
            if self.snake1.body[0] == self.snake2.body[0]:
                return "tie",1
            if self.snake1.body[0] in self.snake2.body:
                return "win_p2",1
            elif self.snake2.body[0] in self.snake1.body:
                return "win_p1",1

            fail1 = self.check_fail(self.snake1)
            fail2 = self.check_fail(self.snake2)
            if fail1 and fail2:
                return "tie",1
            elif fail1:
                return "win_p2",1
            elif fail2:
                return "win_p1",1
        else:
            if self.check_fail(self.snake1):
                return "game_over",level


    def draw_objects(self):
        pygame.draw.rect(
            screen, (40, 70, 20),
            pygame.Rect(self.offset.x - 10, self.offset.y - 10, self.board_w + 20, self.board_h + 20),
            width=10
        )

        self.fruit.draw_fruit(self.offset)
        self.snake1.draw_snake(self.offset)
        if self.snake2:
            self.snake2.draw_snake(self.offset)

    def check_collision(self, snake):
        global highscore, mp_highscore
        if self.fruit.pos == snake.body[0]:
            self.fruit.randomize([self.snake1, self.snake2])
            snake.grow_snake()

            global score, score_1,score_2
            if self.mode == "1P":
                channel1.play(eat)
                score += score_increment
                if score > highscore:
                    highscore = score
                    save_high_score(score, "highscore.txt")
            else:
                if snake is self.snake1:
                    channel1.play(eat)
                    score_1 += score_increment
                    if score_1 > mp_highscore:
                        mp_highscore = score_1
                        save_high_score(score_1,"mp_highscore.txt")
                elif snake is self.snake2:
                    channel1.play(eat)
                    score_2 += score_increment
                    if score_2 > mp_highscore:
                        mp_highscore = score_2
                        save_high_score(score_2,"mp_highscore.txt")

    def check_fail(self, snake):
        if not (0 <= snake.body[0].x < self.cell_number_x) or not (0 <= snake.body[0].y < self.cell_number_y):
            return True
        if snake.body[0] in snake.body[1:]:
            return True
        return False

#inițializări
pygame.init()
pygame.display.set_caption("SnakeBoy")
pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2**12)

#ecran & tablă
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
cell_number_x = 20
cell_number_y = 20
cell_size = 40
offset_x = (SCREEN_WIDTH - (cell_number_x * cell_size)) // 2
offset_y = (SCREEN_HEIGHT - (cell_number_y * cell_size)) // 2
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

icon = pygame.image.load('assets/Images/icon.png').convert()
pygame.display.set_icon(icon)

#variabile joc
game_run = True
score = 0
score_1 = 0
score_2 = 0
highscore = 0
mp_highscore = 0
score_increment = 1
level = 1

#font
title_font = pygame.font.Font('assets/Font/Gamer.ttf', 120)
subtitle_font = pygame.font.Font('assets/Font/Gamer.ttf', 100)
game_font = pygame.font.Font('assets/Font/Gamer.ttf', 65)
volume_button_font = pygame.font.Font('assets/Font/Gamer.ttf', 55)

#imagini
fruit_img = pygame.transform.scale_by(pygame.image.load('assets/Images/fruit.png'),0.4).convert_alpha()
button_surface = pygame.transform.scale_by(pygame.image.load('assets/Images/button.png'), 1.70).convert_alpha()
button1_surface = pygame.transform.scale_by(pygame.image.load('assets/Images/button1.png'), 1.75).convert_alpha()
bg_surface=pygame.transform.scale_by(pygame.image.load('assets/Images/bg.png'), 1).convert_alpha()
bg_surface_rect = bg_surface.get_rect()
logo = pygame.transform.scale_by(pygame.image.load('assets/Images/logo.png'), 2.5).convert_alpha()
logo_rect = logo.get_rect()

#sunet 
vol_mus = 0.2
vol_sfx = 0.2
channel1 = pygame.mixer.Channel(1)
select = pygame.mixer.Sound('assets/Audio/button_select.mp3')
eat = pygame.mixer.Sound('assets/Audio/eat.mp3')
bgm = pygame.mixer.music.load('assets/Audio/bgm.mp3')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#creează tabla de joc
def get_board_config(mode, level):
    if mode == "1P":
        if level <= 4:
            return level*6, level*6, 40
        elif level == 5:
            return 40, 22, 40
    elif mode == "2P":
        return 35, 22, 40

#afișează bara de volum
def volumeBar(vols, slider_x, slider_y):
    slider_width = 500
    slider_height = 50
    pygame.draw.rect(screen, (0,0,0), (slider_x-3.5, slider_y-3.5, slider_width+8, slider_height+8), border_radius=8)

    pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    filled_width = int(slider_width * vols)
    pygame.draw.rect(screen, (0, 200, 0), (slider_x, slider_y, filled_width, slider_height), border_radius=5)

    volume_text = game_font.render(f"{int(vols*100)}%", True, (255, 255, 255))
    screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, slider_y-7))

#încarcă scorul maxim
def load_high_score(filename=("highscore.txt","mp_highscore.txt")):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

#salvează scorul maxim
def save_high_score(score, filename=("highscore.txt","mp_highscore.txt")):
    with open(filename, "w") as file:
        file.write(str(score))

#meniul principal
def main_menu():
    title = title_font.render("SnakeBoy", True, "white")
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 220))

    button_1p = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 100), button_surface, "1 Player", "white", (74, 87, 34))
    button_2p = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT//2), button_surface, "2 Player", "white", (74, 87, 34))
    button_options = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 100), button_surface, "Options", "white", (74, 87, 34))
    button_quit = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 200), button_surface, "Quit", "white", (74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(logo, ((SCREEN_WIDTH//2 - 345),(SCREEN_HEIGHT//2 - 360)))
        for button in [button_1p, button_2p, button_options, button_quit]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1p.checkClick(mouse_pos): 
                    channel1.play(select)
                    return "game_1p"
                if button_2p.checkClick(mouse_pos):
                    channel1.play(select) 
                    return "game_2p"
                if button_options.checkClick(mouse_pos):
                    channel1.play(select) 
                    return "options"
                if button_quit.checkClick(mouse_pos):
                    channel1.play(select) 
                    return "quit"

        pygame.display.update()
        clock.tick(60)

#bucla jocului
def game(mode, level):
    global screen, cell_number_x, cell_number_y, cell_size

    cell_number_x, cell_number_y, cell_size = get_board_config(mode,level)
    mgame = MGAME(mode, level)
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == SCREEN_UPDATE:
                result = mgame.update()
                if result:
                    return result


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and mgame.snake1.direction != Vector2(0, 1):
                    mgame.snake1.direction = Vector2(0, -1)
                if event.key == pygame.K_s and mgame.snake1.direction != Vector2(0, -1):
                    mgame.snake1.direction = Vector2(0, 1)
                if event.key == pygame.K_a and mgame.snake1.direction != Vector2(1, 0):
                    mgame.snake1.direction = Vector2(-1, 0)
                if event.key == pygame.K_d and mgame.snake1.direction != Vector2(-1, 0):
                    mgame.snake1.direction = Vector2(1, 0)

                if mgame.snake2:
                    if event.key == pygame.K_UP and mgame.snake2.direction != Vector2(0, 1):
                        mgame.snake2.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and mgame.snake2.direction != Vector2(0, -1):
                        mgame.snake2.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and mgame.snake2.direction != Vector2(1, 0):
                        mgame.snake2.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and mgame.snake2.direction != Vector2(-1, 0):
                        mgame.snake2.direction = Vector2(1, 0)

        screen.blit(bg_surface,bg_surface_rect)
        mgame.draw_objects()
        if mode == "1P":
            level_text = game_font.render(f"level: {str(level)}", True, (40, 70, 20))
            level_rect = level_text.get_rect(topleft=(20,60))
            score_text = game_font.render(f"Score: {score}", True, (40, 70, 20))
            score_rect = score_text.get_rect(topleft=(20, 20))
            screen.blit(score_text, score_rect)
            screen.blit(level_text, level_rect)

        elif mode == "2P":
            score_1_text = game_font.render(f"Score: {score_1}", True, (40, 70, 20))
            score_1_rect = score_1_text.get_rect(topleft=(40, 70))

            score_2_text = game_font.render(f"Score: {score_2}", True, (40, 70, 20))
            score_2_rect = score_2_text.get_rect(topleft=(1710, 70))

            screen.blit(score_1_text, score_1_rect)
            screen.blit(score_2_text, score_2_rect)

        if mgame.check_level_complete():
            level += 1
            if level > 5:
                return "game_won", level
            mgame = MGAME(mode,level)

        pygame.display.update()
        clock.tick(60)

#meniul de sunet
def volume():
    global vol_sfx, vol_mus
    volume_Text = subtitle_font.render("Volume", True, "white")
    volume_rect = volume_Text.get_rect(center=(SCREEN_WIDTH//2, 190))

    vol_sfx_txt = game_font.render("SFX:", True, "white")
    vol_sfx_rect = vol_sfx_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 210))
    vol_sfx1_button = Button(pos=(SCREEN_WIDTH//2 + 320, SCREEN_HEIGHT // 2 - 150), image=button1_surface, text_input="+1", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx2_button = Button(pos=(SCREEN_WIDTH//2 - 320, SCREEN_HEIGHT // 2 - 150), image=button1_surface, text_input="-1", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx3_button = Button(pos=(SCREEN_WIDTH//2 + 420, SCREEN_HEIGHT // 2 - 150), image=button1_surface, text_input="+10", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx4_button = Button(pos=(SCREEN_WIDTH//2 - 420, SCREEN_HEIGHT // 2 - 150), image=button1_surface, text_input="-10", base_clr="white", hover_clr=(74, 87, 34))

    vol_mus_txt = game_font.render("BGM:", True, "white")
    vol_mus_rect = vol_mus_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 60))
    vol_mus1_button = Button(pos=(SCREEN_WIDTH//2 + 320, SCREEN_HEIGHT // 2), image=button1_surface, text_input="+1", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus2_button = Button(pos=(SCREEN_WIDTH//2 - 320, SCREEN_HEIGHT // 2), image=button1_surface, text_input="-1", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus3_button = Button(pos=(SCREEN_WIDTH//2 + 420, SCREEN_HEIGHT // 2), image=button1_surface, text_input="+10", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus4_button = Button(pos=(SCREEN_WIDTH//2 - 420, SCREEN_HEIGHT // 2), image=button1_surface, text_input="-10", base_clr="white", hover_clr=(74, 87, 34))

    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 + 200), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))
    while True:
        
        screen.blit(bg_surface,bg_surface_rect)
        screen.blit(vol_sfx_txt, vol_sfx_rect)
        screen.blit(vol_mus_txt, vol_mus_rect)
        volume_MousePos = pygame.mouse.get_pos()
        volumeBar(vol_sfx, SCREEN_WIDTH//2 -250, SCREEN_HEIGHT // 2 - 173)
        volumeBar(vol_mus, SCREEN_WIDTH//2 -250, SCREEN_HEIGHT // 2 - 23)
        
        screen.blit(volume_Text, volume_rect)

        for button in [back_button, vol_sfx1_button, vol_sfx2_button, vol_sfx3_button, vol_sfx4_button, vol_mus1_button, vol_mus2_button, vol_mus3_button, vol_mus4_button]:
            button.changeColor(volume_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(volume_MousePos):
                    channel1.play(select)
                    return "options"

                if vol_sfx1_button.checkClick(volume_MousePos):
                    vol_sfx = round(min(vol_sfx + 0.01, 1.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_sfx2_button.checkClick(volume_MousePos):
                    vol_sfx = round(max(vol_sfx - 0.01, 0.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)
                
                if vol_sfx3_button.checkClick(volume_MousePos):
                    vol_sfx = round(min(vol_sfx + 0.1, 1.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_sfx4_button.checkClick(volume_MousePos):
                    vol_sfx = round(max(vol_sfx - 0.1, 0.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_mus1_button.checkClick(volume_MousePos):
                    vol_mus = round(min(vol_mus + 0.01, 1.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

                if vol_mus2_button.checkClick(volume_MousePos):
                    vol_mus = round(max(vol_mus - 0.01, 0.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)
                
                if vol_mus3_button.checkClick(volume_MousePos):
                    vol_mus = round(min(vol_mus + 0.1, 1.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

                if vol_mus4_button.checkClick(volume_MousePos):
                    vol_mus = round(max(vol_mus - 0.1, 0.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

        pygame.display.update()
        clock.tick(60)

#setările
def options():
    options_Text = subtitle_font.render("Options", True, "white")
    options_rect = options_Text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 -300))

    controls_button = Button(pos=(SCREEN_WIDTH // 2 - 360, SCREEN_HEIGHT//2), image=button_surface, text_input="Controls", base_clr="white", hover_clr=(74, 87, 34))
    volume_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2), image=button_surface, text_input="Volume", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 200), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))
    fullscreen_button = Button(pos=(SCREEN_WIDTH // 2 + 360, SCREEN_HEIGHT//2), image=button_surface, text_input="Fullscreen", base_clr="white", hover_clr=(74, 87, 34))
    while True:
        screen.blit(bg_surface,bg_surface_rect)

        options_MousePos = pygame.mouse.get_pos()

        screen.blit(options_Text, options_rect)

        for button in [controls_button, volume_button, fullscreen_button, back_button]:
            button.changeColor(options_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.checkClick(options_MousePos):
                    channel1.play(select)
                    pygame.display.toggle_fullscreen()

                if controls_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "controls"
                
                if volume_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "volume"

                if back_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "main_menu"

        pygame.display.update()
        clock.tick(60)

#controale
def controls():
    controls_Text = subtitle_font.render("Controls", True, "white")
    controls_rect = controls_Text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 300))

    controls_text_sg = game_font.render("Singleplayer:", True, "white")
    controls_sg_rect = controls_text_sg.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT//2 - 150))
    controls_sg_tr = game_font.render("Turn Right: D", True, "white")
    controls_sg_tr_rect = controls_sg_tr.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT//2 - 100))
    controls_sg_tu = game_font.render("Turn Up: W", True, "white")
    controls_sg_tu_rect = controls_sg_tu.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT//2 -50))
    controls_sg_tl = game_font.render("Turn Left: A", True, "white")
    controls_sg_tl_rect = controls_sg_tl.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT//2))
    controls_sg_td = game_font.render("Turn Down: S", True, "white")
    controls_sg_td_rect = controls_sg_td.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT//2 + 50))

    controls_text_mp = game_font.render("Multiplayer:", True, "white")
    controls_mp_rect = controls_text_mp.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 - 150))
    controls_mp_tr = game_font.render("Turn Right:", True, "white")
    controls_mp_tr_rect = controls_mp_tr.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 - 100))
    controls_mp_tu = game_font.render("Turn Up:", True, "white")
    controls_mp_tu_rect = controls_mp_tu.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 -50))
    controls_mp_tl = game_font.render("Turn Left:", True, "white")
    controls_mp_tl_rect = controls_mp_tl.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2))
    controls_mp_td = game_font.render("Turn Down:", True, "white")
    controls_mp_td_rect = controls_mp_td.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 + 50))


    controls_text_mp1 = game_font.render("Player 1:", True, "white")
    controls_mp1_rect = controls_text_mp.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2 - 150))
    controls_mp1_tr = game_font.render("D", True, "white")
    controls_mp1_tr_rect = controls_mp1_tr.get_rect(center=(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT//2 - 100))
    controls_mp1_tu = game_font.render("W", True, "white")
    controls_mp1_tu_rect = controls_mp1_tu.get_rect(center=(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT//2 -50))
    controls_mp1_tl = game_font.render("A", True, "white")
    controls_mp1_tl_rect = controls_mp1_tl.get_rect(center=(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT//2))
    controls_mp1_td = game_font.render("S", True, "white")
    controls_mp1_td_rect = controls_mp1_td.get_rect(center=(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT//2 + 50))

    controls_text_mp2 = game_font.render("Player 2:", True, "white")
    controls_mp2_rect = controls_text_mp2.get_rect(center=(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT//2 - 150))
    controls_mp2_tr = game_font.render("Right Arrow", True, "white")
    controls_mp2_tr_rect = controls_mp2_tr.get_rect(center=(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT//2 - 100))
    controls_mp2_tu = game_font.render("Up Arrow", True, "white")
    controls_mp2_tu_rect = controls_mp2_tu.get_rect(center=(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT//2 -50))
    controls_mp2_tl = game_font.render("Left Arrow", True, "white")
    controls_mp2_tl_rect = controls_mp2_tl.get_rect(center=(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT//2))
    controls_mp2_td = game_font.render("Down Arrow", True, "white")
    controls_mp2_td_rect = controls_mp2_td.get_rect(center=(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT//2 + 50))

    back_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 200), image=button_surface, text_input="Back", base_clr="white", hover_clr="Green")
    while True:
        screen.blit(bg_surface,bg_surface_rect)

        controls_MousePos = pygame.mouse.get_pos()

        screen.blit(controls_Text, controls_rect)
        screen.blit(controls_text_sg, controls_sg_rect)
        screen.blit(controls_sg_tr, controls_sg_tr_rect)
        screen.blit(controls_sg_tu, controls_sg_tu_rect)
        screen.blit(controls_sg_tl, controls_sg_tl_rect)
        screen.blit(controls_sg_td, controls_sg_td_rect)

        screen.blit(controls_text_mp, controls_mp_rect)
        screen.blit(controls_mp_tr, controls_mp_tr_rect)
        screen.blit(controls_mp_tu, controls_mp_tu_rect)
        screen.blit(controls_mp_tl, controls_mp_tl_rect)
        screen.blit(controls_mp_td, controls_mp_td_rect)

        screen.blit(controls_text_mp1, controls_mp1_rect)
        screen.blit(controls_mp1_tr, controls_mp1_tr_rect)
        screen.blit(controls_mp1_tu, controls_mp1_tu_rect)
        screen.blit(controls_mp1_tl, controls_mp1_tl_rect)
        screen.blit(controls_mp1_td, controls_mp1_td_rect)

        screen.blit(controls_text_mp2, controls_mp2_rect)
        screen.blit(controls_mp2_tr, controls_mp2_tr_rect)
        screen.blit(controls_mp2_tu, controls_mp2_tu_rect)
        screen.blit(controls_mp2_tl, controls_mp2_tl_rect)
        screen.blit(controls_mp2_td, controls_mp2_td_rect)

        for button in [back_button]:
            button.changeColor(controls_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(controls_MousePos):
                    channel1.play(select)
                    return "options"

        pygame.display.update()
        clock.tick(60)

#meniul după moarte
def game_over():
    game_over_text = subtitle_font.render("Game Over", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))

    highscore_Text = game_font.render(f"High Score: {load_high_score("highscore.txt")}", True, (255,255,255))
    highscore_rect = highscore_Text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3+70))

    retry_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), image=button_surface, text_input="Retry", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(highscore_Text, highscore_rect)

        for button in [retry_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    channel1.play(select)
                    return "game_1p", 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu"
                if retry_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_1p", 1

        pygame.display.update()
        clock.tick(60)

#meniul după victorie p1
def win_p1():
    game_over_text = subtitle_font.render("PLAYER 1 WINS!", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))

    mp_highscore_Text = game_font.render(f"High Score: {load_high_score("mp_highscore.txt")}", True, (255,255,255))
    mp_highscore_rect = mp_highscore_Text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3+70))

    retry_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), image=button_surface, text_input="Try Again?", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(mp_highscore_Text, mp_highscore_rect)

        for button in [retry_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu"
                if retry_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1

        pygame.display.update()
        clock.tick(60)

#meniul după victorie p2
def win_p2():
    game_over_text = subtitle_font.render("PLAYER 2 WINS!", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))

    mp_highscore_Text = game_font.render(f"High Score: {load_high_score("mp_highscore.txt")}", True, (255,255,255))
    mp_highscore_rect = mp_highscore_Text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3+70))

    retry_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), image=button_surface, text_input="Try Again?", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(mp_highscore_Text, mp_highscore_rect)

        for button in [retry_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu"
                if retry_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1

        pygame.display.update()
        clock.tick(60)

#egalitate
def tie():
    game_over_text = subtitle_font.render("TIE!", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))

    mp_highscore_Text = game_font.render(f"High Score: {load_high_score("mp_highscore.txt")}", True, (255,255,255))
    mp_highscore_rect = mp_highscore_Text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3+70))

    retry_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), image=button_surface, text_input="Try Again?", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(mp_highscore_Text, mp_highscore_rect)

        for button in [retry_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu"
                if retry_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "game_2p",1 

        pygame.display.update()
        clock.tick(60)

#meniul după terminarea jocului
def game_won():
    game_over_text = subtitle_font.render("Congratulations!", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    game_over_text_1 = subtitle_font.render("You Win!", True, "white")
    game_over_rect_1 = game_over_text_1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3+200))

    menu_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), image=button_surface, text_input="Back to menu", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(game_over_text_1, game_over_text_1_rect)

        for button in [menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu", 1

        pygame.display.update()
        clock.tick(60)

#funcția principală
def main():
    level = 1
    state = "main_menu"

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    channel1.set_volume(0.2)

    while True:
        if state == "main_menu":
            state = main_menu()
        elif state == "game_1p":
            state, level = game("1P", level)
        elif state == "game_2p":
            state, level = game("2P",level)
        elif state == "volume":
            state = volume()
        elif state == "options":
            state = options()
        elif state == "controls":
            state = controls()
        elif state == "win_p1":
            state_result = win_p1()
            if isinstance(state_result, tuple):
                state, level = state_result
            else:
                state = state_result
        elif state == "win_p2":
            state_result = win_p2()
            if isinstance(state_result, tuple):
                state, level = state_result
            else:
                state = state_result
        elif state == "tie":
            state_result = tie()
            if isinstance(state_result, tuple):
                state, level = state_result
            else:
                state = state_result
        elif state == "game_over":
            state_result = game_over()
            if isinstance(state_result, tuple):
                state, level = state_result
            else:
                state = state_result
        elif state == "game_won":
            state = game_won()
        elif state == "quit":
            pygame.quit()
            exit()

main()
