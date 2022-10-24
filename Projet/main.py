import math

import pygame
from pygame.locals import *
from itertools import cycle

pygame.init()
screen = pygame.display.set_mode((750, 722))
background_image = "image/background_alquerque.jpg"
pygame.display.set_caption('Alquerque')
pionNoir = pygame.image.load("image/pion1.png")
pionBlanc = pygame.image.load("image/pion2.png")
pionNeutre = pygame.image.load("image/pion0.png")
background = pygame.image.load(background_image).convert()


class Pion(pygame.sprite.Sprite):
    def __init__(self, image, joueur, rect, x, y):
        super().__init__()
        self.image = image
        self.joueur = joueur
        self.rect = rect
        self.x = x
        self.y = y


plateau = [[Pion(pionNoir, 1, pionNoir.get_rect(), 0, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 1),
            Pion(pionNoir, 1, pionNoir.get_rect(), 0, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 3),
            Pion(pionNoir, 1, pionNoir.get_rect(), 0, 4)],
           [Pion(pionNoir, 1, pionNoir.get_rect(), 1, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 1),
            Pion(pionNoir, 1, pionNoir.get_rect(), 1, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 3),
            Pion(pionNoir, 1, pionNoir.get_rect(), 1, 4)],
           [Pion(pionNoir, 1, pionNoir.get_rect(), 2, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 2, 1),
            Pion(pionNeutre, 0, pionNeutre.get_rect(), 2, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 3),
            Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 4)],
           [Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 1),
            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 3),
            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 4)],
           [Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 1),
            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 3),
            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 4)]]


def drawBoard():
    screen.blit(background, background.get_rect())
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            plateau[i][j].rect.topleft = ((165 * (j + 0.15)), (155 * (i + 0.15)))
            if plateau[i][j].image != pionNeutre:
                screen.blit(plateau[i][j].image, plateau[i][j].rect)
    pygame.display.update()


def getPion():
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j].image is not None and (
                    plateau[i][j].rect.collidepoint(event.pos[0], event.pos[1])) is True:
                return i, j
    return False


def getVoisinsList(pion):
    listeVoisins = []
    x = pion.x
    y = pion.y
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (x + y) % 2 == 0:
                if 0 <= x + i <= len(plateau) - 1 and 0 <= y + j <= len(plateau) - 1 and (i != 0 or j != 0):
                    listeVoisins.append(plateau[x + i][y + j])
            else:
                if 0 <= x + i <= len(plateau) - 1 and 0 <= y + j <= len(plateau) - 1 and ((x + i == x) != (y + j == y)):
                    listeVoisins.append(plateau[x + i][y + j])
    return listeVoisins


def possible(pion1, pion2):
    if pion2 in getVoisinsList(pion1) and pion2.joueur == 0:
        return True
    return False


def possibleCapture(pion1, pion2):
    if ((pion1.x + pion2.x) % 2 == 0) and ((pion1.y + pion2.y) % 2 == 0):
        pionMid = plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)]
        pionMid.x = math.floor((pion1.x + pion2.x) / 2)
        pionMid.y = math.floor((pion1.y + pion2.y) / 2)
        if pion2.joueur == 0 and pionMid.joueur != pion1.joueur and pionMid.joueur != 0 and pionMid in getVoisinsList(
                pion1) and pionMid in getVoisinsList(pion2) and (
                (pion1.x < pionMid.x < pion2.x or pion1.x > pionMid.x > pion2.x) or (
                pion1.y < pionMid.y < pion2.y or pion1.y > pionMid.y > pion2.y)):
            return True
    return False


def otherCapture(joueur):
    listeCapture = []
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j].joueur == joueur:
                for k in getVoisinsList(plateau[i][j]):
                    for l in getVoisinsList(k):
                        if possibleCapture(plateau[i][j], l) and (
                                plateau[i][j], l) not in listeCapture:
                            listeCapture.append((plateau[i][j], l))
    return listeCapture


def play(pion1, pion2):
    global player
    if len(otherCapture(player)) >= 1 and possible(pion1, pion2):
        pion1.joueur = 0
        pion1.image = pionNeutre
        player = next(players)
        return True
    elif possible(pion1, pion2):
        pion2.joueur = pion1.joueur
        pion2.image = pion1.image
        pion1.joueur = 0
        pion1.image = pionNeutre
        player = next(players)
        return True
    elif possibleCapture(pion1, pion2):
        plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)].joueur = 0
        plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)].image = pionNeutre
        pion2.joueur = pion1.joueur
        pion2.image = pion1.image
        pion1.joueur = 0
        pion1.image = pionNeutre
        if len(otherCapture(player)) >= 1:
            if (pion1, pion2) not in otherCapture(player):
                return True
        else:
            player = next(players)
            return True
    else:
        return False


def victory():
    cnt1 = 0
    cnt2 = 0
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j].joueur == 1:
                cnt1 += 1
            elif plateau[i][j].joueur == 2:
                cnt2 += 1
            elif plateau[i][j].joueur == 2:
                for k in range(len(plateau)):
                    for l in range(len(plateau[k])):
                        if possible(plateau[i][j], plateau[k][l]) or possibleCapture(plateau[i][j], plateau[k][l]):
                            cnt2 += 1
            elif plateau[i][j].joueur == 2:
                for k in range(len(plateau)):
                    for l in range(len(plateau[k])):
                        if possible(plateau[i][j], plateau[k][l]) or possibleCapture(plateau[i][j], plateau[k][l]):
                            cnt1 += 1

    if cnt1 == 0:
        return True, 2
    elif cnt2 == 0:
        return True, 1
    return False


run = True
firstPion, secondPion = None, None
players = cycle([2, 1])
player = next(players)
while run:
    drawBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            if firstPion is None:
                if getPion() is not False:
                    firstPion = plateau[getPion()[0]][getPion()[1]]
                    firstPion.x = getPion()[0]
                    firstPion.y = getPion()[1]
                    print("firstPion")
            elif secondPion is None:
                if getPion() is not False:
                    secondPion = plateau[getPion()[0]][getPion()[1]]
                    secondPion.x = getPion()[0]
                    secondPion.y = getPion()[1]
                    print("secondPion")
            if firstPion is not None and secondPion is not None:
                if firstPion.joueur == player and secondPion.joueur == 0:
                    play(firstPion, secondPion)
                    if player == 1:
                        print("\nJoueur noir\n")
                    else:
                        print("\nJoueur blanc\n")
                firstPion, secondPion = None, None
            if victory():
                if victory()[1] == 1:
                    print("Le joueur noir a gagné")
                else:
                    print("Le joueur blanc a gagné")
                plateau = [[Pion(pionNoir, 1, pionNoir.get_rect(), 0, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 1),
                            Pion(pionNoir, 1, pionNoir.get_rect(), 0, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 3),
                            Pion(pionNoir, 1, pionNoir.get_rect(), 0, 4)],
                           [Pion(pionNoir, 1, pionNoir.get_rect(), 1, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 1),
                            Pion(pionNoir, 1, pionNoir.get_rect(), 1, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 3),
                            Pion(pionNoir, 1, pionNoir.get_rect(), 1, 4)],
                           [Pion(pionNoir, 1, pionNoir.get_rect(), 2, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 2, 1),
                            Pion(pionNeutre, 0, pionNeutre.get_rect(), 2, 2),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 3),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 4)],
                           [Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 0),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 1),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 2),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 3),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 4)],
                           [Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 0),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 1),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 2),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 3),
                            Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 4)]]
                if player == 1:
                    player = next(players)

pygame.quit()
quit()
