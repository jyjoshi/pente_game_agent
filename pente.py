import copy
import time


def read():
    global color, black_captures, board, white_count, black_count
    global remaining_time, captures, white_captures

    file = open("pente.txt", "r")
    color = file.readline().replace("\n", "")
    remaining_time = float(file.readline())
    captures = file.readline().split(",")
    white_captures, black_captures = [int(i) for i in captures]
    board = [["." for i in range(19)] for j in range(19)]

    white_count = 0
    black_count = 0

    for row in range(19):
        column = 0
        for i in file.readline():
            if i == "w":
                white_count += 1
                board[row][column] = "w"
            elif i == "b":
                black_count += 1
                board[row][column] = "b"
            column += 1

    # print("Updated board")
    # for line in board:
    #     print(line)

    move = [0, 0]  # In the format where first index is the x_coordinate and the second coordinate is the y coordinate

    # print("Previous Captures", white_captures, black_captures)
    # capture_count = update_board_for_captures(board, move)
    # if board[move[1]][move[0]] == "w":
    #     white_captures += capture_count
    # else:
    #     black_captures += capture_count
    # print("Updated Captures", white_captures, black_captures)


def output(move):
    alphabets = "ABCDEFGHJKLMNOPQRST"
    y_coordinate = str(19 - move[0])
    x_coordinate = alphabets[move[1]]
    print(y_coordinate + x_coordinate)


def check_win_by_sequence(board):
    # Check for horizontal wins
    for row in board:
        for i in range(len(row) - 4):
            if row[i:i + 5] == ['b'] * 5 or row[i:i + 5] == ['w'] * 5:
                return True

    # Check for vertical wins
    for j in range(len(board[0])):
        for i in range(len(board) - 4):
            if [board[x][j] for x in range(i, i + 5)] == ['b'] * 5 or [board[x][j] for x in range(i, i + 5)] == [
                'w'] * 5:
                return True

    # Check for diagonal wins
    for i in range(len(board) - 4):
        for j in range(len(board[0]) - 4):
            if [board[i + x][j + x] for x in range(5)] == ['b'] * 5 or [board[i + x][j + x] for x in range(5)] == [
                'w'] * 5:
                return True
            if [board[i + x][j + 4 - x] for x in range(5)] == ['b'] * 5 or [board[i + x][j + 4 - x] for x in
                                                                            range(5)] == ['w'] * 5:
                return True

    return False


# Gives win by sequence the move needs to be provided as [x_coordinate, y_coordinate]
def check_win_sequence(board, move):
    y, x = move
    color = board[x][y]
    # print(board[x][y])
    if color == ".":
        return False

    # print("HERE")
    # print(board)
    # Check for horizontal sequence of 5
    for i in range(y - 4, y + 1):
        if i < 0 or i + 5 > 19:
            continue

        if board[x][i:i + 5] == [color] * 5:
            print("Horizontal Triggered")
            return True

    # Check for vertical sequence of 5
    for j in range(x - 4, x + 1):
        if j < 0 or j + 5 > 19:
            continue
        if [board[j + i][y] for i in range(5)] == [color] * 5:
            print("Vertical Triggered")
            return True

    # Check for diagonal (top-left to bottom-right) sequence of 5
    for i, j in zip(range(x - 4, x + 1), range(y - 4, y + 1)):
        if i < 0 or j < 0 or i + 5 > 19 or j + 5 > 19:
            continue
        if [board[i + k][j + k] for k in range(5)] == [color] * 5:
            print("TL - BR Triggered")
            return True

    # Check for diagonal (top-right to bottom-left) sequence of 5
    for i, j in zip(range(x - 4, x + 1), range(y + 4, y - 1, -1)):
        if i < 0 or j < 0 or i + 5 > 19 or j - 4 < 0 or j > 18:
            continue

        if [board[i + k][j - k] for k in range(5)] == [color] * 5:
            print("TR - BL Triggered")
            return True

    return False


