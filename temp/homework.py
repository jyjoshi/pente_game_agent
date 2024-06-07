import copy
import time


def read():
    global color, black_captures, board, white_count, black_count
    global remaining_time, captures, white_captures

    file = open("input.txt", "r")
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
    file = open("output.txt", "w")
    file.write(y_coordinate + x_coordinate)
    file.close()


def rev_output(move):
    alphabets = "ABCDEFGHJKLMNOPQRST"
    y_coordinate = str(19 - move[0])
    x_coordinate = alphabets[move[1]]
    print(x_coordinate + y_coordinate)


# Gives win by sequence the move needs to be provided as [x_coordinate, y_coordinate]
def check_win_sequence(board, move):

    x, y = move
    color = board[x][y]
    # print(board[x][y])
    if color == ".":
        return False

    for i in range(y - 4, y + 1):
        if i < 0 or i + 5 > 19:
            continue

        if board[x][i:i + 5] == [color] * 5:
            # print("Horizontal Triggered")
            return True

    # Check for vertical sequence of 5
    for j in range(x - 4, x + 1):
        if j < 0 or j + 5 > 19:
            continue
        if [board[j + i][y] for i in range(5)] == [color] * 5:
            # print("Vertical Triggered")
            return True

    # Check for diagonal (top-left to bottom-right) sequence of 5
    for i, j in zip(range(x - 4, x + 1), range(y - 4, y + 1)):
        if i < 0 or j < 0 or i + 5 > 19 or j + 5 > 19:
            continue
        if [board[i + k][j + k] for k in range(5)] == [color] * 5:
            # print("TL - BR Triggered")
            return True

    # Check for diagonal (top-right to bottom-left) sequence of 5
    for i, j in zip(range(x - 4, x + 1), range(y + 4, y - 1, -1)):
        if i < 0 or j < 0 or i + 5 > 19 or j - 4 < 0 or j > 18:
            continue

        if [board[i + k][j - k] for k in range(5)] == [color] * 5:
            # print("TR - BL Triggered")
            return True


    # print((end - start) * 10 ** 5)
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

    if not isValidMove([x + 3, y]):
        if not isValidMove([x, y + 3]):
            possible_directions = [4, 5, 6]
        elif not isValidMove([x, y - 3]):
            possible_directions = [0, 6, 7]
        else:
            possible_directions = [0, 4, 5, 6, 7]
    elif not isValidMove([x - 3, y]):
        if not isValidMove([x, y + 3]):
            possible_directions = [2, 3, 4]
        elif not isValidMove([x, y - 3]):
            possible_directions = [0, 1, 2]
        else:
            possible_directions = [0, 1, 2, 3, 4]
    elif not isValidMove([x, y + 3]):
        possible_directions = [2, 3, 4, 5, 6]
    elif not isValidMove([x, y - 3]):
        possible_directions = [0, 1, 2, 6, 7]
    else:
        possible_directions = [0, 1, 2, 3, 4, 5, 6, 7]

    if board[x][y] == "b":
        piece = "w"
    else:
        piece = "b"
    count = 0
    capture_count = 0
    # print(possible_directions)
    for i in possible_directions:
        y_val = y + directions[i][0][0]
        x_val = x + directions[i][0][1]
        if board[x + directions[i][0][0]][y + directions[i][0][1]] == piece \
                and board[x + directions[i][1][0]][y + directions[i][1][1]] == piece \
                and board[x + directions[i][2][0]][y + directions[i][2][1]] == board[x][y]:
            # print("Capture possible at ", directions[i])
            capture_count += 2
            board[x + directions[i][0][0]][y + directions[i][0][1]] = "."
            board[x + directions[i][1][0]][y + directions[i][1][1]] = "."
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
                 white_count,
                 black_count):
        self.color = color
        self.white_captures = white_captures
        self.black_captures = black_captures
        self.move = move
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


