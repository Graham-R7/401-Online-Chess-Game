"""
the main game
author:@techwithtim
requirements: see requirements.txt
"""

import subprocess
import sys
import get_pip

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except ImportError:
    print("[EXCEPTION] Pygame not installed")
    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except ImportError:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except Exception:
            print("[ERROR 1] Pygame could not be installed")

import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()

# Named constants
WIDTH = 750
HEIGHT = 750
BOARD_IMG_SIZE = (750, 750)
RECT = (113, 113, 525, 525)
TURN_DEFAULT = "w"

board_img = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), BOARD_IMG_SIZE)
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))
turn = TURN_DEFAULT

def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0, 0))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (WIDTH / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except Exception as e:
                    print("Server Offline", e)
                    offline = True

def redraw_gameWindow(win, bo, p1, p2, color, ready):
    win.blit(board_img, (0, 0))
    bo.draw(win, color)

    formatTime1 = f"{int(p1 // 60)}:{int(p1 % 60):02}"
    formatTime2 = f"{int(p2 // 60)}:{int(p2 % 60):02}"

    font = pygame.font.SysFont("comicsans", 30)
    try:
        txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, (255, 255, 255))
        txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, (255, 255, 255))
    except Exception as e:
        print(e)
    win.blit(txt, (520, 10))
    win.blit(txt2, (520, 700))

    txt = font.render("Press q to Quit", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (WIDTH/2 - txt3.get_width()/2, 10))

    if not ready:
        show = "Waiting for Player" if color != "s" else "Waiting for Players"
        font_large = pygame.font.SysFont("comicsans", 80)
        txt = font_large.render(show, 1, (255, 0, 0))
        win.blit(txt, (WIDTH/2 - txt.get_width()/2, 300))

    if color != "s":
        font_small = pygame.font.SysFont("comicsans", 30)
        if color == "w":
            txt3 = font_small.render("YOU ARE WHITE", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font_small.render("YOU ARE BLACK", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))

        txt3 = font_small.render("YOUR TURN" if bo.turn == color else "THEIR TURN", 1, (255, 0, 0))
        win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 700))

    pygame.display.update()

def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text, 1, (255, 0, 0))
    win.blit(txt, (WIDTH/2 - txt.get_width()/2, 300))
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT+1, 3000)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False

def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x, y = pos
    if RECT[0] < x < RECT[0] + RECT[2] and RECT[1] < y < RECT[1] + RECT[3]:
        divX = x - RECT[0]
        divY = y - RECT[1]
        i = int(divX / (RECT[2] / 8))
        j = int(divY / (RECT[3] / 8))
        return i, j
    return -1, -1

def connect():
    global n
    n = Network()
    return n.board

def main():
    global turn, bo, name
    color = bo.start_user
    count = 0
    bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if color != "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(win, "Other player left")
            run = False
            break

        if color != "s":
            if p1Time <= 0:
                bo = n.send("winner b")
            elif p2Time <= 0:
                bo = n.send("winner w")

            if bo.check_mate("b"):
                bo = n.send("winner b")
            elif bo.check_mate("w"):
                bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(win, "White is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "Black is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    bo = n.send("winner b" if color == "w" else "winner w")
                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")
                if event.key == pygame.K_LEFT:
                    bo = n.send("back")
            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
    
    n.disconnect()
    bo = 0
    menu_screen(win, name)

name = input("Please type your name: ")
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
menu_screen(win, name)
