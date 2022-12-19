import math

import pygame
from pygame.locals import *
from itertools import cycle

pygame.init()
screen = pygame.display.set_mode((750, 722))
background_image = "image/background_alquerque.jpg"
pygame.display.set_caption('Alquerque')
blackPawn = pygame.image.load("image/pion1.png")
whitePawn = pygame.image.load("image/pion2.png")
neutralPawn = pygame.image.load("image/pion0.png")
background = pygame.image.load(background_image).convert()


class Pawn(pygame.sprite.Sprite):
    def __init__(self, image, player, rect, x, y):
        super().__init__()
        self.image = image
        self.player = player
        self.rect = rect
        self.x = x
        self.y = y


class Board:
    def __init__(self):
        self.board = [[Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 1),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 3),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 4)],
                        [Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 1),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 3),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 4)],
                        [Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 1),
                         Pawn(neutralPawn, 0, neutralPawn.get_rect(), 2, 2),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 4)],
                        [Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 1),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 4)],
                        [Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 1),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 4)]]

    # board = [[Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 1),
    #             Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 3),
    #             Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 4)],
    #            [Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 1),
    #             Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 3),
    #             Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 4)],
    #            [Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 1),
    #             Pawn(neutralPawn, 0, neutralPawn.get_rect(), 2, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 3),
    #             Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 4)],
    #            [Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 1),
    #             Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 3),
    #             Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 4)],
    #            [Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 1),
    #             Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 3),
    #             Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 4)]]

    def drawBoard(self):
        screen.blit(background, background.get_rect())
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j].rect.topleft = ((165 * (j + 0.15)), (155 * (i + 0.15)))
                if self.board[i][j].image != neutralPawn:
                    screen.blit(self.board[i][j].image, self.board[i][j].rect)
        pygame.display.update()

    def getPawn(self, event):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].image is not None and (
                        self.board[i][j].rect.collidepoint(event.pos[0], event.pos[1])) is True:
                    return i, j
        return False

    def getPawnAt(self, x, y):
        return self.board[x][y]

    def getNeighborList(self, pawn):
        neighborList = []
        x = pawn.x
        y = pawn.y
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x + y) % 2 == 0:
                    if 0 <= x + i <= len(self.board) - 1 and 0 <= y + j <= len(self.board) - 1 and (
                            i != 0 or j != 0):
                        neighborList.append(self.board[x + i][y + j])
                else:
                    if 0 <= x + i <= len(self.board) - 1 and 0 <= y + j <= len(self.board) - 1 and (
                            (x + i == x) != (y + j == y)):
                        neighborList.append(self.board[x + i][y + j])
        return neighborList

    def possible(self, pawn1, pawn2):
        if pawn2 in self.getNeighborList(pawn1) and pawn2.player == 0:
            return True
        return False

    def possibleCapture(self, pawn1, pawn2):
        if ((pawn1.x + pawn2.x) % 2 == 0) and ((pawn1.y + pawn2.y) % 2 == 0):
            midPawn = self.board[math.floor((pawn1.x + pawn2.x) / 2)][math.floor((pawn1.y + pawn2.y) / 2)]
            midPawn.x = math.floor((pawn1.x + pawn2.x) / 2)
            midPawn.y = math.floor((pawn1.y + pawn2.y) / 2)
            if pawn2.player == 0 and midPawn.player != pawn1.player and midPawn.player != 0 and midPawn in self.getNeighborList(
                    pawn1) and midPawn in self.getNeighborList(pawn2) and (
                    (pawn1.x < midPawn.x < pawn2.x or pawn1.x > midPawn.x > pawn2.x) or (
                    pawn1.y < midPawn.y < pawn2.y or pawn1.y > midPawn.y > pawn2.y)):
                return True
        return False

    def otherCapture(self, player):
        captureList = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].player == player:
                    for k in self.getNeighborList(self.board[i][j]):
                        for l in self.getNeighborList(k):
                            if self.possibleCapture(self.board[i][j], l) and (
                                    self.board[i][j], l) not in captureList:
                                captureList.append((self.board[i][j], l))
        return captureList

    def remove(self, pawn1):
        pawn1.player = 0
        pawn1.image = neutralPawn
        print("Tu n'as pas capturé")

    def move(self, pawn1, pawn2):
        pawn2.player = pawn1.player
        pawn2.image = pawn1.image
        pawn1.player = 0
        pawn1.image = neutralPawn

    def capture(self, pawn1, pawn2):
        self.board[math.floor((pawn1.x + pawn2.x) / 2)][math.floor((pawn1.y + pawn2.y) / 2)].player = 0
        self.board[math.floor((pawn1.x + pawn2.x) / 2)][math.floor((pawn1.y + pawn2.y) / 2)].image = neutralPawn
        pawn2.player = pawn1.player
        pawn2.image = pawn1.image
        pawn1.player = 0
        pawn1.image = neutralPawn

    def play(self, pawn1, pawn2, player, players):
        # global player
        if len(self.otherCapture(player)) >= 1 and self.possible(pawn1, pawn2):
            self.remove(pawn1)
            player = next(players)
            return player
        elif self.possible(pawn1, pawn2):
            self.move(pawn1, pawn2)
            player = next(players)
            return player
        elif self.possibleCapture(pawn1, pawn2):
            self.capture(pawn1, pawn2)
            if len(self.otherCapture(player)) >= 1 and (pawn1, pawn2) not in self.otherCapture(player):
                return player
            else:
                player = next(players)
                return player
        else:
            return player

    def victory(self):
        cnt1 = 0
        cnt2 = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                for k in range(len(self.board)):
                    for l in range(len(self.board[k])):
                        if self.board[i][j].player == 1 and (
                                self.possible(self.board[i][j], self.board[k][l]) or self.possibleCapture(
                            self.board[
                                i][
                                j],
                            self.board[
                                k][
                                l])):
                            cnt1 += 1
                        elif self.board[i][j].player == 2 and (
                                self.possible(self.board[i][j], self.board[k][l]) or self.possibleCapture(
                            self.board[
                                i][
                                j],
                            self.board[
                                k][
                                l])):
                            cnt2 += 1
        if cnt1 == 0:
            return True, 2
        elif cnt2 == 0:
            return True, 1
        return False

    def resetBoard(self):
        self.board = [[Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 1),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 3),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 0, 4)],
                        [Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 1),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 2), Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 3),
                         Pawn(blackPawn, 1, blackPawn.get_rect(), 1, 4)],
                        [Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 0), Pawn(blackPawn, 1, blackPawn.get_rect(), 2, 1),
                         Pawn(neutralPawn, 0, neutralPawn.get_rect(), 2, 2),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 2, 4)],
                        [Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 1),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 3, 4)],
                        [Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 0), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 1),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 2), Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 3),
                         Pawn(whitePawn, 2, whitePawn.get_rect(), 4, 4)]]


