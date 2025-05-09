import pgzrun
from random import randint

WIDTH = 720
HEIGHT = 480

player = Actor("guy1")
enemy = Actor("enemy")
player.pos = 40,HEIGHT-70

level = 0
box_enemies = []
walk = True
dead = False
won = False
created = False

background = {
    0 : ["backg",15,40,HEIGHT-70],
    1 : ["backg2",80, 40 , HEIGHT - 120 ],
    2 : ["backg3",15,40,HEIGHT-70],
    3 : ["backg4",15,40,HEIGHT-70]
}

enemy.pos = WIDTH - 100 , background[level][3]

def draw():
    global dead,bg
    if not won:
        if dead:
            if_dead()
        else:
            if_not_dead()
    else:
        if_won()
        
def if_dead():
    screen.blit(background[level][0],(0,0))
    screen.draw.text("You Are Dead !!!",((WIDTH//2-100),HEIGHT//2),fontsize=30, color="white")
        
def if_not_dead():
    screen.blit(background[level][0],(0,0))
    player.draw()
    enemy.draw()
    draw_box_enemy()

def if_won():
    screen.blit(background[level][0],(0,0))
    screen.draw.text("You Won !!!",((WIDTH//2-100),HEIGHT//2),fontsize=30, color="white")
    player.draw()
    player.pos = (WIDTH//2)+100,HEIGHT//2
    player.image = "cheer"

def update():
    global count , bg ,level,dead , won,created
    enemy.left -=2
    move_box()
    check_collision()
    
    if not dead:
        if player.bottom >= HEIGHT-background[level][1]:
            player.pos = player.x,player.y
        else:
            gravity_done()
            
        if level == 0:
            level_find(0)
               
        elif level == 1:
            level_find(1)

        elif level == 2:
            level_find(2)

        elif level == 3:
            level_find(3)
            
        if player.left >= WIDTH:
            if level < 3:
                level +=1
                screen.clear()
                created = False
                player.pos = background[level][2],background[level][3]
                enemy.pos = WIDTH , background[level][3]
                sounds.win.play()
            else:
                screen.clear()
                player.pos = WIDTH//2,HEIGHT//2
                player.image = "cheer"
                won = True
                sounds.win.play()
    

def level_find(n):
    global created,dead
    if not created:
        num_box(n)
        created = True

    if enemy.right == 500 :
        num_box(n)
                
    if enemy.right <= 0 :
        enemy.pos = WIDTH , background[level][3]
        created = False
        num_box(n)
                
    if enemy.colliderect(player):
        dead  = True
        sounds.lose.play()
    

def num_box(num):
    if num == 0:
        create_box_enemy(randint(30,40),randint(200,299))
    elif num == 1:
        create_box_enemy(randint(30,40),randint(200,299))
        create_box_enemy(randint(0,10),randint(300,400))
    elif num==2:
        create_box_enemy(randint(30,40),randint(200,299))
        create_box_enemy(randint(0,10),randint(300,350))
        create_box_enemy(randint(20,30),randint(350,400))
    elif num == 3:
        create_box_enemy(randint(30,40),randint(200,299))
        create_box_enemy(randint(0,10),randint(300,350))
        create_box_enemy(randint(20,30),randint(350,400))
        create_box_enemy(randint(20,30),randint(400,500))
            
def create_box_enemy(width,height):
    bg = ["bluebox","greenbox","redbox","yellowbox"]
    enemy = Actor(bg[randint(0,3)])
    enemy.draw()
    enemy.pos = WIDTH -width , background[level][3]-height
    box_enemies.append(enemy)

def draw_box_enemy():
    for enemy in box_enemies:
        enemy.draw()

def move_box():
    for enemy in box_enemies:
        enemy.x -=3

def check_collision():
    global dead
    for enemy in box_enemies:
        if player.colliderect(enemy):
            dead = True
            
def gravity_done():
    player.vy = 0
    GRAVITY = 2
    uy = player.vy
    player.vy += GRAVITY
    player.y += player.vy
    
        
def on_key_down(key):
    if key == keys.UP:
        player.pos=(player.x ,player.y-80)
        player.image = "guy2"
    elif key == keys.D:
        player.pos=(player.x+50 ,player.y)
        walking()
    elif key == keys.A:
        player.pos=(player.x-50 ,player.y)
        walking()
        
def walking():
    global walk
    if walk:
        player.image = "guy1"
        sounds.footstep.play()
        walk = False
    else:
        player.image = "guy2"
        sounds.footstep.play()
        walk = True
    
pgzrun.go()