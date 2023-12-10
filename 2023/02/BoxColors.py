class BoxColors:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __repr__(self):
        return f"({self.r}R, {self.g}G, {self.b}B)"
    
    def exceeds(self, other):
        return self.r > other.r or self.g > other.g or self.b > other.b
    
    def max_with(self, other):
        self.r = max(self.r, other.r)
        self.g = max(self.g, other.g)
        self.b = max(self.b, other.b)

    def power(self):
        return self.r * self.g * self.b

