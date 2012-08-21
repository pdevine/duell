import random

STATE_CREATED = 'created'
STATE_RUNNING = 'running'
STATE_OVER = 'game over'

DIRECTION_FORWARD = 'forward'
DIRECTION_BACKWARD = 'backward'

MAX_SCORE = 5

class InvalidMoveError(Exception):
    pass

class GameStateError(Exception):
    pass

class Board:
    def __init__(self, max_score=MAX_SCORE):
        self.max_score = max_score
        self.state = STATE_CREATED

        self.board = [None] * 23
        self.cards = [Card(x) for x in [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5 + [5] * 5]
        self.discards = []
        self.shuffle()

        self.player1 = Player()
        self.player2 = Player()

        self.deal()

        self.turn = random.choice([self.player1, self.player2])
        self.board[0] = self.player1
        self.board[-1] = self.player2

    def deal(self):
        for cnt in range(5):
            for player in [self.player1, self.player2]:
                self.draw(player)

    def shuffle(self):
        random.shuffle(self.cards)

    def move(self, player, direction, card):
        if self.state == STATE_OVER:
            raise GameStateError()

        if self.turn != player:
            raise InvalidMoveError()

        player1_pos = self.board.index(self.player1)
        player2_pos = self.board.index(self.player2)

        amount = card.val

        if player == self.player1:
            if direction == DIRECTION_FORWARD:
                if player1_pos + amount < len(self.board)/2:
                    self.board[player1_pos] = None
                    self.board[player1_pos + amount] = self.player1
                elif player1_pos + amount == player2_pos:
                    self.score(self.player1)
                else:
                    raise InvalidMoveError()
            else:
                if player1_pos - amount >= 0:
                    self.board[player1_pos] = None
                    self.board[player1_pos - amount] = self.player1
                else:
                    raise InvalidMoveError()
        else:
            if direction == DIRECTION_FORWARD:
                if player2_pos - amount > len(self.board)/2:
                    self.board[player2_pos] = None
                    self.board[player2_pos - amount] = self.player2
                elif player2_pos - amount == player1_pos:
                    self.score(self.player2)
                else:
                    raise InvalidMoveError()
            else:
                if player2_pos + amount < len(self.board):
                    self.board[player2_pos] = None
                    self.board[player2_pos + amount] = self.player2
                else:
                    raise InvalidMoveError()

        player.cards.remove(card)
        self.discards.append(card)
        player.draw()
        self.change_turn()

    def change_turn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def top_card(self):
        if self.discards:
            return self.discards[-1]
        return None

    def score(self, player):
        if player == self.player1:
            self.player1.score += 1
            if self.player1.score >= self.max_score:
                self.state = STATE_OVER
        else:
            self.player2.score += 1
            if self.player2.score >= self.max_score:
                self.state = STATE_OVER

        # reset board positions
        self.board = [None] * 23
        self.board[0] = self.player1
        self.board[-1] = self.player2

    def check_furthest(self):
        if self.board.index(self.player1) > (len(self.board) - self.board.index(self.player2)):
            # player1 wins
            self.turn = self.player2
        elif self.board.index(self.player1) < (len(self.board) - self.board.index(self.player2)):
            # player2 wins
            self.turn = self.player1
        else:
            self.change_turn()

    def draw(self, player, amount=1):
        for count in range(amount):
            player.cards.append(self.cards.pop())

class Card:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "Card (%s)" % self.val

class Player:
    def __init__(self):
        self.cards = []
        self.score = 0

