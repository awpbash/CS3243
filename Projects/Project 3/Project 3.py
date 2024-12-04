from typing import Tuple, List, Literal

# State class
class State:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def win(self):
        """Check if the game is won by capturing the opponent's King."""
        opponent_color = 'black' if self.color == 'white' else 'white'
        return not any(piece.name == "King" and piece.color == opponent_color for piece in self.board.pieces)

    def generate_future_states(self):
        """Generate possible future states by applying all legal moves in a prioritized order."""
        legal_moves = get_legal_moves(self.board, self.color)
        ordered_moves = order_moves(legal_moves, self.board, self.color)  # Prioritize captures
        future_states = []

        for move in ordered_moves:
            new_pieces = [Piece(p.name, p.color, p.position) for p in self.board.pieces]
            new_board = Board(new_pieces)
            new_board.move_piece(move[0], move[1])

            if not any(piece.name == "King" and piece.color != self.color for piece in new_board.pieces):
                return [(State(new_board, self.color), move)]

            new_color = 'black' if self.color == 'white' else 'white'
            future_states.append((State(new_board, new_color), move))

        return future_states


    def eval(self):
        """Evaluate the current board state based on material value only."""
        piece_values = {"King": 1000, "Rook": 6, "Bishop": 5, "Knight": 4, "Squire": 3, "Combatant": 2}
        return sum(
            piece_values.get(piece.name, 0) * (1 if piece.color == 'white' else -1)
            for piece in self.board.pieces
        )

def order_moves(moves, board, color):
    """Simple heuristic for ordering moves, prioritizing captures."""
    piece_values = {"King": 1000, "Rook": 6, "Bishop": 5, "Knight": 4, "Squire": 3, "Combatant": 2}
    ordered_moves = []
    for move in moves:
        start_pos, end_pos = move
        score = 0
        target_piece = board.get_piece(end_pos)
        if target_piece and target_piece.color != color:
            score += piece_values.get(target_piece.name, 0)  # Higher score for captures
        ordered_moves.append((move, score))

    ordered_moves.sort(key=lambda x: x[1], reverse=True)  # Sort by score
    return [move[0] for move in ordered_moves]

# Alpha-beta pruning function without Zobrist hashing or transposition table
def alpha_beta_pruning(state, depth, alpha, beta, maximizingPlayer):
    """Alpha-beta pruning function without transposition table."""
    if depth == 0 or state.win():
        return state.eval(), None

    best_move = None
    if maximizingPlayer:
        value = -float('inf')
        for child, move in state.generate_future_states():
            eval, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, False)
            if eval > value:
                value = eval
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = float('inf')
        for child, move in state.generate_future_states():
            eval, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, True)
            if eval < value:
                value = eval
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move

# Piece and Board classes (same as your existing classes)
class Piece:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position

    def __repr__(self):
        return f"{self.name}({self.color}) at {self.position}"

class Board:
    def __init__(self, pieces):
        self.pieces = pieces
        self.piece_map = {piece.position: piece for piece in pieces}

    def get_piece(self, position):
        return self.piece_map.get(position, None)

    def move_piece(self, start_position, new_position):
        piece = self.get_piece(start_position)
        captured_piece = self.get_piece(new_position)

        if captured_piece:
            self.pieces.remove(captured_piece)
            del self.piece_map[new_position]

        piece.position = new_position
        self.piece_map[new_position] = piece
        del self.piece_map[start_position]

    def occupied(self, position):
        return position in self.piece_map

# Function to find legal moves
def get_legal_moves(piece_entry, color: Literal['white', 'black']):
    if isinstance(piece_entry, list) and isinstance(piece_entry[0], tuple):
        pieces = [Piece(name, color, position) for name, color, position in piece_entry]
        board = Board(pieces)
    else:
        board = piece_entry

    legal_moves = []
    for piece in board.pieces:
        if piece.color == color:
            if piece.name == "King":
                legal_moves += [(piece.position, move) for move in get_king_moves(board, piece)]
            elif piece.name == "Rook":
                legal_moves += [(piece.position, move) for move in get_rook_moves(board, piece)]
            elif piece.name == "Bishop":
                legal_moves += [(piece.position, move) for move in get_bishop_moves(board, piece)]
            elif piece.name == "Knight":
                legal_moves += [(piece.position, move) for move in get_knight_moves(board, piece)]
            elif piece.name == "Squire":
                legal_moves += [(piece.position, move) for move in get_squire_moves(board, piece)]
            elif piece.name == "Combatant":
                legal_moves += [(piece.position, move) for move in get_combatant_moves(board, piece)]
    return legal_moves

