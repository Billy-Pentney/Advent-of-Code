class Scratchcard:
    def __init__(self, id, win_nums, act_nums, count=1):
        self.id = id
        self.win_nums = sorted(win_nums)
        self.act_nums = sorted(act_nums)
        self.count = count

        # Get the count of numbers which were winners AND in the picked nums
        self.num_wins = 0

        for win_num in self.win_nums:
            if win_num in self.act_nums:
                # self.act_nums.remove(win_num)
                self.num_wins += 1

        self.score = 0
        if self.num_wins > 0:
            self.score = 2**(self.num_wins-1)

    # def get_num_wins(self):
    #     wins = set(self.act_nums).intersection(self.win_nums)
    #     return len(wins)
    
    def __repr__(self):
        return f"Card #{self.id}: {self.num_wins} wins, {self.score} score"