import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    # Check rows
    for row in board:
        if all(s == player for s in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def board_full(board):
    return all(cell != '-' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 10 - depth
    if check_win(board, 'X'):
        return depth - 10
    if board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = '-'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = '-'
                    best_score = min(score, best_score)
        return best_score

def get_cpu_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def get_player_move(board):
    while True:
        try:
            row = int(input("Enter row (0, 1, or 2): "))
            col = int(input("Enter column (0, 1, or 2): "))
            if 0 <= row <= 2 and 0 <= col <= 2:
                if board[row][col] == '-':
                    return (row, col)
                else:
                    print("That spot is already taken.")
            else:
                print("Row and column must be between 0 and 2.")
        except ValueError:
            print("Please enter valid integers for row and column.")

def main():
    board = [['-' for _ in range(3)] for _ in range(3)]
    current_player = 'Player'  # Player starts first

    while True:
        print_board(board)
        if current_player == 'Player':
            row, col = get_player_move(board)
            board[row][col] = 'X'
            if check_win(board, 'X'):
                print_board(board)
                print("Congratulations! You win!")
                break
            current_player = 'CPU'
        else:
            print("CPU is making a move...")
            row, col = get_cpu_move(board)
            board[row][col] = 'O'
            if check_win(board, 'O'):
                print_board(board)
                print("CPU wins! Better luck next time.")
                break
            current_player = 'Player'

        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()
