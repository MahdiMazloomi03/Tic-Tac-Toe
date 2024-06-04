import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * (4 * len(row) - 1))

def evaluate(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if all(cell == 'X' for cell in row):
            return 1
        elif all(cell == 'O' for cell in row):
            return -1

    for col in range(len(board[0])):
        if all(board[row][col] == 'X' for row in range(len(board))):
            return 1
        elif all(board[row][col] == 'O' for row in range(len(board))):
            return -1

    if all(board[i][i] == 'X' for i in range(len(board))) or all(board[i][len(board) - 1 - i] == 'X' for i in range(len(board))):
        return 1
    elif all(board[i][i] == 'O' for i in range(len(board))) or all(board[i][len(board) - 1 - i] == 'O' for i in range(len(board))):
        return -1

    # Check for a draw
    if all(cell != ' ' for row in board for cell in row):
        return 0

    return None

def is_terminal(board):
    return evaluate(board) is not None

def get_empty_cells(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == ' ']

def minimax(board, depth, alpha, beta, maximizing_player):
    result = evaluate(board)

    if result is not None or depth == 0:
        return result

    empty_cells = get_empty_cells(board)

    if maximizing_player:
        max_eval = float('-inf')
        for cell in empty_cells:
            i, j = cell
            board[i][j] = 'X' if depth % 2 == 0 else 'O'
            print(f"Max: Trying ({i}, {j}), alpha = {alpha}, beta = {beta}")
            eval = minimax(board, depth - 1, alpha, beta, False) or 0  # Default to 0 if the result is None
            board[i][j] = ' '  # Undo the move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            print(f"Max: ({i}, {j}) -> eval = {eval}, alpha = {alpha}, beta = {beta}")
            if beta <= alpha:
                print("Max: Pruning!")
                break
        return max_eval
    else:
        min_eval = float('inf')
        for cell in empty_cells:
            i, j = cell
            board[i][j] = 'X' if depth % 2 == 0 else 'O'
            print(f"Min: Trying ({i}, {j}), alpha = {alpha}, beta = {beta}")
            eval = minimax(board, depth - 1, alpha, beta, True) or 0  
            board[i][j] = ' '  # Undo the move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            print(f"Min: ({i}, {j}) -> eval = {eval}, alpha = {alpha}, beta = {beta}")
            if beta <= alpha:
                print("Min: Pruning!")
                break
        return min_eval

def get_best_move(board, difficulty, depth, size):
    if difficulty == 'easy' or size > 3:
        depth_limit = 2
    elif difficulty == 'hard':
        depth_limit = float('inf')
    else:
        raise ValueError("Invalid difficulty level. Use 'easy' or 'hard'.")

    best_move = None
    best_eval = float('-inf')
    empty_cells = get_empty_cells(board)

    for cell in empty_cells:
        i, j = cell
        board[i][j] = 'X' if depth % 2 == 0 else 'O'
        eval = minimax(board, depth_limit, float('-inf'), float('inf'), False)
        board[i][j] = ' '  # Undo the move

        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)

    return best_move

def play_tic_tac_toe():
    size = int(input("Enter the size of the board (e.g., 3 for a 3x3 board): "))
    difficulty = input("Choose difficulty level ('easy' or 'hard'): ")
    mode = input("Choose game mode ('1' for player vs computer, '2' for computer vs computer): ")

    board = [[' ' for _ in range(size)] for _ in range(size)]
    player_turn = True  # True if player's turn, False if computer's turn

    while not is_terminal(board):
        print_board(board)

        if player_turn and mode == '1':
            row = int(input(f"Enter the row (0 to {size-1}): "))
            col = int(input(f"Enter the column (0 to {size-1}): "))
            if board[row][col] == ' ':
                board[row][col] = 'O'
            else:
                print("Cell already occupied. Try again.")
                continue
        else:
            print("Computer's turn:")
            move = get_best_move(board, difficulty, len(get_empty_cells(board)), size)
            if (size%2):
                symbol = 'X' if len(get_empty_cells(board)) % 2 == 0 else 'O'
            else:
                symbol = 'O' if len(get_empty_cells(board)) % 2 == 0 else 'X'
            board[move[0]][move[1]] = symbol
            print(f"{symbol} played at ({move[0]}, {move[1]})")

        player_turn = not player_turn if mode == '1' else True

    print_board(board)
    result = evaluate(board)

    if result == -1:
        if player_turn and mode == '1':
            print("You win!")
        else:
            print("Computer 2 wins!" if mode == '2' else "Computer wins!")
    elif result == 1:
        if player_turn and mode == '1':
            print("Computer wins!")
        else:
            print("You win!" if mode == '1' else "Computer 1 wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_tic_tac_toe()

