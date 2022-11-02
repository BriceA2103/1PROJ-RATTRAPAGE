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


class Plateau:
    def __init__(self):
        self.plateau = [[Pion(pionNoir, 1, pionNoir.get_rect(), 0, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 1),
                         Pion(pionNoir, 1, pionNoir.get_rect(), 0, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 3),
                         Pion(pionNoir, 1, pionNoir.get_rect(), 0, 4)],
                        [Pion(pionNoir, 1, pionNoir.get_rect(), 1, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 1),
                         Pion(pionNoir, 1, pionNoir.get_rect(), 1, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 3),
                         Pion(pionNoir, 1, pionNoir.get_rect(), 1, 4)],
                        [Pion(pionNoir, 1, pionNoir.get_rect(), 2, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 2, 1),
                         Pion(pionNeutre, 0, pionNeutre.get_rect(), 2, 2),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 3),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 4)],
                        [Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 1),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 3),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 4)],
                        [Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 1),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 3),
                         Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 4)]]

    # plateau = [[Pion(pionNoir, 1, pionNoir.get_rect(), 0, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 1),
    #             Pion(pionNoir, 1, pionNoir.get_rect(), 0, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 3),
    #             Pion(pionNoir, 1, pionNoir.get_rect(), 0, 4)],
    #            [Pion(pionNoir, 1, pionNoir.get_rect(), 1, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 1),
    #             Pion(pionNoir, 1, pionNoir.get_rect(), 1, 2), Pion(pionNoir, 1, pionNoir.get_rect(), 1, 3),
    #             Pion(pionNoir, 1, pionNoir.get_rect(), 1, 4)],
    #            [Pion(pionNoir, 1, pionNoir.get_rect(), 2, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 2, 1),
    #             Pion(pionNeutre, 0, pionNeutre.get_rect(), 2, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 3),
    #             Pion(pionBlanc, 2, pionBlanc.get_rect(), 2, 4)],
    #            [Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 1),
    #             Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 3),
    #             Pion(pionBlanc, 2, pionBlanc.get_rect(), 3, 4)],
    #            [Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 0), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 1),
    #             Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 2), Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 3),
    #             Pion(pionBlanc, 2, pionBlanc.get_rect(), 4, 4)]]

    def drawBoard(self):
        screen.blit(background, background.get_rect())
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                self.plateau[i][j].rect.topleft = ((165 * (j + 0.15)), (155 * (i + 0.15)))
                if self.plateau[i][j].image != pionNeutre:
                    screen.blit(self.plateau[i][j].image, self.plateau[i][j].rect)
        pygame.display.update()

    def getPion(self, event):
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j].image is not None and (
                        self.plateau[i][j].rect.collidepoint(event.pos[0], event.pos[1])) is True:
                    return i, j
        return False

    def getListeVoisins(self, pion):
        listeVoisins = []
        x = pion.x
        y = pion.y
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x + y) % 2 == 0:
                    if 0 <= x + i <= len(self.plateau) - 1 and 0 <= y + j <= len(self.plateau) - 1 and (
                            i != 0 or j != 0):
                        listeVoisins.append(self.plateau[x + i][y + j])
                else:
                    if 0 <= x + i <= len(self.plateau) - 1 and 0 <= y + j <= len(self.plateau) - 1 and (
                            (x + i == x) != (y + j == y)):
                        listeVoisins.append(self.plateau[x + i][y + j])
        return listeVoisins

    def possible(self, pion1, pion2):
        if pion2 in self.getListeVoisins(pion1) and pion2.joueur == 0:
            return True
        return False

    def possibleCapture(self, pion1, pion2):
        if ((pion1.x + pion2.x) % 2 == 0) and ((pion1.y + pion2.y) % 2 == 0):
            pionMid = self.plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)]
            pionMid.x = math.floor((pion1.x + pion2.x) / 2)
            pionMid.y = math.floor((pion1.y + pion2.y) / 2)
            if pion2.joueur == 0 and pionMid.joueur != pion1.joueur and pionMid.joueur != 0 and pionMid in self.getListeVoisins(
                    pion1) and pionMid in self.getListeVoisins(pion2) and (
                    (pion1.x < pionMid.x < pion2.x or pion1.x > pionMid.x > pion2.x) or (
                    pion1.y < pionMid.y < pion2.y or pion1.y > pionMid.y > pion2.y)):
                return True
        return False

    def otherCapture(self, joueur):
        listeCapture = []
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j].joueur == joueur:
                    for k in self.getListeVoisins(self.plateau[i][j]):
                        for l in self.getListeVoisins(k):
                            if self.possibleCapture(self.plateau[i][j], l) and (
                                    self.plateau[i][j], l) not in listeCapture:
                                listeCapture.append((self.plateau[i][j], l))
        return listeCapture

    def remove(self, pion1):
        pion1.joueur = 0
        pion1.image = pionNeutre
        print("Tu n'as pas capturé")

    def move(self, pion1, pion2):
        pion2.joueur = pion1.joueur
        pion2.image = pion1.image
        pion1.joueur = 0
        pion1.image = pionNeutre

    def capture(self, pion1, pion2):
        self.plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)].joueur = 0
        self.plateau[math.floor((pion1.x + pion2.x) / 2)][math.floor((pion1.y + pion2.y) / 2)].image = pionNeutre
        pion2.joueur = pion1.joueur
        pion2.image = pion1.image
        pion1.joueur = 0
        pion1.image = pionNeutre

    def play(self, pion1, pion2, joueur, players):
        # global player
        if len(self.otherCapture(joueur)) >= 1 and self.possible(pion1, pion2):
            self.remove(pion1)
            joueur = next(players)
            return joueur
        elif self.possible(pion1, pion2):
            self.move(pion1, pion2)
            joueur = next(players)
            return joueur
        elif self.possibleCapture(pion1, pion2):
            self.capture(pion1, pion2)
            if len(self.otherCapture(joueur)) >= 1 and (pion1, pion2) not in self.otherCapture(joueur):
                return joueur
            else:
                joueur = next(players)
                return joueur
        else:
            return joueur

    def victory(self):
        cnt1 = 0
        cnt2 = 0
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                for k in range(len(self.plateau)):
                    for l in range(len(self.plateau[k])):
                        if self.plateau[i][j].joueur == 1 and (
                                self.possible(self.plateau[i][j], self.plateau[k][l]) or self.possibleCapture(
                            self.plateau[
                                i][
                                j],
                            self.plateau[
                                k][
                                l])):
                            cnt1 += 1
                        elif self.plateau[i][j].joueur == 2 and (
                                self.possible(self.plateau[i][j], self.plateau[k][l]) or self.possibleCapture(
                            self.plateau[
                                i][
                                j],
                            self.plateau[
                                k][
                                l])):
                            cnt2 += 1
        if cnt1 == 0:
            return True, 2
        elif cnt2 == 0:
            return True, 1
        return False

