import pgzrun
from random import randint

WIDTH = 720
HEIGHT = 480

MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3

game_state = MENU
sound_enabled = True
music_playing = False

start_button = Rect((WIDTH//2 - 100, HEIGHT//2 - 50), (200, 50))
sound_button = Rect((WIDTH//2 - 100, HEIGHT//2 + 20), (200, 50))
quit_button = Rect((WIDTH//2 - 100, HEIGHT//2 + 90), (200, 50))

class Enemy:
    def __init__(self, x, y, platform):
        self.actor = Actor("enemy")
        self.actor.pos = x, y
        self.platform = platform
        self.direction = 1
        self.speed = 2
        self.animation_timer = 0
        self.current_sprite = "enemy"
    
    def update(self):
        self.actor.x += self.speed * self.direction
        
        if self.actor.right > self.platform.right:
            self.direction = -1
            self.actor.right = self.platform.right
        elif self.actor.left < self.platform.left:
            self.direction = 1
            self.actor.left = self.platform.left
        
        self.animation_timer += 1
        if self.animation_timer >= 15:
            self.animation_timer = 0
            self.current_sprite = "enemy2" if self.current_sprite == "enemy" else "enemy"
            self.actor.image = self.current_sprite
    
    def draw(self):
        self.actor.draw()

player = Actor("sprite1")
player.pos = 40, HEIGHT-70

player.vy = 0
player.vx = 0
player.animation_timer = 0
player.current_sprite = "sprite1"
player.facing_right = True

JUMP_POWER = -15
GRAVITY = 0.8
MOVE_SPEED = 5

level = 0
platforms = []
enemies = []
walk = True
dead = False
won = False
created = False

background = {
    0 : ["backg", 15, 40, HEIGHT-70],
    1 : ["backg2", 80, 40, HEIGHT-120],
    2 : ["backg3", 15, 40, HEIGHT-70],
    3 : ["backg4", 15, 40, HEIGHT-70]}

def create_platforms():
    global platforms, enemies
    platforms = []
    enemies = []
    
    base_platform = Rect((0, HEIGHT-40), (WIDTH, 40))
    platforms.append(base_platform)
    if level == 0:
        for i in range(4): 
            y = HEIGHT - 120 + i * 20
            p = Rect((150, y), (100, 20))
            platforms.append(p)
        enemies.append(Enemy(150 + 10, HEIGHT - 120 - 12, platforms[1]))

    elif level == 1:
        p1 = Rect((150, HEIGHT-60), (100, 20))
        p2 = Rect((350, HEIGHT-150), (100, 20))
        platforms.extend([p1, p2])  
        for i in range(10): 
            y = HEIGHT - 240 + i * 20
            p = Rect((550, y), (100, 20))
            platforms.append(p)
        enemies.append(Enemy(p1.x + 10, p1.y - 12, p1))
        enemies.append(Enemy(p2.x + 10, p2.y - 12, p2))
        
    elif level == 2:
        p1 = Rect((200, HEIGHT-150), (100, 20))
        platforms.append(p1)
        for i in range(9): 
            y = HEIGHT - 260 + i * 20
            p = Rect((400, y), (100, 20))
            platforms.append(p)
        for i in range(9): 
            y = HEIGHT - 220 + i * 20
            p = Rect((600, y), (100, 20))
            platforms.append(p)
        enemies.append(Enemy(p1.x + 10, p1.y - 12, p1))
        enemies.append(Enemy(400 + 10, HEIGHT - 260 - 12, platforms[2])) 
        enemies.append(Enemy(600 + 10, HEIGHT - 220 - 12, platforms[11])) 
        
    elif level == 3:
        p1 = Rect((150, HEIGHT-170), (100, 20))
        p2 = Rect((350, HEIGHT-190), (100, 20))
        p3 = Rect((550, HEIGHT-160), (100, 20))
        platforms.extend([p1, p2, p3])
        enemies.append(Enemy(p1.x + 10, p1.y + 117, p1))
        enemies.append(Enemy(p2.x + 10, p2.y + 137, p2))
        enemies.append(Enemy(p3.x + 10, p3.y + 107, p3))

def draw_menu():
    screen.fill((0, 0, 0))
    screen.draw.text("PLATFORMER GAME", (WIDTH//2 - 180, HEIGHT//4), fontsize=50, color="white")
    
    screen.draw.filled_rect(start_button, (0, 255, 0))
    screen.draw.text("Iniciar Jogo", (start_button.x + 50, start_button.y + 15), fontsize=30, color="black")
    
    screen.draw.filled_rect(sound_button, (0, 255, 0))
    sound_text = "Som: Ligado" if sound_enabled else "Som: Desligado"
    screen.draw.text(sound_text, (sound_button.x + 50, sound_button.y + 15), fontsize=30, color="black")
    
    screen.draw.filled_rect(quit_button, (0, 255, 0))
    screen.draw.text("Sair", (quit_button.x + 75, quit_button.y + 15), fontsize=30, color="black")

def draw():
    global dead
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        if dead:
            if_dead()
        else:
            if_not_dead()
    elif game_state == VICTORY:
        if_won()

def if_dead():
    global music_playing
    screen.blit(background[level][0], (0,0))
    screen.draw.text("You dead!", ((WIDTH//2-80), HEIGHT//2), fontsize=50, color="black")
    screen.draw.text("Press SPACEBAR to go back to menu", ((WIDTH//2-200), HEIGHT//2 + 50), fontsize=30, color="black")
    if music_playing:
        music.stop()
        music_playing = False

def if_not_dead():
    screen.blit(background[level][0], (0,0))
    # Desenha a plataforma base com o sprite
    screen.blit("baseplatsprite", (0, HEIGHT-40))
    
    for platform in platforms[1:]:  # Pula a primeira plataforma (base) que já foi desenhada
        if level == 0:
            screen.blit("plat0sprite", (platform.x, platform.y))
        elif level == 1:
            screen.blit("plat1sprite", (platform.x, platform.y))
        elif level == 2:
            screen.blit("plat2sprite", (platform.x, platform.y))
        elif level == 3:
            screen.blit("plat3sprite", (platform.x, platform.y))
    player.draw()
    for enemy in enemies:
        enemy.draw()

def if_won():
    global music_playing
    screen.blit(background[level][0], (0,0))
    screen.draw.text("You Won!", ((WIDTH//2-100), HEIGHT//2), fontsize=50, color="black")
    screen.draw.text("Press SPACEBAR to go back to menu", ((WIDTH//2-200), HEIGHT//2 + 50), fontsize=30, color="black")
    player.draw()
    player.pos = (WIDTH//2)+100, HEIGHT//2
    player.image = "cheer"
    player.scale = 10.0
    if music_playing:
        music.stop()
        music_playing = False

def update():
    global level, dead, won, created, game_state
    
    if game_state == PLAYING:
        if not dead:
            # Atualização da animação do player
            if player.vx != 0:
                player.animation_timer += 1
                if player.animation_timer >= 10:
                    player.animation_timer = 0
                    if player.current_sprite == "sprite1":
                        player.current_sprite = "sprite2"
                    else:
                        player.current_sprite = "sprite1"
            else:
                player.animation_timer = 0
                player.current_sprite = "idle"

            if player.vx > 0:
                player.facing_right = True
            elif player.vx < 0:
                player.facing_right = False

            if player.facing_right:
                player.image = player.current_sprite
            else:
                player.image = player.current_sprite + "left"

            player.vy += GRAVITY
            player.y += player.vy
            player.x += player.vx
            
            for platform in platforms:
                if player.colliderect(platform):
                    if player.vy > 0 and player.bottom > platform.top and player.bottom < platform.bottom:
                        player.bottom = platform.top
                        player.vy = 0
                    elif player.vy < 0 and player.top < platform.bottom and player.top > platform.top:
                        player.top = platform.bottom
                        player.vy = 0
                    elif player.right > platform.left and player.left < platform.left:
                        player.right = platform.left
                    elif player.left < platform.right and player.right > platform.right:
                        player.left = platform.right
            
            if player.left < 0:
                player.left = 0
            if player.right > WIDTH:
                if level < 3:
                    level += 1
                    screen.clear()
                    created = False
                    player.pos = 40, HEIGHT-70
                    create_platforms()
                    if sound_enabled:
                        sounds.win.play()
                else:
                    screen.clear()
                    player.pos = WIDTH//2, HEIGHT//2
                    player.image = "cheer"
                    game_state = VICTORY
                    if sound_enabled:
                        sounds.win.play()
            
            for enemy in enemies:
                enemy.update()
                if player.colliderect(enemy.actor):
                    dead = True
                    if sound_enabled:
                        sounds.lose.play()

def toggle_sound():
    global sound_enabled, music_playing
    sound_enabled = not sound_enabled
    if sound_enabled:
        if game_state == PLAYING:
            music.play('theme.wav')
            music_playing = True
    else:
        music.stop()
        music_playing = False

def on_mouse_down(pos, button):
    global game_state, sound_enabled, music_playing
    
    if game_state == MENU:
        if start_button.collidepoint(pos):
            game_state = PLAYING
            reset_game()
            if sound_enabled:
                music.play('theme.wav')
                music_playing = True
        elif sound_button.collidepoint(pos):
            toggle_sound()
        elif quit_button.collidepoint(pos):
            quit()

def on_key_down(key):
    global game_state, dead, level
    
    if game_state == PLAYING:
        if key == keys.W and player.vy == 0:
            player.vy = JUMP_POWER
        elif key == keys.D:
            player.vx = MOVE_SPEED
        elif key == keys.A:
            player.vx = -MOVE_SPEED
    
    if key == keys.SPACE and (dead or game_state == VICTORY):
        game_state = MENU
        reset_game()

def on_key_up(key):
    if key in (keys.A, keys.D):
        player.vx = 0

def reset_game():
    global level, dead, won, created, player, music_playing
    level = 0
    dead = False
    won = False
    created = False
    player.pos = 40, HEIGHT-70
    create_platforms()
    if sound_enabled and not music_playing:
        music.play('theme.wav')
        music_playing = True

create_platforms()
pgzrun.go()