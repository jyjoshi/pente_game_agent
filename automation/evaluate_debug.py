board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'w', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', 'w', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'w', 'b', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
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
color = "WHITE"


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
        if b_count or w_count:
            print("Pattern", b_patterns[i])
            print("Weights", weights[i])
            print("Black Count", b_count)
            print("White Count", w_count)
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
        value += (b_count - w_count) * capture_weights[i]
        if b_count or w_count:
            print("Pattern", b_capture_patterns[i])
            print("Weights", weights[i])
            print("Black Count", b_count)
            print("White Count", w_count)


    for i in range(len(b_block_patterns)):
        b = b_block_patterns[i]
        w = w_block_patterns[i]
        b_count = sliding_window(xboard, len(b), b)
        w_count = sliding_window(xboard, len(w), w)
        value += (b_count - w_count) * block_weights[i]
        if b_count or w_count:
            print("Pattern", b_block_patterns[i])
            print("Weights", weights[i])
            print("Black Count", b_count)
            print("White Count", w_count)
    return multiplier * value


for line in board:
    print(line)
print(evaluate(board))