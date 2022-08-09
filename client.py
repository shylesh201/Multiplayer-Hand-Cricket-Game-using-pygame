import pygame
pygame.init()
from network import Network
import pickle

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("HAND CRICKET")
background_image = pygame.image.load("hc.jpeg").convert()

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(wind, game, p):
    global text1, text2
    wind.fill((0,50,0))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for Opponent", 1, (255, 255, 255), True)
        wind.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Player", 1, (255, 255, 255))
        wind.blit(text, (80, 90))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Opponent", 1, (255, 255, 255))
        wind.blit(text, (380, 90))

        if p == 1 and game.done_bat[0] == 1:
            text1 = font.render("Batsman", 1, (255, 255, 255))
            text2 = font.render("Bowler", 1, (255, 255, 255))
        elif p == 0 and game.done_bat[0] == 1:
            text1 = font.render("Bowler", 1, (255, 255, 255))
            text2 = font.render("Batsman", 1, (255, 255, 255))
        elif p == 1:
            text1 = font.render("Bowler", 1, (255, 255, 255))
            text2 = font.render("Batsman", 1, (255, 255, 255))
        elif p == 0:
            text1 = font.render("Batsman", 1, (255, 255, 255))
            text2 = font.render("Bowler", 1, (255, 255, 255))

        wind.blit(text1, (80, 160))
        wind.blit(text2, (380, 160))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        score1 = game.get_player_score(0)
        score2 = game.get_player_score(1)

        if p == 1:
            wind.blit(text2, (100, 320))
            wind.blit(text1, (410, 320))
            t_score1 = font.render(str(score2), 1, (255, 75, 75))
            t_score2 = font.render(str(score1), 1, (255, 75, 75))
        else:
            wind.blit(text1, (100, 320))
            wind.blit(text2, (410, 320))
            t_score1 = font.render(str(score1), 1, (255, 75, 75))
            t_score2 = font.render(str(score2), 1, (255, 75, 75))

        wind.blit(t_score1, (130, 250))
        wind.blit(t_score2, (430, 250))

        if game.done_bat[0] ==1 and game.done_bat[1] ==1:
            pass
        elif game.done_bat[0] == 1 and game.get_player_score(1) == 0 and p == 1:
            text0 = font.render("OPPONENT IS OUT", 1, (255, 75, 75))
            wind.blit(text0, (75, 10))
        elif game.done_bat[0] == 1 and game.get_player_score(1) == 0 and p == 0:
            text0 = font.render("YOU ARE OUT", 1, (255, 75, 75))
            wind.blit(text0, (120, 10))

        for btn in btns:
            btn.draw(wind)

    pygame.display.update()

# creating run buttons

btns = [Button("1", 75, 420, (255, 255, 255)), Button("2", 275, 420, (255, 255, 255)),
        Button("3", 475, 420, (255, 255, 255)), Button("4", 75, 545, (255, 255, 255)),
        Button("5", 275, 545, (255, 255, 255)), Button("6", 475, 545, (255, 255, 255)), ]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            #print("game id =",game.id)
            #print("game score =",game.score)
            # print("got the game ")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            print("game.bothWent() = ",game.bothWent())
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("score")
            except:
                run = False
                print("Couldn't get game for score")
                break

        #print("game.done_bat[0] = ", game.done_bat[0], "and game.done_bat[0] =", game.done_bat[1])

        if game.done_bat[0] and game.done_bat[1]:
            print("result")
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 60)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("YOW WON", 1, (255, 75, 75))
            elif game.winner() == -1:
                text = font.render("TIE GAME", 1, (255, 75, 75))
            else:
                text = font.render("YOU LOST", 1, (255, 75, 75))

            win.blit(text, (150, 10))
            pygame.display.update()
            pygame.time.delay(3000)

        #recieve events from client side
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                                print(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
                                print(btn.text)
        # print("redrawWindow() player ",player)
        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(5)
        win.fill((180,255,100))
        font = pygame.font.SysFont("ariel", 80)
        text = font.render("CLICK TO PLAY", 1, (0, 50, 0))
        win.blit(text, (120, 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(background_image, [0, 150])

        pygame.display.update()

    main()


while True:
    menu_screen()