import pyxel
from random import randint
from time import sleep

# Bienvenue dans le SNAKE !
# A vous de manger le plus de pomme possible !
# Un defis ? Obtenez un score de 25 !
# Appuyez RAPIDEMENT sur espace si vous souhaitez mettre pause 


TITLE = "SNAKE"
WIDTH = 144
HEIGHT = 104
CASE = 8

SCORE = 0
MAX_SCORE = 0
FRAME_REFRESH = 5


def reset():
    global HEAD, SNAKE, DIRECTION, FOOD, DEATH
    SNAKE = [[7,7],[6,7],[5,7]]
    HEAD = SNAKE[0]
    DIRECTION = [1,0]
    FOOD = [randint(0, WIDTH//CASE - 1), randint(0, HEIGHT//CASE - 1)]
    DEATH = False


pyxel.init(WIDTH,HEIGHT,title = TITLE)
pyxel.load("snake_sprites.pyxres")
reset()


def update():
    global DIRECTION , FOOD , SCORE,MAX_SCORE, HEAD, SNAKE, DEATH, LAST_DIRECTION
    if DIRECTION != [0,0]:
        if pyxel.frame_count % FRAME_REFRESH == 0:
            HEAD = [SNAKE[0][0] + DIRECTION[0], SNAKE[0][1] + DIRECTION[1]]
            SNAKE.insert(0, HEAD)
            SNAKE.pop(-1)

            if HEAD in SNAKE[1:] \
                    or HEAD[0] < 0 \
                    or HEAD[0] > WIDTH/CASE - 1 \
                    or HEAD[1] < 0 \
                    or HEAD[1] > HEIGHT/CASE - 1 :
                DEATH = True
                pyxel.play(0, 1)
                sleep(0.5)
                pyxel.stop()
                

            if HEAD == FOOD:
                SCORE += 1
                pyxel.play(0,0)
                if MAX_SCORE < SCORE:
                    MAX_SCORE = SCORE
                SNAKE.insert(0,FOOD)
                while FOOD in SNAKE:
                    FOOD = [randint(0, WIDTH//CASE - 1), randint(0, HEIGHT//CASE - 1)]
                

        if pyxel.btn(pyxel.KEY_ESCAPE):
            exit()
        elif pyxel.btn(pyxel.KEY_RIGHT) and DIRECTION in [[0,1], [0,-1]]:
            DIRECTION = [1,0]
        elif pyxel.btn(pyxel.KEY_LEFT) and DIRECTION in [[0,1], [0,-1]]:
            DIRECTION = [-1,0]
        elif pyxel.btn(pyxel.KEY_UP) and DIRECTION in [[1,0], [-1,0]]:
            DIRECTION = [0,-1]
        elif pyxel.btn(pyxel.KEY_DOWN) and DIRECTION in [[1,0], [-1,0]]:
            DIRECTION = [0,1]
        elif pyxel.btn(pyxel.KEY_SPACE):
            LAST_DIRECTION = DIRECTION
            DIRECTION = [0,0]
            sleep(0.3)
        elif pyxel.btn(pyxel.KEY_R):
            SCORE = 0
            reset()
            d_music()
            pyxel.playm(0, loop=True)
    else:
        if pyxel.btn(pyxel.KEY_SPACE):
            DIRECTION = LAST_DIRECTION


def draw():
    if not DEATH == True:
        if DIRECTION != [0,0]:
            pyxel.cls(0)

            for j in range(8):
                for i in range(10):
                    pyxel.blt(16*i,16*j,1,0,0,16,16)

            pyxel.text(4,4,f"SCORE : {SCORE}", 0)
            pyxel.text(4,14,f"BEST SCORE : {MAX_SCORE}", 0)

            for anneau in SNAKE[1:]:
                x, y = anneau[0], anneau[1]
                pyxel.blt(x * CASE, y * CASE, 0, 8, 0, 8, 8)

            x_HEAD, y_HEAD = SNAKE[0]
            pyxel.blt(x_HEAD * CASE, y_HEAD * CASE, 0, 0, 0, 8, 8)
            
        
            x_food,y_food = FOOD
            pyxel.blt(x_food * CASE, y_food * CASE, 2,0,0,8,8)
        else:
            pyxel.text(62,50,"PAUSE", 0)


    else:
        pyxel.cls(0)
        pyxel.text(55,40,"GAME OVER", 7)
        pyxel.text(39,50,"PRESS (R) RESTART", 7)


def d_music():
    pyxel.sounds[0].set(
        notes="c3e3g3c4c4", tones="s", volumes="4", effects=("n" * 4 + "f"), speed=7
    )
    pyxel.sounds[1].set(
        notes="f3 b2 f2 b1  f1 f1 f1 f1",
        tones="p",
        volumes=("4" * 4 + "4321"),
        effects=("n" * 7 + "f"),
        speed=9,
    )

    melody1 = (
        "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "e3 e3 e3 f3 d3 r c3 r"
        + ("r" * 8)
        + "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "b2 b2 b2 f3 d3 r c3 r"
        + ("r" * 8)
    )

    melody2 = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )

    pyxel.sounds[2].set(
        notes=melody1 * 2 + melody2 * 2,
        tones="s",
        volumes=("3"),
        effects=("nnnsffff"),
        speed=20,
    )

    harmony1 = (
        "a1 a1 a1 b1  f1 f1 c2 c2"
        "c2 c2 c2 c2  g1 g1 b1 b1"
        * 3
        + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
    )
    harmony2 = (
        ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3 + "f1" * 16 + "g1" * 16
    )

    pyxel.sounds[3].set(
        notes=harmony1 * 2 + harmony2 * 2, tones="t", volumes="5", effects="f", speed=20
    )
    pyxel.sounds[4].set(
        notes=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
        tones="n",
        volumes="6622 6622 6622 6426",
        effects="f",
        speed=20,
    )

    pyxel.musics[0].set([], [2], [3], [4])


d_music()
pyxel.playm(0, loop=True)
pyxel.run(update, draw)