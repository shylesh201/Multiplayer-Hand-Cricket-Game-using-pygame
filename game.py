class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]        #client,oppenent
        self.wins = [0, 0]
        self.ties = 0
        self.score = [0, 0]   #score of 1st player, 2nd player
        self.done_bat = [0, 0]     #1-batting over, 0-not done

    def get_player_move(self, p):
        return self.moves[p]

    def get_player_score(self, p):
       return self.score[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def batsman(self, batsman1, bowler1, score):
        print("Playe 1 done:", self.done_bat[0], "Player 2 done:", self.done_bat[1])
        p1 = self.moves[batsman1]
        p2 = self.moves[bowler1]
        print("p1=", p1)
        print("p2=", p2)
        if p1 == p2:
            self.done_bat[batsman1] = 1
            print("done_bat=", batsman1)
        else:
            score = score + int(p1)
            print("score[batsman1]", score)
        return score

    def winner(self):
        s1 = self.score[0]
        s2 = self.score[1]
        print(s1)
        print(s2)
        if s1 > s2:
            winner = 0
        elif s1 < s2:
            winner = 1
        else:
            winner = -1
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False