def game():
    run = True
    firstPion, secondPion = None, None
    players = cycle([2, 1])
    player = next(players)
    plateau = Plateau()
    while run:
        plateau.drawBoard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                if firstPion is None:
                    if plateau.getPion(event) is not False:
                        firstPion = plateau.plateau[plateau.getPion(event)[0]][plateau.getPion(event)[1]]
                        firstPion.x = plateau.getPion(event)[0]
                        firstPion.y = plateau.getPion(event)[1]
                        print("firstPion")
                elif secondPion is None:
                    if plateau.getPion(event) is not False:
                        secondPion = plateau.plateau[plateau.getPion(event)[0]][plateau.getPion(event)[1]]
                        secondPion.x = plateau.getPion(event)[0]
                        secondPion.y = plateau.getPion(event)[1]
                        print("secondPion")
                if firstPion is not None and secondPion is not None:
                    if firstPion.joueur == player and secondPion.joueur == 0:
                        player = plateau.play(firstPion, secondPion, player, players)
                        if player == 1:
                            print("\nJoueur noir\n")
                        else:
                            print("\nJoueur blanc\n")
                    firstPion, secondPion = None, None
                if plateau.victory():
                    if plateau.victory()[1] == 1:
                        print("Le joueur noir a gagné")
                    else:
                        print("Le joueur blanc a gagné")
                    plateau.plateau = [
                        [Pion(pionNoir, 1, pionNoir.get_rect(), 0, 0), Pion(pionNoir, 1, pionNoir.get_rect(), 0, 1),
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
game()