def sliding_window(grid, window_size, pattern):
    matches = 0
    half_window = window_size // 2

    # iterate over all positions in the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # check horizontal pattern match
            if j <= len(grid[0]) - window_size:
                # if grid[i][j] == pattern[0] and
                #     grid[i][j] == pattern[0] and
                #     grid[i][j] == pattern[0] and
                #     grid[i][j] == pattern[0] and
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
    if node.color == "BLACK":
        color_param = "WHITE"
    else:
        color_param = "BLACK"

    # if check_draw(node.board):
    #     return 0, node.move, node

    if depth == 0:
        return evaluate(node.board, node), node.move, node

    moves = spiral(node.board)
    best_move = moves[0]

    if maximizing_player:
        best_node = None
        value = -float("inf")
        for move in moves:
            new_node = Node(node.board,
                            move,
                            node.white_captures,
                            node.black_captures,
                            color_param,
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
                # print("Infinity Here")
                return float("inf"), move, new_node
            elif (node.piece == "b" and new_node.black_captures >= 10) or \
                    (node.piece == "w" and new_node.white_captures >= 10):
                # print("Maybe Here")
                return float("inf"), move, new_node

            local_val, local_move, local_node = alpha_beta(new_node, depth - 1, alpha, beta, False)
            if local_val > value:
                best_move = move
                value = local_val
                best_node = local_node
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move, best_node
    else:
        best_node = None
        value = float("inf")
        for move in moves:
            # if node.move == [8, 6] and move == [7, 7]:
            #     print("Move Reached")
            new_node = Node(node.board,
                            move,
                            node.white_captures,
                            node.black_captures,
                            color_param,
                            node.white_count,
                            node.black_count)
            # if new_node.move == [7, 7] and new_node.parent.move == [8, 6]:
            #     print("The board is looking like")
            #     for line in new_node.board:
            #         print(line)
            #     print("Where we need to be")

            capture_count = update_board_for_captures(new_node.board, move)
            if node.piece == "b":
                new_node.white_count -= capture_count
                new_node.black_captures += capture_count
            else:
                new_node.black_count -= capture_count
                new_node.white_captures += capture_count
            # print(new_node.board)
            if check_win_sequence(new_node.board, move):
                # print("-Infinity triggered")
                return -float("inf"), move, new_node
            elif (node.piece == "b" and new_node.black_captures >= 10) or (
                    node.piece == "w" and new_node.white_captures >= 10):
                # print("Maybe Here?")
                return -float("inf"), move, new_node
            local_val, local_move, local_node = alpha_beta(new_node, depth - 1, alpha, beta, True)
            if local_val < value:
                # print("Inside val update")
                value = local_val
                best_move = move
                best_node = local_node
                # print("Value updated", value)
            beta = min(beta, value)
            if alpha >= beta:
                # print("Break in min occured. Node : ", node.move)
                break
        return value, best_move, best_node


# open4s_w =
# open4s_b =
# closed4s_w =
# closed4s_b =
# open3s_b = [['.', 'b', 'b', 'b', '.']]
# open3s_w = [['.', 'w', 'w', 'w', '.']]
# closed3s =



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
capture_weights = [100, 100, 3, 3, 6]

b_block_patterns = [['b', 'w', 'w', 'w', 'w', 'b'], ['b', 'w', 'w', 'w', 'b'], ['b', 'w', 'w', 'b']]
w_block_patterns = [['w', 'b', 'b', 'b', 'b', 'w'], ['w', 'b', 'b', 'b', 'w'], ['w', 'b', 'b', 'w']]
block_weights = [10000, 600, 15]


def evaluate(xboard, node):
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






def is_first_white_move():
    if white_count == 0 and black_count == 0 and white_captures == 0 and black_captures == 0:
        return True
    else:
        return False


def is_second_white_move(board):
    if white_count == 1 and black_count == 1 and white_captures == 0 and black_captures == 0:
        if board[9][12] == ".":
            return True, [9, 12]
        else:
            return True, [9, 6]
    else:
        return False, []


def is_black_first_move():
    if white_count == 1 and black_count == 0 and white_captures == 0 and black_captures == 0:
        return True
    else:
        return False


def get_move(node, depth):
    print("In Return Action")
    if color == 'WHITE':
        if is_first_white_move():
            return [9, 9]
        is_second_move, second_move = is_second_white_move(node.board)
        if is_second_move:
            return second_move
    elif color == 'BLACK':
        if is_black_first_move():
            return [10, 9]

    return alpha_beta(node, depth, -float("inf"), float("inf"), True)[1]


INITIAL_DEPTH = 2

read()
if remaining_time <= 100:
    INITIAL_DEPTH = 1

move = [-1, -1]
node = Node(board,
            move,
            white_captures,
            black_captures,
            color,
            white_count,
            black_count)

start = time.time()

move = get_move(node, INITIAL_DEPTH)
print(move)
end = time.time()

print(end - start)

output(move)
