def check_win_sequence(board, move):
    x, y = move
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

read()
move = [6, 8]
for line in board:
    print(line)
print(check_win_sequence(board, move))


