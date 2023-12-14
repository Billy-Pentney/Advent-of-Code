import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


class Reindeer:

    def __init__(self, name, move_speed, move_time, rest_time):
        self.name = name
        self.move_speed = int(move_speed)
        self.move_time = int(move_time)
        self.rest_time = int(rest_time)
        self.distance = 0
        self.moving_for = 0
        self.resting_for = 0
        self.points = 0

    def __repr__(self):
        return f"\'{self.name}\':".ljust(15) + f"{self.move_speed} km/s for {self.move_time} secs, then 0km/s for {self.rest_time} secs"
    
    def calc_distance_at_time(self, t):
        # After t seconds

        # At the end of the cycle, the reindeer can move again
        cycle_time = self.move_time + self.rest_time

        remainder = t % cycle_time
        time_with_cycles = t - remainder
        num_cycles = time_with_cycles / cycle_time

        dist = num_cycles * self.move_speed * self.move_time

        # The remaining time is spent moving
        dist += self.move_speed * min(self.move_time, remainder)            

        return dist

    def add_point(self):
        self.points+=1

    def increment_distance(self):
        if self.moving_for < self.move_time:
            # Move
            self.distance += self.move_speed
            self.moving_for += 1
        else:
            # Cannot move
            if self.resting_for < self.rest_time:
                # Rest
                self.resting_for += 1

            if self.resting_for == self.rest_time:
                self.moving_for = 0
                self.resting_for = 0

        return self.distance






# Name: Speed (km/s), Move Time (s), Rest Time (s)
pattern = "(\w+): (\d+) km/s, (\d+), (\d+)"

def parse_reindeer(lines):
    reindeer = []
    for line in lines:
        match = re.match(pattern, line)
        if (match):
            name = match.group(1)
            speed = match.group(2)
            move_time = match.group(3)
            rest_time = match.group(4)
            reindeer.append(Reindeer(name, speed, move_time, rest_time))

    return reindeer



## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    reindeer = parse_reindeer(lines)
    print(reindeer)

    finish_time = 1000

    winner = None
    winner_dist = 0
    for deer in reindeer:
        dist = deer.calc_distance_at_time(finish_time)
        if winner is None or dist > winner_dist:
            winner = deer
            winner_dist = dist

    # print("Winner:", winner)
    return winner_dist


## Solve Part Two
def part_two(fileaddr):
    lines = read_file(fileaddr)
    reindeer = parse_reindeer(lines)
    print(reindeer)

    finish_time = 2503

    for t in range(1, finish_time+1):
        max_dist = 0
        win_deer = []
        dists = []
        for deer in reindeer:
            dist = deer.increment_distance()
            dists.append(dist)
            if dist > max_dist:
                win_deer = [deer]
                max_dist = dist
            elif dist == max_dist:
                win_deer.append(deer)

        print(dists)

        # Distribute points for this distance
        for deer in win_deer:
            deer.add_point()

    # Find the reindeer which earned the most points
    max_pts = 0
    win_deer = None
    for deer in reindeer:
        print(deer, "has points", deer.points)
        if deer.points > max_pts:
            max_pts = deer.points
            win_deer = deer

    # print("Winner:", winner)
    return max_pts










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
