#include <stdio.h>

char board[3][3];  // 3x3 board

// Function to initialize the board with numbers
void initBoard() {
    char c = '1';
    for(int i=0;i<3;i++) {
        for(int j=0;j<3;j++) {
            board[i][j] = c++;
        }
    }
}

// Function to display the board
void displayBoard() {
    printf("\n");
    for(int i=0;i<3;i++) {
        for(int j=0;j<3;j++) {
            printf(" %c ", board[i][j]);
            if(j<2) printf("|");
        }
        printf("\n");
        if(i<2) printf("---+---+---\n");
    }
    printf("\n");
}

// Function to check if a player has won
int checkWin() {
    for(int i=0;i<3;i++) {
        // Check rows
        if(board[i][0]==board[i][1] && board[i][1]==board[i][2])
            return 1;
        // Check columns
        if(board[0][i]==board[1][i] && board[1][i]==board[2][i])
            return 1;
    }
    // Check diagonals
    if(board[0][0]==board[1][1] && board[1][1]==board[2][2])
        return 1;
    if(board[0][2]==board[1][1] && board[1][1]==board[2][0])
        return 1;

    return 0;
}

// Function to check if board is full (draw)
int isFull() {
    for(int i=0;i<3;i++)
        for(int j=0;j<3;j++)
            if(board[i][j] != 'X' && board[i][j] != 'O')
                return 0;
    return 1;
}

int main() {
    int choice, row, col, player=1;
    char mark;

    initBoard();
    
    while(1) {
        displayBoard();
        mark = (player == 1) ? 'X' : 'O';
        printf("Player %d (%c), enter position (1-9): ", player, mark);
        scanf("%d", &choice);

        if(choice < 1 || choice > 9) {
            printf("Invalid move, try again.\n");
            continue;
        }

        row = (choice-1)/3;
        col = (choice-1)%3;

        if(board[row][col] == 'X' || board[row][col] == 'O') {
            printf("Position already taken, try again.\n");
            continue;
        }

        board[row][col] = mark;

        if(checkWin()) {
            displayBoard();
            printf("Player %d wins!\n", player);
            break;
        }

        if(isFull()) {
            displayBoard();
            printf("It's a draw!\n");
            break;
        }

        player = (player==1) ? 2 : 1;  // Switch player
    }

    return 0;
}
