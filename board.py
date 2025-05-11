import pygame
from piece import Piece

# colors (you can change these)
WHITE = (245, 245, 245)
GRAY  = ( 50,  50,  50)
RED_COLOR   = (200,  50,  50)
BLACK_COLOR = ( 30,  30,  30)
GOLD = (255, 215,  0)

class Board:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self._setup_pieces()

    def _setup_pieces(self):
        for r in range(self.rows):
            for c in range(self.cols):
                # only place on dark squares
                if (r + c) % 2 == 0:
                    continue
                if r < 3:
                    # top three rows: black
                    self.grid[r][c] = Piece(r, c, "black")
                elif r > 4:
                    # bottom three rows: red
                    self.grid[r][c] = Piece(r, c, "red")

    def draw(self, surface):
        tile_size = surface.get_width() // self.cols
        # draw squares
        for r in range(self.rows):
            for c in range(self.cols):
                color = WHITE if (r + c) % 2 == 0 else GRAY
                rect = (c * tile_size, r * tile_size, tile_size, tile_size)
                pygame.draw.rect(surface, color, rect)
        # draw pieces
        for r in range(self.rows):
            for c in range(self.cols):
                piece = self.grid[r][c]
                if piece:
                    center = (c * tile_size + tile_size//2,
                              r * tile_size + tile_size//2)
                    radius = tile_size//2 - 8
                    col = RED_COLOR if piece.color == "red" else BLACK_COLOR
                    pygame.draw.circle(surface, col, center, radius)
                    if piece.king:
                        pygame.draw.circle(surface, GOLD, center, radius//2)

    def get_valid_moves(self, piece):
        if piece is None:
            return {}
        moves = {}
        directions = []
        # Regular men move forward only
        if piece.color == "red":
            directions = [(-1, -1), (-1, 1)]
        else:  # black
            directions = [(1, -1), (1, 1)]
        # Kings move both ways
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = piece.row + dr, piece.col + dc
            # Simple move
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] is None:
                moves[(r, c)] = []
            # Capture move?
            elif 0 <= r < self.rows and 0 <= c < self.cols \
                 and self.grid[r][c] is not None \
                 and self.grid[r][c].color != piece.color:
                jump_r, jump_c = r + dr, c + dc
                if 0 <= jump_r < self.rows and 0 <= jump_c < self.cols \
                   and self.grid[jump_r][jump_c] is None:
                    moves[(jump_r, jump_c)] = [(r, c)]
        return moves

    def move_piece(self, piece, dest_row, dest_col):
        captured = []
        dr = dest_row - piece.row
        dc = dest_col - piece.col
        if abs(dr) == 2 and abs(dc) == 2:
            mid_r = piece.row + dr // 2
            mid_c = piece.col + dc // 2
            captured_piece = self.grid[mid_r][mid_c]
            self.grid[mid_r][mid_c] = None
            captured.append(captured_piece)
        self.grid[piece.row][piece.col] = None
        piece.row, piece.col = dest_row, dest_col
        self.grid[dest_row][dest_col] = piece
        # King promotion
        if (piece.color == "red"   and dest_row == 0) \
        or (piece.color == "black" and dest_row == self.rows - 1):
            piece.make_king()
        return captured
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.grid:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def has_capture(self, color):
        for piece in self.get_all_pieces(color):
            for caps in self.get_valid_moves(piece).values():
                if caps: 
                    return True
        return False
    
    def encode_state(self):
        symbols = []
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.grid[r][c]
                if p is None:
                    symbols.append('.')
                else:
                    if p.color == "red":
                        symbols.append('R' if p.king else 'r')
                    else:
                        symbols.append('B' if p.king else 'b')
        return ''.join(symbols)
    
    def check_winner(self):
        # no pieces, opponent wins
        if not self.get_all_pieces("red"):
            return "black"
        if not self.get_all_pieces("black"):
            return "red"

        # no legal moves, opponent wins
        red_moves   = any(self.get_valid_moves(p) for p in self.get_all_pieces("red"))
        black_moves = any(self.get_valid_moves(p) for p in self.get_all_pieces("black"))
        if not red_moves:
            return "black"
        if not black_moves:
            return "red"

        return None