def update_board_for_captures(board, move):
    x, y = move
    directions = [
        [[0, 1], [0, 2], [0, 3]],
        [[1, 1], [2, 2], [3, 3]],
        [[1, 0], [2, 0], [3, 0]],
        [[1, -1], [2, -2], [3, -3]],
        [[0, -1], [0, -2], [0, -3]],
        [[-1, -1], [-2, -2], [-3, -3]],
        [[-1, 0], [-2, 0], [-3, 0]],
        [[-1, 1], [-2, 2], [-3, 3]]
    ]

    if not isValidMove([y + 3, x]):
        if not isValidMove([y, x + 3]):
            possible_directions = [4, 5, 6]
        elif not isValidMove([y, x - 3]):
            possible_directions = [0, 6, 7]
        else:
            possible_directions = [0, 4, 5, 6, 7]
    elif not isValidMove([y - 3, x]):
        if not isValidMove([y, x + 3]):
            possible_directions = [2, 3, 4]
        elif not isValidMove([y, x - 3]):
            possible_directions = [0, 1, 2]
        else:
            possible_directions = [0, 1, 2, 3, 4]
    elif not isValidMove([y, x + 3]):
        possible_directions = [2, 3, 4, 5, 6]
    elif not isValidMove([y, x - 3]):
        possible_directions = [0, 1, 2, 6, 7]
    else:
        possible_directions = [0, 1, 2, 3, 4, 5, 6, 7]

    if board[y][x] == "b":
        piece = "w"
    else:
        piece = "b"
    count = 0
    capture_count = 0
    # print(possible_directions)
    for i in possible_directions:
        y_val = y + directions[i][0][0]
        x_val = x + directions[i][0][1]
        if board[y + directions[i][0][0]][x + directions[i][0][1]] == piece \
                and board[y + directions[i][1][0]][x + directions[i][1][1]] == piece \
                and board[y + directions[i][2][0]][x + directions[i][2][1]] == board[y][x]:
            # print("Capture possible at ", directions[i])
            capture_count += 2
            board[y + directions[i][0][0]][x + directions[i][0][1]] = "."
            board[y + directions[i][1][0]][x + directions[i][1][1]] = "."
        # print("Capture count ", capture_count)
        # print("Updated board")
        # for line in board:
        #     print(line)

        # print(directions[i])
        # print(directions[i][0])
        # print(directions[i][1])
        # print(directions[i][2])
        count += 1
    return capture_count


def check_draw(board):
    blank_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ".":
                blank_count += 1
    if blank_count == 0:
        return True
    return False


def isValidMove(move):
    return 0 <= move[0] < 19 and 0 <= move[1] < 19


class Node:
    def __init__(self,
                 board,
                 move,
                 white_captures,
                 black_captures,
                 color,
                 remaining_time,
                 white_count,
                 black_count):
        self.color = color
        self.white_captures = white_captures
        self.black_captures = black_captures
        self.move = move
        self.remaining_time = remaining_time
        # provide move -1, -1 for the initial input
        if move == [-1, -1]:
            self.white_count = white_count
            self.black_count = black_count
            if color == "BLACK":
                self.piece = "b"
                self.opp_piece = "w"
            else:
                self.piece = "w"
                self.opp_piece = "b"
            # self.board = [[board[j][i] for i in range(19)] for j in range(19)]
            self.board = copy.deepcopy(board)
        else:
            # self.board = [[board[j][i] for i in range(19)] for j in range(19)]
            self.board = copy.deepcopy(board)
            if color == 'WHITE':
                self.board[move[0]][move[1]] = 'b'
                self.piece = 'w'
                self.opp_piece = 'b'
                self.white_count = white_count
                self.black_count = black_count + 1
            else:
                self.board[move[0]][move[1]] = 'w'
                self.piece = 'b'
                self.opp_piece = 'w'
                self.white_count = white_count + 1
                self.black_count = black_count
            # print("Move is ", move)
            # for line in self.board:
            #     print(line)
        #     self.board = [
        #         ["w" if color == "BLACK" else "b" if ((i == move[0]) and (j == move[1])) else board[j][i] for i in
        #          range(19)] for j in range(19)]
        #     if self.board[move[1]][move[0]] == "w":
        #         self.piece = "b"
        #         self.opp_piece = "w"
        #         self.white_count = white_count + 1
        #         self.black_count = black_count
        #     else:
        #         self.piece = "w"
        #         self.opp_piece = "b"
        #         self.black_count = black_count + 1
        #         self.white_count = white_count


def sliding_window_2d(grid, window_size, pattern):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Horizontal window
            if j <= len(grid[0]) - window_size:
                window = grid[i][j:j + window_size]
                if all([a == b for a, b in zip(pattern, window)]):
                    return True
            # Vertical window
            if i <= len(grid) - window_size:
                window = [row[j] for row in grid[i:i + window_size]]
                if all([a == b for a, b in zip(pattern, window)]):
                    return True
            # Diagonal window (top-left to bottom-right)
            if i <= len(grid) - window_size and j <= len(grid[0]) - window_size:
                window = [grid[i + k][j + k] for k in range(window_size)]
                if all([a == b for a, b in zip(pattern, window)]):
                    return True
            # Diagonal window (bottom-left to top-right)
            if i >= window_size - 1 and j <= len(grid[0]) - window_size:
                window = [grid[i - k][j + k] for k in range(window_size)]
                if all([a == b for a, b in zip(pattern, window)]):
                    return True
    return False


