

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

board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'w', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', 'w', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
pattern = ['w', 'b', 'b', 'b', 'b', 'w']

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
        # if b_count != 0:
        #     print("B Pattern Matched", b)
        # if w_count != 0:
        #     print("W Pattern Matched", w)
        #     # for line in xboard:
        #     #     print(line)
        value += (b_count - w_count) * weights[i]
    for i in range(len(b_capture_patterns)):
        b = b_capture_patterns[i]
        w = w_capture_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * weights[i]

    for i in range(len(b_block_patterns)):
        b = b_block_patterns[i]
        w = w_block_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * weights[i]
        if i == 0 and w_count > 0 and value == 1800:
            print("Pattern triggered")
            print("value ", value)
            print(xboard)
    return multiplier * value
