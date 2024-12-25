
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        initial_nums = [int(row.strip("\n")) for row in file.readlines()]

    return np.array(initial_nums, dtype='int64')


def mix(num, secret_num):
    
    ## To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. 
    # #Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    
    return num ^ secret_num

    
def prune(num):
    ## To prune the secret number, calculate the value of the secret number modulo 16777216. 
    # Then, the secret number becomes the result of that operation. 
    return num % 16777216




def apply_round(secret_num):
    
    ## Multiply the secret number by 64. 
    # Then, mix this result into the secret number. 
    # Finally, prune the secret number.
    x = secret_num * 64
    x_m = mix(x, secret_num)
    x_mp = prune(x_m)

    ## Divide the secret number by 32 & round down to integer.
    # Then, mix this result into the secret number. 
    # Finally, prune the secret number.
    y = x_mp // 32
    y_m = mix(y, x_mp)
    y_mp = prune(y_m)

    ## Multiply the secret number by 2048. 
    # Then, mix this result into the secret number. 
    # Finally, prune the secret number.
    z = y_mp*2048
    z_m = mix(z, y_mp)
    z_mp = prune(z_m)

    return z_mp

    


def solve(nums, iters=2000):
    # Sums the total of the secret numbers after all iterations
    total_final_secrets = 0
    
    # Stores a dict for each sequence of price changes of length 4, to a dictionary mapping
    # the monkey i to the price by monkey i after that sequence is first observed in the secret numbers by monkey i.
    value_after_sequence = {}

    for monkey, num in enumerate(nums):
        secret_num = num

        # Store the sequence of price changes by this monkey
        price_changes = []
        prev_price = secret_num % 10

        for iter in range(iters):
            secret_num = apply_round(secret_num)

            price = int(secret_num % 10)
            price_diff = price - prev_price
            price_changes.append(price_diff)

            ## If we've seen at least 3 previous changes in price...
            if iter >= 3:
                ## Create a string describing the last 4 price changes e.g. "012-1"
                price_change_seq_str = "".join([str(h) for h in price_changes[-4:]])

                ## Store the value (price) at the end of this sequence for this monkey
                if price_change_seq_str in value_after_sequence.keys():
                    prices_after_seq = value_after_sequence[price_change_seq_str]
                    if monkey not in prices_after_seq.keys():
                        ## Only store the price if we haven't seen this sequence before for this monkey
                        value_after_sequence[price_change_seq_str][monkey] = price
                else:
                    ## Create a new dictionary to store the value of this sequence
                    value_after_sequence[price_change_seq_str] = {monkey: price}
        
            prev_price = price

        total_final_secrets += secret_num

    print(f"Simulated {iters} iterations!")

    ## Now, for each sequence, compute the profit, by summing across the four monkeys
    max_profit = 0
    print("Num of unique price-change sequences:", len(value_after_sequence))
    
    print("Computing maximum profit...")
    # Compute the profit of each unique sequence of 4 price changes
    for si, (seq, seq_prices) in enumerate(value_after_sequence.items()):
        profit = 0
        for monkey, price in seq_prices.items():
            profit += price

        if profit > max_profit:
            max_profit = int(profit)
            print(f"#{si+1} ({seq}) has profit {profit:.0f}")

    print()
    return total_final_secrets, int(max_profit)





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    secret_nums = load(fname)

    total_secrets, max_profit = solve(secret_nums, 2000)
    print(f"(Part 1) Total after Iterations: {total_secrets}")
    print(f"(Part 2) Max Profit: {max_profit}")
