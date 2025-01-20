import random
import copy
#(['x','x','o'], ['x', '', ''], ['o', 'x', ''])

def rotate_right(tup):
    rotated = ((tup[2][0], tup[1][0], tup[0][0]),
               (tup[2][1], tup[1][1], tup[0][1]),
               (tup[2][2], tup[1][2], tup[0][2]))

    return rotated

def flip(tup):
    flipped = ((tup[0][2], tup[0][1], tup[0][0]),
               (tup[1][2], tup[1][1], tup[1][0]),
               (tup[2][2], tup[2][1], tup[2][0]))

    return flipped

def print_tup(tup, arr = False):
    if arr:
        for x in tup:
            print(x[0])
            print(x[1])
            print(x[2])
            print('')
    else:
            print(tup[0])
            print(tup[1])
            print(tup[2])
            print('')

def all_comb(tup):
    out = []

    flipped = flip(tup)

    out.append(tup)
    for i in range(3):
        tup = rotate_right(tup)
        out.append(tup)

    out.append(flipped)
    for i in range(3):
        flipped = rotate_right(flipped)
        out.append(flipped)

    return out

def to_tuple(board):
    return tuple(tuple(row) for row in board)
# test = ((1, 2, 3), (4, 5, 6), (7, 8, 9))

# x = all_comb(test)
# print_tup(x, True)


class TicTacToe:
    def __init__(self):
        # Initialize a 3x3 board with empty spaces
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.moves = set(range(1,10))


    def print_board(self):
        # Display the current state of the board
        print('-' * 5)
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

        print(self.moves)
        print()

    def move(self, x):
        if x.isdigit():
            number = int(x)
            if 1 <= number <= 9:
                number = number - 1
                row = number//3
                col = number%3
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.player
                    self.player = 'O' if self.player == 'X' else 'X'
                    self.moves.remove(number + 1)
                    return
            
        print("Invalid Input")

    def move_random(self):
        x = random.choice(list(self.moves))
        x = str(x)
        self.move(x)

    def check(self):
        winner = None
        for i in range(3):
            if self.board[i][0] == 'O' and self.board[i][1] == 'O' and self.board[i][2] == 'O':
                return 'O'
            if self.board[i][0] == 'X' and self.board[i][1] == 'X' and self.board[i][2] == 'X':
                return 'X'
            if self.board[0][i] == 'O' and self.board[1][i] == 'O' and self.board[2][i] == 'O':
                return 'O'
            if self.board[0][i] == 'X' and self.board[1][i] == 'X' and self.board[2][i] == 'X':
                return 'X'

        if self.board[0][0] == 'O' and self.board[1][1] == 'O' and self.board[2][2] == 'O':
            return 'O'
        if self.board[0][0] == 'X' and self.board[1][1] == 'X' and self.board[2][2] == 'X':
            return 'X'
        if self.board[0][2] == 'O' and self.board[1][1] == 'O' and self.board[2][0] == 'O':
            return 'O'
        if self.board[0][2] == 'X' and self.board[1][1] == 'X' and self.board[2][0] == 'X':
            return 'X'

        if len(self.moves) == 0:
            return "No one"

        return None
        
#game loop
# game = TicTacToe()
# game.print_board()
# while True:
#     player_in = input()
#     if player_in == '':
#         print("game ended")
#         break
#     else:
#         game.move(x = player_in)
    
#     game.print_board()

#     winner = game.check()
#     if winner is not None:
#         print(winner + " wins")
#         break

#some stats BEFORE
MAP = {}
for i in range(10000):
    game = TicTacToe()
    while True:
        game.move_random()
        winner = game.check()
        if winner is not None:
            if winner in MAP:
                MAP[winner] += 1
            else:
                MAP[winner] = 1

            break

print(MAP)
print("WINRATE = ",MAP['O']/sum(MAP.values()))



#TEMPORAL DIFFERENCE LEARNING
#RANDOM OPPONENT, AGENT GOES SECOND

def get_move(VTABLE, epsilon, board, moves):
    board = copy.deepcopy(board)
    scores = {}

    for number in moves:
        number = number - 1
        found = False
        row = number//3
        col = number%3
        board[row][col] = 'O'

        tup = to_tuple(board)
        all = all_comb(tup)

        for comb in all:
            if comb in VTABLE:
                scores[number + 1] = VTABLE[comb]
                found = True
                break

        if not found:
            VTABLE[comb] = 0.5
            scores[number + 1] = 0.5


        board[row][col] = ' '


    maxP = 0
    possible = []
    for k in scores:
        if scores[k]>maxP:
            maxP = scores[k]
            possible = []
            possible.append(k)
        elif scores[k] == maxP:
            possible.append(k)

    best = random.choice(possible)
    rand = random.choice(list(scores.keys()))
    choice = random.choices([best, rand], [1 - epsilon, epsilon], k=1)[0]
    #print(scores, possible, maxP, best, rand, choice)

    return choice, choice == best




    
VTABLE = {}
epsilon = 0.5

for i in range(100000):
    if i % 10000 == 0:
        epsilon -= 0.05

    game = TicTacToe()
    states = []
    best_arr = []
    while True:
        game.move_random()

        winner = game.check()
        if winner == 'X':
            VTABLE[game_state] = 0
            game_state = to_tuple(game.board)
            states.append(game_state)
            break
        if winner == 'No one':
            VTABLE[game_state] = 0.25
            game_state = to_tuple(game.board)
            states.append(game_state)
            break

        ai_move, best = get_move(VTABLE, epsilon, game.board, game.moves)
        game.move(str(ai_move))
        game_state = to_tuple(game.board)
        states.append(game_state)
        best_arr.append(best)

        winner = game.check()
        if winner == 'O':
            VTABLE[game_state] = 1
            break


    for i in range(0, len(states)):
        found = False
        tup = states[i]
        all = all_comb(tup)

        for comb in all:
            if comb in VTABLE:
                states[i] = comb
                found = True
                break

        if not found:
            VTABLE[all[0]] = 0.5



    for i in range(len(states) - 2, -1, -1):
        before, after = states[i], states[i+1]

        if best_arr[i]:
            VTABLE[before] = VTABLE[before] + 0.5*(VTABLE[after] - VTABLE[before])

    
print()
#print(VTABLE.values())
        





#some stats
MAP = {}
for i in range(10000):
    game = TicTacToe()
    while True:
        game.move_random()

        winner = game.check()
        if winner is not None:
            if winner in MAP:
                MAP[winner] += 1
            else:
                MAP[winner] = 1
            break

        ai_move, best = get_move(VTABLE, 0, game.board, game.moves)
        game.move(str(ai_move))
        winner = game.check()
        if winner is not None:
            if winner in MAP:
                MAP[winner] += 1
            else:
                MAP[winner] = 1
            break


print(MAP)
print("WINRATE = ",MAP['O']/sum(MAP.values()))
print("NOT LOSE RATE = ",(MAP['O'] + MAP['No one'])/sum(MAP.values()))


        
