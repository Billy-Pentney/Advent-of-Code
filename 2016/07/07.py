
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    addresses = []
    for line in lines:
        i = 0
        ## outside square brackets 
        supernets = []
        ## Inside square brackets
        hypernets = []

        for j, ch in enumerate(line):
            if ch == '[':
                ## End of a supernet (start a new bracket)
                supernets.append(line[i:j])
                i = j+1
            elif ch == ']':
                ## End of a hypernet (bracketed)
                hypernets.append(line[i:j])
                i = j+1
            elif j == len(line)-1:
                ## if here, then not in square brackets, so must be supernet
                supernets.append(line[i:])

            j += 1

        addresses.append((supernets, hypernets))

    return addresses

def has_abba(code: str):
    """
    Checks if the given string contains an ABBA code. 
    This is a length-4 palindrome where the first and second letter are different.
    """
    for i in range(len(code)-3):
        ## First two characters
        pre = code[i:i+2]
        ## Last two characters reversed
        suff = code[i+3:i+1:-1]
        if code[i] != code[i+1] and pre == suff:
            ## Contains an ABBA code
            return True
        
    return False
    
def supports_ssl(supernet: list, hypernet: list) -> bool:
    """
    Checks if a given list of supernets and list of hypernets contains an ABA code.
    This must be a string of the form ABA in a supernet, where the equivalent BAB string is seen in a hypernet.
    Returns true if found, false otherwise.
    """
    potential_babs = []

    for code in supernet:
        for i in range(len(code)-2):
            ## ABA is 3 chars
            aba = code[i:i+3]
            if aba[0] != aba[2] or aba[0] == aba[1]:
                continue
            ## Reverse the ABA code
            bab = aba[1] + aba[0] + aba[1]
            potential_babs.append(bab)

    if len(potential_babs) == 0:
        return False
    
    for code in hypernet:
        if any([bab in code for bab in potential_babs]):
            ## Found aba in Supernet and bab in hypernet 
            return True

    return False


def count_tls_ips(addresses: list):
    num_hypernets = 0
    for supernets, hypernets in addresses:
        supernet_aba = any([has_abba(code) for code in supernets])
        no_hypernet_aba = not any([has_abba(code) for code in hypernets])
        if supernet_aba and no_hypernet_aba:
            print(f"{supernets} [{hypernets}] is valid")
            num_hypernets += 1

    return num_hypernets

def count_ssl_ips(addresses: list):
    num_hypernets = sum([
        supports_ssl(supernets, hypernets) 
        for supernets, hypernets in addresses
    ])
    return num_hypernets


from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    addresses = load(fname)
    # print(addresses)
    print("Part one:", count_tls_ips(addresses))
    print("Part two:", count_ssl_ips(addresses))
