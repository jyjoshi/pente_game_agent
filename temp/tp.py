def alpha_beta_search(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or state.is_terminal():
        return state.get_utility(), None

    best_move = None
    if maximizing_player:
        best_value = -float("inf")
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value, _ = alpha_beta_search(new_state, depth - 1, alpha, beta, False)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        if depth == INITIAL_DEPTH:  # only update best move at root node
            return best_move
        else:
            return best_value
    else:
        best_value = float("inf")
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value, _ = alpha_beta_search(new_state, depth - 1, alpha, beta, True)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if alpha >= beta:
                break
        if depth == INITIAL_DEPTH:  # only update best move at root node
            return best_move
        else:
            return best_value

INITIAL_DEPTH = 4  # depth of search at root node
best_move = alpha_beta_search(initial_state, INITIAL_DEPTH, -float("inf"), float("inf"), True)
