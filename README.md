# Hacking the Virtual Memory

Run the Program First in a different terminal
In a seperate Terminal Instance run this script

```terminal
    ps aux | grep ./loop | grep -v grep
```

The output of the above command will be like this

```terminal
    kellsat+   465  0.0  0.0   2496   524 pts/1    S+   01:17   0:00 ./build/loop
```
the 465 in the 2nd Column is the PID of the process
Now Locate to the proc folder

```teminal
    cd /proc
```

run the following command in the terminal to list all the folders

```terminal
    ls -la
```

You will find a folder with the process id that we found earlier
In my case it is 465. cd into that folder.

Now we need the Heap Memory Address Information.

so we will run the following command

```terminal
    cat maps
```

---

## Output is like this

```terminal
    5651abe96000-5651abe97000 r--p 00000000 00:42 6192449487973722           /mnt/c/Dev/Virtual Memory Hacks/build/loop
    5651abe97000-5651abe98000 r-xp 00001000 00:42 6192449487973722           /mnt/c/Dev/Virtual Memory Hacks/build/loop
    5651abe98000-5651abe99000 r--p 00002000 00:42 6192449487973722           /mnt/c/Dev/Virtual Memory Hacks/build/loop
    5651abe99000-5651abe9a000 r--p 00002000 00:42 6192449487973722           /mnt/c/Dev/Virtual Memory Hacks/build/loop
    5651abe9a000-5651abe9b000 rw-p 00003000 00:42 6192449487973722           /mnt/c/Dev/Virtual Memory Hacks/build/loop
    5651ac9a3000-5651ac9c4000 rw-p 00000000 00:00 0                          [heap]
    7fb12f114000-7fb12f139000 r--p 00000000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f139000-7fb12f2b1000 r-xp 00025000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f2b1000-7fb12f2fb000 r--p 0019d000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f2fb000-7fb12f2fc000 ---p 001e7000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f2fc000-7fb12f2ff000 r--p 001e7000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f2ff000-7fb12f302000 rw-p 001ea000 08:20 37092                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fb12f302000-7fb12f308000 rw-p 00000000 00:00 0
    7fb12f315000-7fb12f316000 r--p 00000000 08:20 21193                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fb12f316000-7fb12f339000 r-xp 00001000 08:20 21193                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fb12f339000-7fb12f341000 r--p 00024000 08:20 21193                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fb12f342000-7fb12f343000 r--p 0002c000 08:20 21193                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fb12f343000-7fb12f344000 rw-p 0002d000 08:20 21193                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fb12f344000-7fb12f345000 rw-p 00000000 00:00 0
    7ffcaf015000-7ffcaf037000 rw-p 00000000 00:00 0                          [stack]
    7ffcaf122000-7ffcaf126000 r--p 00000000 00:00 0                          [vvar]
    7ffcaf126000-7ffcaf127000 r-xp 00000000 00:00 0                          [vdso]
```

Using the maps file, we can find all the information we need to locate our string:

```teminal
    5651ac9a3000-5651ac9c4000 rw-p 00000000 00:00 0                          [heap]
```

The heap:

- Starts at address 0x010ff000 in the virtual memory of the process
- Ends at memory address: 0x01120000
- Is readable and writable (rw)

A quick look back to our (still running) loop program we would se there will be the address in the heap.