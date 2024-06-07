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

    return False