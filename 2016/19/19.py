
def load(fname):
    with open(fname, "r") as file:
        num_elves = int(file.readlines()[0].strip("\n"))
    return num_elves

def compute_present_stealing(num_elves):
    """
    Solves Part 1 by playing the game with each elf stealing from its left neighbour.
    Returns the index (from 1 to n) of the last remaining elf.
    """

    elves_with_presents = list(range(num_elves))

    while len(elves_with_presents) > 1:
        # print(f"New round with {len(elves_with_presents)} elves!")
        n_elves_with_presents = len(elves_with_presents)

        ## Store a list of all elves removed from the game (for efficient removal)
        elves_stolen_from = set()

        ## Compare adjacent pairs, with elf i stealing from elf i+1
        for i in range(0,n_elves_with_presents,2):
            victim = elves_with_presents[(i+1) % n_elves_with_presents]
            elves_stolen_from.add(victim)

        ## Find the elves who DIDN'T have their presents stolen
        new_elves_with_presents = set(elves_with_presents).difference(elves_stolen_from)
        ## Now sort the elves so we visit them in order
        elves_with_presents = sorted(list(new_elves_with_presents))

    return elves_with_presents[0]+1


class ElfNode():
    """
    A single Linked-List node, which stores the next elf node in the circle. 
    """
    def __init__(self, elf_num: int, next=None):
        self.elf_num = elf_num
        self.next = next
        
    def to_string(self, n_nodes):
        s = f"{self.elf_num+1}"
        if self.next and n_nodes > 1:
            s += f"-{self.next.to_string(n_nodes-1)}"
        return s
    

def compute_present_stealing_opposite(num_elves):
    """
    Solves Part 2 by playing the game with each elf stealing from its neighbour on the opposite side of the circle.
    For a given elf, its opposite is the elf which is furthest away, with ties broken in favour of the lower-numbered elf.
    Returns the index (from 1 to n) of the last remaining elf.
    """

    ## Construct a singly-linked list with one node for each elf
    head = ElfNode(0)
    curr = head
    for i in range(1, num_elves):
        curr.next = ElfNode(i)
        curr = curr.next
    ## Make the linked-list circular
    curr.next = head

    num_elves_remaining = num_elves

    ## Compare pairs on opposite sides of the circle
    ## Note: we now remove elves in real time
    circle_width = num_elves_remaining // 2

    ## Start a traversal with two pointers, one at the start of the list and one halfway through
    thief = head
    victim_predecessor = head
    ## Step forward half of the number of nodes in the circle
    for i in range(circle_width-1):
        victim_predecessor = victim_predecessor.next

    ## Repeat until there's only one elf left
    while thief != victim_predecessor.next:
        victim = victim_predecessor.next
        ## Drop the victim (had presents stolen)
        victim_predecessor.next = victim.next
        num_elves_remaining -= 1
        ## It's the next elf's turn to steal
        thief = thief.next
        ## Every other turn, we increment the opposite pointer
        if num_elves_remaining % 2 == 0:
            victim_predecessor = victim_predecessor.next

    return thief.elf_num + 1

    



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    num_elves = load(fname)

    winner_p1 = compute_present_stealing(num_elves)
    print("Part one:", winner_p1)    
    winner_p2 = compute_present_stealing_opposite(num_elves)
    print("Part two:", winner_p2)