import sys, os
import re
from math import lcm

HIGH_PULSE = 1
LOW_PULSE = 0

module_pattern = "(\w+) -> (\w+(?:, \w+)*)"

class MyModule:
    def __init__(self, line):
        match = re.match(module_pattern, line)
        if match:
            self.name = match.group(1)
            self.output_modules = match.group(2).split(", ")
        self.input_names = []
        self.output_high = False
        self.high_pulse_times = []
        self.high_pulse_snapshots = []

    def has_outputted_high(self, times):
        return len(self.high_pulse_times) >= times

    def get_output(self):
        if self.output_high:
            return HIGH_PULSE
        return LOW_PULSE

    def __repr__(self):
        return f"Module {self.name} outputs: {self.output_modules}"

    def receive_pulse(self):
        pass


class Broadcaster(MyModule):
    def __init__(self, line):
        super().__init__(line)
    
    def receive_pulse(self, input_high):
        self.output_high = input_high

    def __repr__(self):
        return f"[{self.name} -> {self.output_modules}]"



## Flip-flop modules (prefix %)
class Flipflop(MyModule):
    def __init__(self, line):
        super().__init__(line)
        # Initially off
        self.output_high = False
    
    def receive_pulse(self, input_high, input_name=None, button_click_i=None):
        # On any LOW pulse, flip the state
        if not input_high:
            self.output_high = not self.output_high
            
    def __repr__(self):
        return f"[%{self.name} -> {self.output_modules}]"


## Conjunction modules (prefix &)
class Conjunc(MyModule):
    def __init__(self, line):
        super().__init__(line)
        self.inputs = {}
        # Sends low by default
        self.output_high = False

    def add_initial_input(self, input_name):
        self.inputs[input_name] = False

    def receive_pulse(self, input_high: bool, input_name: str, button_click_i=None):
        self.inputs[input_name] = input_high
        all_inputs_high = all(self.inputs.values())
        # Send LOW if all inputs are HIGH; or send HIGH otherwise
        self.output_high = not all_inputs_high

        if self.output_high and len(self.high_pulse_times) < 5:
            self.high_pulse_times.append(button_click_i)
            self.high_pulse_snapshots.append(self.inputs.copy())

        return self.output_high
    
    def __repr__(self):
        return f"[&{self.name} -> {self.output_modules}]"



class Controller:
    def __init__(self, modules):
        self.num_pulses = { LOW_PULSE: 0, HIGH_PULSE: 0 }
        self.modules = modules

        self.modules['button'] = MyModule("button -> broadcaster")

        ## Initialise the inputs for the Conjunction modules
        for name, module in self.modules.items():
            for next_name in module.output_modules:
                # All conjunction modules should have their inputs initialised as LOW
                if next_name in self.modules.keys() and isinstance(self.modules[next_name], Conjunc):
                    self.modules[next_name].add_initial_input(input_name=name)


    def find_module(self, mod_name):
        if mod_name in self.modules.keys():
            return self.modules[mod_name]
        return None
    
    def find_inputs_to(self, mod_name):
        inputs = []
        for name, module in self.modules.items():
            if mod_name in module.output_modules:
                inputs.append(module)
        return inputs

    def simulate_button_clicks(self, num_clicks):
        for i in range(0, num_clicks):
            self.push_button(i)


    def push_button(self, click_num):
        next_actions = ['button']
        actions = []

        while len(next_actions) > 0:
            actions = next_actions
            next_actions = []

            for mod_name in actions:
                module = self.modules[mod_name]
                output_pulse = module.get_output()
                output_high = module.output_high

                for next_mod_name in module.output_modules:
                    self.num_pulses[output_pulse] += 1

                    # pulse = ['low', 'high'][output_pulse]
                    # print(f" >> {mod_name} -{pulse}-> {next_mod_name}")

                    next_mod = self.find_module(next_mod_name)
                    
                    if next_mod is None:
                        continue

                    if isinstance(next_mod, Conjunc):
                        next_mod.receive_pulse(output_high, mod_name, click_num)
                        next_actions.append(next_mod_name)

                    elif isinstance(next_mod, Flipflop):
                        if output_pulse == LOW_PULSE:
                            next_mod.receive_pulse(output_high, mod_name, click_num)
                            next_actions.append(next_mod_name)

                    else:
                        next_actions.append(next_mod_name)


    def steps_till_modules_high(self, target_modules):
        i = 0
        # Run until we've seen *each* of the given modules output a high pulse twice
        while not all([tm.has_outputted_high(2) for tm in target_modules]):
            self.push_button(i)
            i += 1

        high_pulses_at = [tm.high_pulse_times for tm in target_modules]
        # high_pulses_ss = [tm.high_pulse_snapshots for tm in target_modules]

        cycle_lens = [hp[1] - hp[0] for hp in high_pulses_at]
        print(high_pulses_at)

        def calc_diffs(list):
            diffs = []
            for i in range(1, len(list)):
                diffs.append(list[i]- list[i-1])
            return diffs 

        diffs = [calc_diffs(l) for l in high_pulses_at]
        print(diffs)

        # print(high_pulses_ss)
        print(cycle_lens)
        lcm_len = lcm(*cycle_lens)
        # print("Lcm:",lcm_len)
        # max_start = max([hp[0] for hp in high_pulses_at])
        
        # return max_start + lcm_len
        return lcm_len

            



def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]




def make_module_controller(fileaddr):
    lines = read_file(fileaddr)
    module_dict = {}

    for line in lines:
        if line.startswith('broadcaster'):
            broadcaster = Broadcaster(line)
            module_dict['broadcaster'] = broadcaster
        elif line.startswith('%'):
            flipflop = Flipflop(line[1:])
            module_dict[flipflop.name] = flipflop
        elif line.startswith('&'):
            conjunc = Conjunc(line[1:])
            module_dict[conjunc.name] = conjunc

    return Controller(module_dict)



def part_one(fileaddr):
    controller = make_module_controller(fileaddr)
    button_clicks = 1000
    controller.simulate_button_clicks(button_clicks)
    num_pulses = controller.num_pulses        
    print(f"Low: {num_pulses[LOW_PULSE]}, High: {num_pulses[HIGH_PULSE]}")
    return num_pulses[LOW_PULSE] * num_pulses[HIGH_PULSE]




def part_two(fileaddr):
    controller = make_module_controller(fileaddr)
    target = "rx"
    inputs_to_target = controller.find_inputs_to(target)

    if len(inputs_to_target) != 1:
        print(f"Unexpected number of inputs to module {target}")
        return None
    
    predecessor_of_target = inputs_to_target[0]
    conjunc_inputs = controller.find_inputs_to(predecessor_of_target.name)

    print(conjunc_inputs)
    return controller.steps_till_modules_high(conjunc_inputs)





if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if part == '1':
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