def game():
    run = True
    firstPawn, secondPawn = None, None
    players = cycle([2, 1])
    player = next(players)
    board = Board()
    while run:
        board.drawBoard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                if firstPawn is None:
                    if board.getPawn(event) is not False:
                        firstPawn = board.getPawnAt(board.getPawn(event)[0], board.getPawn(event)[1])
                        firstPawn.x = board.getPawn(event)[0]
                        firstPawn.y = board.getPawn(event)[1]
                        print("firstPawn")
                elif secondPawn is None:
                    if board.getPawn(event) is not False:
                        secondPawn = board.getPawnAt(board.getPawn(event)[0], board.getPawn(event)[1])
                        secondPawn.x = board.getPawn(event)[0]
                        secondPawn.y = board.getPawn(event)[1]
                        print("secondPawn")
                if firstPawn is not None and secondPawn is not None:
                    if firstPawn.player == player and secondPawn.player == 0:
                        player = board.play(firstPawn, secondPawn, player, players)
                        if player == 1:
                            print("\nJoueur noir\n")
                        else:
                            print("\nJoueur blanc\n")
                    firstPawn, secondPawn = None, None
                if board.victory():
                    if board.victory()[1] == 1:
                        print("Le joueur noir a gagné")
                    else:
                        print("Le joueur blanc a gagné")
                    board.resetBoard()
                    if player == 1:
                        player = next(players)

    pygame.quit()
    quit()


game()
