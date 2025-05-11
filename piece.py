class Piece:
    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        return f"<Piece {self.color[0].upper()}{'K' if self.king else ''} at ({self.row},{self.col})>"
