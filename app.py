from flask import Flask, render_template, request, jsonify
from app.zone_logic import initialize_board, is_valid_move, move_piece, get_valid_moves



app = Flask(__name__)

# Initialize the board with pieces and zones
board = initialize_board()

current_turn = 1  # 1 for Player 1, 2 for Player 2

@app.route('/')
def index():
    # The board layout for the custom chessboard zones
    board_layout = [
        [{'image': 'zone_4_black.png', 'rotation': 180}, {'image': 'zone_4_black.png', 'rotation': 180}, 
         {'image': 'zone_4_black.png', 'rotation': 180}, {'image': 'zone_4_black.png', 'rotation': 180}, 
         {'image': 'zone_4_black.png', 'rotation': 180}, {'image': 'zone_4_black.png', 'rotation': 180}, 
         {'image': 'zone_4_black.png', 'rotation': 180}, {'image': 'zone_4_black.png', 'rotation': 180}, ],
        
        [{'image': 'zone_3_corner.png', 'rotation': 180}, {'image': 'zone_3_straight_edge.png', 'rotation': 180}, 
        {'image': 'zone_3_straight_edge.png', 'rotation': 180}, {'image': 'zone_3_straight_edge.png', 'rotation': 180},
        {'image': 'zone_3_straight_edge.png', 'rotation': 180}, {'image': 'zone_3_straight_edge.png', 'rotation': 180}, 
        {'image': 'zone_3_straight_edge.png', 'rotation': 180}, {'image': 'zone_3_corner.png', 'rotation': -90}],

        [{'image': 'zone_3_straight_edge.png', 'rotation': 90}, {'image': 'zone_2_corner.png', 'rotation': 180},
        {'image': 'zone_2_straight_edge.png', 'rotation': 180}, {'image': 'zone_2_straight_edge.png', 'rotation': 180},
        {'image': 'zone_2_straight_edge.png', 'rotation': 180}, {'image': 'zone_2_straight_edge.png', 'rotation': 180},
        {'image': 'zone_2_corner.png', 'rotation': -90}, {'image': 'zone_3_straight_edge.png', 'rotation': -90}],
        
        [{'image': 'zone_3_straight_edge.png', 'rotation': 90}, {'image': 'zone_2_straight_edge.png', 'rotation': 90},
        {'image': 'zone_1_corner.png', 'rotation': 180}, {'image': 'zone_1_straight_edge.png', 'rotation': 180},
        {'image': 'zone_1_straight_edge.png', 'rotation': 180}, {'image': 'zone_1_corner.png', 'rotation': -90},
        {'image': 'zone_2_straight_edge.png', 'rotation': -90}, {'image': 'zone_3_straight_edge.png', 'rotation': -90}],

        [{'image': 'zone_3_straight_edge.png', 'rotation': 90}, {'image': 'zone_2_straight_edge.png', 'rotation': 90},
         {'image': 'zone_1_corner.png', 'rotation': 90}, {'image': 'zone_1_straight_edge.png', 'rotation': 0},
         {'image': 'zone_1_straight_edge.png', 'rotation': 0}, {'image': 'zone_1_corner.png', 'rotation': 360},
         {'image': 'zone_2_straight_edge.png', 'rotation': -90}, {'image': 'zone_3_straight_edge.png', 'rotation': -90}],
        
        [{'image': 'zone_3_straight_edge.png', 'rotation': 90}, {'image': 'zone_2_corner.png', 'rotation': 90},
         {'image': 'zone_2_straight_edge.png', 'rotation': 0}, {'image': 'zone_2_straight_edge.png', 'rotation': 0},
         {'image': 'zone_2_straight_edge.png', 'rotation': 0}, {'image': 'zone_2_straight_edge.png', 'rotation': 0},
         {'image': 'zone_2_corner.png', 'rotation': 0}, {'image': 'zone_3_straight_edge.png', 'rotation': -90}],
        
        [{'image': 'zone_3_corner.png', 'rotation': 90}, {'image': 'zone_3_straight_edge.png', 'rotation': 0}, 
         {'image': 'zone_3_straight_edge.png', 'rotation': 0}, {'image': 'zone_3_straight_edge.png', 'rotation': 0},
         {'image': 'zone_3_straight_edge.png', 'rotation': 0}, {'image': 'zone_3_straight_edge.png', 'rotation': 0},
         {'image': 'zone_3_straight_edge.png', 'rotation': 0}, {'image': 'zone_3_corner.png', 'rotation': 0}],

        [{'image': 'zone_4_white.png', 'rotation': 0}, {'image': 'zone_4_white.png', 'rotation': 0}, 
         {'image': 'zone_4_white.png', 'rotation': 0}, {'image': 'zone_4_white.png', 'rotation': 0},
         {'image': 'zone_4_white.png', 'rotation': 0}, {'image': 'zone_4_white.png', 'rotation': 0}, 
         {'image': 'zone_4_white.png', 'rotation': 0}, {'image': 'zone_4_white.png', 'rotation': 0}]
    ]
    
    return render_template('index.html', board_layout=board_layout, chess_pieces=board, enumerate=enumerate)


@app.route('/move', methods=['POST'])
def move():
    global current_turn
    data = request.get_json()
    start_pos = data['start']
    end_pos = data['end']
    piece = board[start_pos[0]][start_pos[1]]

    # Check if it's the current player's turn
    if (current_turn == 1 and piece['color'] != 'white') or (current_turn == 2 and piece['color'] != 'black'):
        return jsonify({"error": "Not your turn!"}), 400

    # Validate and make the move
    if is_valid_move(piece, start_pos, end_pos, board):
        board = move_piece(start_pos, end_pos, board)
        
        # Switch turns
        current_turn = 1 if current_turn == 2 else 2
        
        return jsonify({"board": board, "current_turn": current_turn, "success": True})
    else:
        return jsonify({"error": "Invalid move!"}), 400

@app.route('/valid_moves', methods=['POST'])
def valid_moves():
    data = request.get_json()
    start_pos = data['start']
    piece = board[start_pos[0]][start_pos[1]]
    
    # Get all valid moves for the selected piece
    valid_moves = get_valid_moves(piece, start_pos, board)
    
    return jsonify({"valid_moves": valid_moves})

if __name__ == '__main__':
    app.run(debug=True)