# Initialize agent and call alpha-beta pruning
def studentAgent(gameboard: List[Tuple[str, str, Tuple[int, int]]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pieces = [Piece(name, color, position) for name, color, position in gameboard]
    board = Board(pieces)
    start = State(board, 'white')
    score, best_move = alpha_beta_pruning(start, 5, -float('inf'), float('inf'), True)
    return best_move if best_move else None

# Move generation functions
def get_king_moves(board, piece):
    moves = []
    x, y = piece.position
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_position = (x+i, y+j)
            if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                if not board.occupied(new_position):
                    moves.append(new_position)
                else:
                    if board.get_piece(new_position).color != piece.color:
                        moves.append(new_position)
    return moves
def get_rook_moves(board, piece):
    moves = []
    x, y = piece.position
    
    # Directions in which the rook can move: vertical and horizontal
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Up, Down
    
    for dx, dy in directions:
        nx, ny = x, y
        while True:
            nx += dx
            ny += dy
            
            # Break if out of bounds
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break
            
            # Get the piece at the new position
            target_piece = board.get_piece((nx, ny))
            
            # If the square is not occupied, it's a valid move
            if target_piece is None:
                moves.append((nx, ny))
            else:
                # If it's an opponent's piece, capture and stop
                if target_piece.color != piece.color:
                    moves.append((nx, ny))
                # If it's our piece, stop here (but don't capture)
                break
    
    return moves
def get_bishop_moves(board, piece):
    moves = []
    x, y = piece.position
    
    # Bishop moves in four diagonal directions
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dx, dy in directions:
        nx, ny = x, y
        
        # Continue moving in the current direction until we hit a boundary or piece
        while True:
            nx += dx
            ny += dy
            
            # Check if the new position is within bounds
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break  # Stop if out of bounds
            
            # If the position is occupied, check if it's an opponent's piece and stop
            if board.occupied((nx, ny)):
                if board.get_piece((nx, ny)).color != piece.color:
                    moves.append((nx, ny))  # Capturing move
                break  # Stop after encountering any piece (either friendly or opponent)
            else:
                # If the position is not occupied, add it as a legal move
                moves.append((nx, ny))
    
    return moves
def get_knight_moves(board, piece):
    moves = []
    x, y = piece.position
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i) + abs(j) == 3:
                new_position = (x+i, y+j)
                if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                    if not board.occupied(new_position):
                        moves.append(new_position)
                    else:
                        if board.get_piece(new_position).color != piece.color:
                            moves.append(new_position)
    return moves
def get_squire_moves(board, piece):
    moves = []
    x, y = piece.position
    directions = [(2,0), (-2,0), (0,2), (0,-2), (1, 1), (1, -1), (-1, 1), (-1, -1)] #manhattan distance of 2
    for direction in directions:
        new_position = (x+direction[0], y+direction[1])
        if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
            if not board.occupied(new_position):
                moves.append(new_position)
            else:
                if board.get_piece(new_position).color != piece.color:
                    moves.append(new_position)
    return moves
def get_combatant_moves(board, piece):
    moves = []
    orthogonal = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    x, y = piece.position
    for direction in orthogonal:
        new_position = (x+direction[0], y+direction[1])
        if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
            if not board.occupied(new_position):
                moves.append(new_position)
    for direction in diagonal:
        new_position = (x+direction[0], y+direction[1])
        if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
            target_piece = board.get_piece(new_position)
            if target_piece and target_piece.color != piece.color:
                moves.append(new_position)  # Capturing move
    return moves