import sys, os
import re

HIGH_PULSE = 1
LOW_PULSE = 0

module_pattern = "(\w+) -> (\w+(?:, \w+)*)"

class MyModule:
    def __init__(self, line):
        match = re.match(module_pattern, line)
        if match:
            self.name = match.group(1)
            self.output_modules = match.group(2).split(", ")
        self.state = LOW_PULSE

    def get_output(self):
        return self.state

    def __repr__(self):
        return f"Module {self.name} outputs: {self.output_modules}"


## Flip-flop modules (prefix %)
class Flipflop(MyModule):
    def __init__(self, line):
        super().__init__(line)
        # Initially off
        self.state = LOW_PULSE

    def get_output(self):
        return self.state
    
    def flipstate(self):
        self.state = HIGH_PULSE - self.state
            


## Conjunction modules (prefix &)
class Conjunc(MyModule):
    def __init__(self, line):
        super().__init__(line)
        self.high_inputs = set()
        self.low_inputs = set()
        # Sends high by default
        self.state = HIGH_PULSE

    def set_input_pulse(self, input_name: str, pulse: int):
        before_state = self.state
        if pulse == LOW_PULSE:
            self.low_inputs.add(input_name)
            self.high_inputs.discard(input_name)
        else:
            self.high_inputs.add(input_name)
            self.low_inputs.discard(input_name)
            
        after_state = self.get_output()
        if after_state != before_state:
            return after_state
        

    def get_output(self):
        if len(self.low_inputs) == 0:
            # All inputs are high, so the module is low
            self.state = LOW_PULSE
        else:
            # At least one input is low, so the module is high
            self.state = HIGH_PULSE

        return self.state

def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]


def take_snapshot(module_dict):
    snapshot = {}
    for name, module in module_dict.items():
        snapshot[name] = module.state
    return snapshot



## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    module_dict = {}

    for line in lines:
        if line.startswith('broadcaster'):
            broadcaster = MyModule(line)
            module_dict['broadcaster'] = broadcaster
        elif line.startswith('%'):
            flipflop = Flipflop(line[1:])
            module_dict[flipflop.name] = flipflop
        elif line.startswith('&'):
            conjunc = Conjunc(line[1:])
            module_dict[conjunc.name] = conjunc

    # print(module_dict)

    num_pulses = [0,0]

    button_clicks = 2

    iters = 0
    machine_snapshots = [take_snapshot(module_dict)]

    for i in range(0, button_clicks):
        print("i:",i)
        next_actions = ['broadcaster']
        num_pulses[LOW_PULSE] += 1

        while len(next_actions) > 0:
            actions = next_actions
            next_actions = []

            for mod_name in actions:
                module = module_dict[mod_name]
                output_pulse = module.get_output()

                ## TO FIX - Doesn't give correct num of High pulses for Test 2

                for next_mod_name in module.output_modules:
                    num_pulses[output_pulse] += 1

                    if next_mod_name not in module_dict.keys():
                        continue

                    next_mod = module_dict[next_mod_name]

                    if isinstance(next_mod, Conjunc):
                        new_mod_state = next_mod.set_input_pulse(mod_name, output_pulse)
                        if new_mod_state is not None:
                            next_actions.append(next_mod_name)

                    elif isinstance(next_mod, Flipflop):
                        if output_pulse == LOW_PULSE:
                            next_mod.flipstate()
                            next_actions.append(next_mod_name)
                    
                    pulse = ['low', 'high'][output_pulse]
                    print(f" >> {mod_name} -{pulse}-> {next_mod_name}")

                                    
        # print(f"i:{i}, highs: {num_pulses[HIGH_PULSE]}, lows: {num_pulses[LOW_PULSE]}")

        # snapshot = take_snapshot(module_dict)
        # for si, old_snapshot in enumerate(machine_snapshots):
        #     if old_snapshot == snapshot:
        #         # Loop found
        #         loop_len = i+1 - si
        #         print(f"!! loop after {si} clicks")
        #         num_loops = button_clicks / loop_len
        #         num_pulses[HIGH_PULSE] *= num_loops
        #         num_pulses[LOW_PULSE] *= num_loops
        #         return num_pulses[HIGH_PULSE] * num_pulses[LOW_PULSE]
            
        # machine_snapshots.append(snapshot)

    print(num_pulses)
    return num_pulses[LOW_PULSE] * num_pulses[HIGH_PULSE]


## Solve Part Two
def part_two(fileaddr):
    return










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
    