def sliding_window(grid, window_size, pattern):
    matches = 0
    half_window = window_size // 2

    # iterate over all positions in the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # check horizontal pattern match
            if j <= len(grid[0]) - window_size:
                window = grid[i][j:j + window_size]
                if window == pattern:
                    matches += 1

            # check vertical pattern match
            if i <= len(grid) - window_size:
                window = [grid[k][j] for k in range(i, i + window_size)]
                if window == pattern:
                    matches += 1

            # check diagonal pattern match (top-left to bottom-right)
            if i <= len(grid) - window_size and j <= len(grid[0]) - window_size:
                window = [grid[i + k][j + k] for k in range(window_size)]
                if window == pattern:
                    matches += 1

            # check diagonal pattern match (top-right to bottom-left)
            if i <= len(grid) - window_size and j >= half_window:
                window = [grid[i + k][j - k] for k in range(window_size)]
                if window == pattern:
                    matches += 1

    return matches


def alpha_beta(node, depth, alpha, beta, maximizing_player):
    # print("Move that resulted in node :", node.move)
    # for line in node.board:
    #     print(line)
    if node.color == "BLACK":
        color_param = "WHITE"
    else:
        color_param = "BLACK"
    if depth == 0:
        # print("Depth is zero")
        # for line in node.board:
        #     print(line)
        # if len(node.board) != 19:
        #     print("Problem")
        return evaluate(node.board), node.move

    if maximizing_player:
        value = -float("inf")
        moves = spiral(node.board)
        best_move = moves[0]
        print("Initial best move", best_move)
        for move in moves:
            print(moves[:20])
            if move == [12, 10]:
                print("Move Reached")
            new_node = Node(node.board,
                            move,
                            node.white_captures,
                            node.black_captures,
                            color_param,
                            node.remaining_time,
                            node.white_count,
                            node.black_count)

            capture_count = update_board_for_captures(new_node.board, move)
            if node.piece == "b":
                new_node.white_count -= capture_count
                new_node.black_captures += capture_count
            else:
                new_node.black_count -= capture_count
                new_node.white_captures += capture_count

            # Check for terminal cases at this level
            if check_win_sequence(new_node.board, move):
                print("Here")
                return float("inf"), move
            elif (node.piece == "b" and new_node.black_captures >= 10) or \
                    (node.piece == "w" and new_node.white_captures >= 10):
                print("Maybe Here")
                # for line in node.board:
                #     print(line)
                return float("inf"), move
            elif check_draw(new_node.board):
                return 0, move
            local_val, local_move = alpha_beta(new_node, depth - 1, alpha, beta, False)
            if local_val > value:
                best_move = local_move
                value = local_val
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = float("inf")
        moves = spiral(node.board)
        best_move = moves[0]
        for move in moves:
            new_node = Node(node.board,
                            move,
                            node.white_captures,
                            node.black_captures,
                            color_param,
                            node.remaining_time,
                            node.white_count,
                            node.black_count)
            capture_count = update_board_for_captures(new_node.board, move)
            if node.piece == "b":
                new_node.white_count -= capture_count
                new_node.black_captures += capture_count
            else:
                new_node.black_count -= capture_count
                new_node.white_captures += capture_count
            # print(new_node.board)
            if check_win_sequence(new_node.board, move):
                # print("Here")
                return -float("inf"), move
            elif (node.piece == "b" and new_node.black_captures >= 10) or (
                    node.piece == "w" and new_node.white_captures >= 10):
                print("Maybe Here?")
                return -float("inf"), move
            elif check_draw(new_node.board):
                return 0
            local_val, local_move = alpha_beta(new_node, depth - 1, alpha, beta, True)
            # print("local val", local_val)
            # print("Val", value)
            if local_val < value:
                # print("Inside val update")
                value = local_val
                best_move = local_move
                # print("Value updated", value)
            beta = min(beta, value)
            if alpha >= beta:
                print("Break in min occured. Node : ", node.move)
                break
        return value, best_move

# res_b = []
# res_w = []
# for i in range(len(b_patterns)):
#     x = b_patterns[i].split()
#     y = w_patterns[i].split()
#     res_b.append(x)
#     res_w.append(y)


# print(res_b)
# print(res_w)
# b_list = []
# w_list = []
# for i in range(len(b_block_patterns)):
#     b = list(b_block_patterns[i])
#     w = list(w_block_patterns[i])
#     b_list.append(b)
#     w_list.append(w)
# print(b_list)
# print(w_list)


b_patterns = [['.', 'b', 'b', 'b', '.'], ['b', 'b', 'b', '.'], ['.', 'b', 'b', 'b'], ['.', 'b', '.', 'b', 'b'],
              ['.', 'b', 'b', '.', 'b'], ['.', 'b', 'b', 'b', 'b', '.'], ['.', 'b', 'b', 'b', 'b'],
              ['b', 'b', 'b', 'b', '.']]
