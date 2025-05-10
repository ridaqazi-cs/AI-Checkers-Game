# piece.py

class Piece:
    def __init__(self, row, col, color, king=False):
        """
        row, col: integer board coordinates (0–7)
        color: "red" or "black"
        king: boolean, True if this piece is a king
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = king

    def make_king(self):
        """Promote this piece to a king."""
        self.king = True

    def __repr__(self):
        return f"<Piece {self.color[0].upper()}{'K' if self.king else ''} at ({self.row},{self.col})>"
