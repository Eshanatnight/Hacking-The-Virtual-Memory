#!/usr/bin/python3

'''
Locate and replace the first occurence of a string in the heap of a process.

Useage: ./read_write_heap.py <pid> <seach_string> <replacement_string>

- PID is the pid of the target process
- search_string is the ASCII string you are looking to overwrite
- replace_by_string is the ASCII string you want to replace search_string with
'''

import sys

def print_usage_and_exit():
    print(f"Usage: \'read_write_heap.py\' <pid> <search_string> <replace_by_string>")
    sys.exit(1)

def main():
    # if there are not enough arguments, print usage and exit
    if (len(sys.argv) != 4):
        print_usage_and_exit()

    # Get the pid from the first argument
    pid : int = int(sys.argv[1])

    # If incorrect pid, print usage and exit
    if (pid <= 0):
        print_usage_and_exit()

    search_string : str = str(sys.argv[2])

    # If empty search string, print usage and exit
    if (search_string == ""):
        print_usage_and_exit()

    write_string = str(sys.argv[3])

    # If empty write string or the search string, print usage and exit
    if (write_string == "" or search_string == ""):
        print_usage_and_exit()

    # Open the maps and mem files of the process
    maps_filename: str = f"/proc/{pid}/maps"
    print(f"[*] maps: {maps_filename}")

    mem_filename: str = f"/proc/{pid}/mem"
    print(f"[*] mem: {mem_filename}")


    # Try opening the maps file in read mode
    try:
        maps_file = open(maps_filename, "r")
    except IOError as e:
        print(f"[!] Error opening file: {maps_filename}")
        print(f"[!] IO Error: {e.errno} \t {e.strerror}")
        sys.exit(1) # exitout if error opening maps file


    for line in maps_file:

        sline = line.split(' ')

        # check if we found the heap
        if (sline[-1][:-1] != "[heap]"):
            continue

        # found heap
        print(f"[*] Found [heap]")

        # Now we parse the line
        addr     = sline[0]
        perm     = sline[1]
        offset   = sline[2]
        device   = sline[3]
        inode    = sline[4]
        pathname = sline[-1][:-1]

        print(f"\t Path Name   : {pathname}")
        print(f"\t Addresses   : {addr}")
        print(f"\t Permissions : {perm}")
        print(f"\t Offset      : {offset}")
        print(f"\t Inode      : {inode}")

        # Now we need to check if the permissions are correct
        if (perm[0] != 'r' or perm[1] != 'w'):
            print(f"[!] Error: {pathname} does not have the correct permissions")
            maps_file.close()
            sys.exit(1)

        # Now we need to split the address into the start and end
        addr = addr.split('-')
        if (len(addr) != 2):
            # Never should happen
            # But never trust anyone, not even your os!

            print(f"[!] Error: {pathname} does not have the correct address format")
            maps_file.close()
            sys.exit(1)

        addr_start = int(addr[0], 16)
        addr_end   = int(addr[1], 16)
        print(f"Start Address: [{addr_start :x}] End Address: [{addr_end :x}]")

        # Now we need to open the mem file in read/write mode
        try:
            mem_file = open(mem_filename, "rb+")
        except IOError as e:
            print(f"[!] Error opening file: {mem_filename}")
            print(f"[!] IO Error: {e.errno} \t {e.strerror}")
            maps_file.close()
            sys.exit(1) # exitout if error opening mem file

        # Read the Heap
        mem_file.seek(addr_start)
        heap = mem_file.read(addr_end - addr_start)

        # Now lest find the string
        try:
            i= heap.index(bytes(search_string, "ASCII"))

        except Exception:
            print(f"[!] Error: Could not find {search_string} in the heap")
            maps_file.close()
            mem_file.close()
            sys.exit(1)

        # If the string was found, we can now overwrite it
        print(f"[*] Found {search_string} at index {addr_start + i :x}")

        # Overwrite the string
        print(f"[*] Overwriting {search_string} with {write_string} at index {addr_start + i :x}")
        mem_file.seek(addr_start + i)
        mem_file.write(bytes(write_string, "ASCII"))

        # Close the files
        maps_file.close()
        mem_file.close()

        # Since we only have one heap, we can exit
        break




if __name__ == '__main__':
    main()