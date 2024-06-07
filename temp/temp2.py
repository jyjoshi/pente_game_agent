import time


def read():
    global color, black_captures, board, white_count, black_count
    global remaining_time, captures, white_captures

    file = open("input.txt", "r")
    color = file.readline()
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


size = 19
start = time.time()
x = [["0" for i in range(size)] for j in range(size)]


# print(x)


def modifyBoard(x, a, b):
    new_board = [["1" if (i, j) == (a, b) else x[i][j] for i in range(size)] for j in range(size)]
    # print(new_board)


# a, b = (2, 0)
# modifyBoard(x, a, b)
# # print(x)
# end = time.time()
# print((end - start) * 150 ** 2)


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
            if color == "BlACK":
                self.piece = "b"
                self.opp_piece = "w"
            else:
                self.piece = "w"
                self.opp_piece = "b"
            self.board = [[board[j][i] for i in range(19)] for j in range(19)]
        else:
            self.board = [
                ["w" if color == "BLACK" else "b" if ((i == move[0]) and (j == move[1])) else board[j][i] for i in
                 range(19)] for j in range(19)]
            if self.board[move[1]][move[0]] == "w":
                self.piece = "b"
                self.opp_piece = "w"
                self.white_count = white_count + 1
                self.black_count = black_count
            else:
                self.piece = "w"
                self.opp_piece = "b"
                self.black_count = black_count + 1
                self.white_count = white_count


start = time.time()
read()
print(check_draw(board))
end = time.time()

print((end - start) * 1000)


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


def alpha_beta(node, board, depth, alpha, beta, maximizing_player):
    if node.color == "BLACK":
        color_param = "WHITE"
    else:
        color_param = "BLACK"
    if depth == 0:
        return evaluate(node)

    if maximizing_player:
        value = -float("inf")
        for move in get_possible_moves(node.board):
            new_board = make_move(board, move)
            new_node = (node.board, move, node.white_captures, node.black_captures, color_param, node.remaining_time,
                        node.white_count, node.black_count)
            # Check for terminal cases at this level
            if check_win_sequence(new_node.board, move):
                return float("inf")
            elif (node.piece == "b" and new_node.black_captures >= 10) or (
                    node.piece == "w" and new_node.white_captures >= 10):
                return float("inf")
            elif check_draw(new_node.board):
                return 0
            else:
                value = max(value, alpha_beta(new_board, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float("inf")
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            value = min(value, alpha_beta(new_board, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def spiral_traversal(grid):
    """
    Traverse the 2D grid in a spiral pattern, starting from the center of the grid and spiraling outwards.
    Return the indices of the "." values in the order in which they are encountered.

    Args:
        grid (List[List[str]]): A 2D grid of strings.

    Returns:
        List[Tuple[int, int]]: The indices of the "." values in the spiral order.
    """
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns
    result = []

    # Initialize the center indices.
    row = m // 2
    col = n // 2
    step = 1

    # Traverse the grid in a spiral pattern, starting from the center.
    while row >= 0 and col >= 0:
        # Traverse the top row.
        for i in range(col - step + 1, col + step):
            if 0 <= row - step < m and 0 <= i < n and grid[row - step][i] == ".":
                result.append((row - step, i))
        # Traverse the right column.
        for i in range(row - step + 1, row + step):
            if 0 <= i < m and 0 <= col + step < n and grid[i][col + step] == ".":
                result.append((i, col + step))
        # Traverse the bottom row.
        for i in range(col + step - 1, col - step - 1, -1):
            if 0 <= row + step < m and 0 <= i < n and grid[row + step][i] == ".":
                result.append((row + step, i))
        # Traverse the left column.
        for i in range(row + step - 1, row - step - 1, -1):
            if 0 <= i < m and 0 <= col - step < n and grid[i][col - step] == ".":
                result.append((i, col - step))

        # Move to the next layer of the spiral.
        step += 1
        row -= 1
        col -= 1

    return result


print("This one counts")
start_draw_check = time.time()
check_draw(board)
end_draw_check = time.time()
print(end - start)

move = [0, 0]
node = Node(board, move, white_captures, black_captures, color, remaining_time, white_count, black_count)

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
# Hence on max we return a plus (inf) if we find a win condition.
# On Min we return a (-inf) if we find a win condition (this is an opponent's win)
# For draws we have to consider values like 0

