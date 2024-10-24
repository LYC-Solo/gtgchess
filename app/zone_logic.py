def initialize_board():
    return [
        ["brook", "bknight", "bbishop", "bking", "bqueen", "bbishop", "bknight", "brook"],
        ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"],
        ["wrook", "wknight", "wbishop", "wking", "wqueen", "wbishop", "wknight", "wrook"]
    ]

# Function to move a piece on the board
def move_piece(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]  # Get the piece at the start position
    board[end_pos[0]][end_pos[1]] = piece  # Move the piece to the end position
    board[start_pos[0]][start_pos[1]] = None  # Empty the start position
    return board  # Return the updated board

def get_valid_moves(piece, start_pos, board):
    valid_moves = []
    
    # Loop through all possible positions on the board
    for row in range(8):
        for col in range(8):
            if is_valid_move(piece, start_pos, (row, col), board):
                valid_moves.append((row, col))
                
    return valid_moves

def is_valid_move(board, start_pos, end_pos):
    start_piece = board[start_pos[0]][start_pos[1]]
    end_piece = board[end_pos[0]][end_pos[1]]

    if start_piece is None:
        return False  # No piece at the start position

    piece_type = start_piece[1:]  # Remove 'w' or 'b' to get piece type
    if piece_type == 'pawn':
        return validate_pawn_move(start_piece, start_pos, end_pos, board)
    elif piece_type == 'rook':
        return validate_rook_move(start_piece, start_pos, end_pos, board)
    elif piece_type == 'knight':
        return validate_knight_move(start_piece, start_pos, end_pos)
    elif piece_type == 'bishop':
        return validate_bishop_move(start_piece, start_pos, end_pos, board)
    elif piece_type == 'queen':
        return validate_queen_move(start_piece, start_pos, end_pos, board)
    elif piece_type == 'king':
        return validate_king_move(start_piece, start_pos, end_pos, board)

    return False  # Invalid piece

def validate_pawn_move(piece, start_pos, end_pos, board):
    direction = 1 if piece[0] == 'w' else -1  # White pawns move up, black pawns move down
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_col == end_col:  # Moving forward
        if (end_row - start_row) == direction and board[end_row][end_col] is None:
            return True
        if (end_row - start_row) == 2 * direction and start_row in [1, 6] and board[end_row][end_col] is None:
            return True
    elif abs(start_col - end_col) == 1 and (end_row - start_row) == direction:  # Capturing diagonally
        if board[end_row][end_col] is not None and board[end_row][end_col][0] != piece[0]:
            return True

    return False

def validate_rook_move(piece, start_pos, end_pos, board):
    return validate_straight_move(piece, start_pos, end_pos, board)

def validate_knight_move(piece, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
        return True
    if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
        return True
    return False

def validate_bishop_move(piece, start_pos, end_pos, board):
    return validate_diagonal_move(piece, start_pos, end_pos, board)

def validate_queen_move(piece, start_pos, end_pos, board):
    return validate_straight_move(piece, start_pos, end_pos, board) or validate_diagonal_move(piece, start_pos, end_pos, board)

def validate_king_move(piece, start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        return True
    return False

def validate_straight_move(piece, start_pos, end_pos, board):
    # Check for straight line moves (Rook, Queen)
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row == end_row:  # Horizontal move
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] is not None:
                return False
        return True
    elif start_col == end_col:  # Vertical move
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] is not None:
                return False
        return True

    return False

def validate_diagonal_move(piece, start_pos, end_pos, board):
    # Check for diagonal line moves (Bishop, Queen)
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if abs(start_row - end_row) == abs(start_col - end_col):
        step_row = 1 if start_row < end_row else -1
        step_col = 1 if start_col < end_col else -1
        for i in range(1, abs(start_row - end_row)):
            if board[start_row + i * step_row][start_col + i * step_col] is not None:
                return False
        return True

    return False
