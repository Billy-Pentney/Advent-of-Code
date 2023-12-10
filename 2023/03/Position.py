class Position:
    def __init__(self, row, start_col, end_col, val):
        self.row = row
        self.start_col = start_col
        self.end_col = end_col
        self.val = val

class Number(Position):
    def __repr__(self):
        return f"({self.val}, r={self.row}, c={self.start_col}-{self.end_col})"

class Symbol(Position):
    def __init__(self, row, col, val):
        self.row = row
        self.start_col = col
        self.end_col = col
        self.col = col
        self.val = val

    def __repr__(self):
        return f"({self.val}, r={self.row}, c={self.start_col})"

