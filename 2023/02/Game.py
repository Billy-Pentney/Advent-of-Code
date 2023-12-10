import BoxColors

class Game:
    def __init__(self, id, cycles):
        self.id = id
        self.cycles = cycles
    
    def __str__(self):
        return f"Game #{self.id}: {self.cycles}"
    
    def is_possible(self, max_box_colors):
        for colors in self.cycles:
            if colors.exceeds(max_box_colors):
                return False
            
        return True

    def compute_power(self):
        req_colors = BoxColors(0,0,0)
        for cycle in self.cycles:
            req_colors.max_with(cycle)
        power = req_colors.power()
        # print(self, "has power:", power)
        return power

