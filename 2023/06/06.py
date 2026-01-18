import sys, os
import re




def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


def parse_times_dists(lines):
    times_pattern = "Time: (( *\d+)+)"
    dist_pattern = "Distance: (( *\d+)+)"
    match_time = re.match(times_pattern, lines[0])
    match_dist = re.match(dist_pattern, lines[1])

    times = [int(t) for t in match_time.group(1).split(" ") if len(t) > 0] 
    distances = [int(d) for d in match_dist.group(1).split(" ") if len(d) > 0]
    print(times)
    print(distances)

    return times, distances


def compute_num_possible_wins(time_taken, dist_to_beat):
    wins = 0        
    # Hold for t seconds (accelerate to t mm/ms)
    for speed in range(1, time_taken):
        remaining_time = time_taken-speed
        dist_travelled = speed*remaining_time
        if (dist_travelled > dist_to_beat):
            wins += 1
    return wins




## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    times, distances = parse_times_dists(lines)

    product = 1

    for i in range(0, len(times)):
        product *= compute_num_possible_wins(times[i], distances[i])

    return product




## Solve Part Two
def part_two(fileaddr):
    lines = read_file(fileaddr)
    times, distances = parse_times_dists(lines)

    times = [str(t) for t in times]
    distances = [str(d) for d in distances]
    
    # Concatenate
    time = int("".join(times))
    dist = int("".join(distances))

    return compute_num_possible_wins(time, dist)










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
    