w_patterns = [['.', 'w', 'w', 'w', '.'], ['w', 'w', 'w', '.'], ['.', 'w', 'w', 'w'], ['.', 'w', '.', 'w', 'w'],
              ['.', 'w', 'w', '.', 'w'], ['.', 'w', 'w', 'w', 'w', '.'], ['.', 'w', 'w', 'w', 'w'],
              ['w', 'w', 'w', 'w', '.']]
weights = [600, 300, 300, 450, 450, 10000, 9000, 9000]
b_capture_patterns = [['b', 'w', 'w', '.'], ['.', 'w', 'w', 'b'], ['b', 'w', '.', '.'], ['.', '.', 'w', 'b'],
                      ['.', 'w', 'w', '.']]
w_capture_patterns = [['w', 'b', 'b', '.'], ['.', 'b', 'b', 'w'], ['w', 'b', '.', '.'], ['.', '.', 'b', 'w'],
                      ['.', 'b', 'b', '.']]
capture_weights = [10, 10, 3, 3, 6]

b_block_patterns = [['b', 'w', 'w', 'w', 'w', 'b'], ['b', 'w', 'w', 'w', 'b'], ['b', 'w', 'w', 'b']]
w_block_patterns = [['w', 'b', 'b', 'b', 'b', 'w'], ['w', 'b', 'b', 'b', 'w'], ['w', 'b', 'b', 'w']]
block_weights = [10000, 600, 15]


def evaluate(xboard):
    value = 0
    multiplier = 1
    if color == "WHITE":
        multiplier = -1
    for i in range(len(b_patterns)):
        b = b_patterns[i]
        w = w_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * weights[i]

    for i in range(len(b_capture_patterns)):
        b = b_capture_patterns[i]
        w = w_capture_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * capture_weights[i]

    for i in range(len(b_block_patterns)):
        b = b_block_patterns[i]
        w = w_block_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * block_weights[i]
    return multiplier * value


# x = spiral_traversal(board)


# Returns a list of indices in the format [x, y] where x is the x coordinate and y is the y coordinate
def spiral(board):
    center = len(board) // 2
    X = Y = len(board)
    x = y = 0
    dx = 0
    dy = -1
    indices = []
    for i in range(max(X, Y) ** 2):
        if (-X / 2 < x <= X / 2) and (-Y / 2 < y <= Y / 2):
            # DO STUFF...
            if board[x + center][y + center] == ".":
                indices.append([x + center, y + center])
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy
    return indices


# board = [["." for i in range(5)] for j in range(5)]
# board[0][0] = "b"
# board[3][4] = "w"


read()

start = time.time()

move = [-1, -1]
node = Node(board,
            move,
            white_captures,
            black_captures,
            color,
            remaining_time,
            white_count,
            black_count)

start = time.time()
print(node.color)
# if color == "BLACK" and white_count == 1 and black_captures == 0:
#     # First move for black
#     print("K8")
# elif color == "WHITE" and black_count == 0 and white_captures == 0:
#     # First move for white
#     print("K10")
# elif color == "WHITE" and black_count == 1 and white_captures == 0 and white_count == 1:
#     # Second move for white
#     print("N10")
# else:
#     x = alpha_beta(node, 2, -float("inf"), float("inf"), True)
#     output(x[1])


x = alpha_beta(node, 2, -float("inf"), float("inf"), True)
output(x[1])
print(x)
end = time.time()
print(end - start)

# full_b_patterns = b_patterns + b_capture_patterns + b_block_patterns
# full_b_weights = weights + capture_weights + block_weights
# for i in range(len(full_b_patterns)):
#     print(full_b_patterns[i], full_b_weights[i])


#
# end = time.time()
# print(end - start)
# ". b b b b .".split()
# start = time.time()
# pattern = ". b b b b .".split()
# print(pattern)
# print(sliding_window(board, len(pattern), pattern))
# end = time.time()
# print(end - start)
# start_time = time.time()
# print(evaluate(board))
# end_time = time.time()
# print(end_time - start_time)

# for line in board:
#     print(line)
#
# x = spiral(board)
# print(x)


# The way I am writing code I pass to the node the move I make and
# the color that it will play
# And it updates the last move that I made.
# So before I pass the node to the next depth
# I should check if we have reached any terminal condition and
# if yes accordingly evaluate my position at current depth.
# The terminal conditions that can occur at current depth
# Can only result in either my piece winning or drawing the game.
# In a sense we check for the terminal conditions and give +ve (inf)
# If our player wins otherwise we give (-inf)
# On max nodes I think it is only possible for our player to win.
# Hence, on max we return a plus (inf) if we find a win condition.
# On Min we return a (-inf) if we find a win condition (this is an opponent's win)
# For draws we have to consider values like 0
