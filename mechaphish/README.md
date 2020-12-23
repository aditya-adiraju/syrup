mechaphish
---

[Mechaphish](https://shellphish.net/cgc/) is team shellphish's submission to the DARPA Cyber Grand Challenge, a multi-year competition to design systems to automate the discovery and patching of bugs. They placed 3rd in the competition and later open-sourced the entire system.

Many parts of mechaphish were designed with the CGC binaries in mind, not our normal x86 binaries, so using some parts of their system may be impossible

There are also some interesting components that would make the fuzzing approach more feasible in CTFs, namely speeding up the fuzzing process

Here's the ultimate goal, given a binary from a competition and some sample inputs:
1. Decompile to llvm (using a tool like mcsema or llvm-mctoll or something different)
2. Recompile to x86 using afl-cc to instrument
3. Run the afl++ fuzzer
4. Run the mechaphish [driller](https://github.com/shellphish/driller) alongside the fuzzer to augment it with symbolic execution
5. Once the binary has crashed, use [Rex](https://github.com/angr/rex) or [angrop](https://github.com/angr/angrop) to generate an exploit

What currently works:
- `mechaphish.py` starts and manages a number of afl qemu instances, and starts a driller thread
    - The augmented fuzzing does help afl along when it gets stuck, though the feedback loop between afl and driller can be painfully slow sometimes
- The `dockerfile` starts with the afl++ container and adds the driller dependencies
- `llvm-mctoll` works to some extent in local testing, though it requires a header file and often crashes/generates invalid llvm (it made a llvm file that hung clang once)

What doesn't work:
- `Rex` doesnt seem to want to work, often failing when trying to load the binary, which may have to do with the tool being designed with CGC DECREE binaries in mind
- `afl-dyninst` doesn't even want to compile, though it seems like a promising solution

Other ideas:
1. Using something like [afl-dyninst](https://github.com/vanhauser-thc/afl-dyninst) to insert instrumentation
2. Experimenting with other afl like fuzzers
3. Lifting to llvm and then fuzzing directly with libFuzzer for even more speed [link](https://github.com/lifting-bits/mcsema/blob/master/docs/UsingLibFuzzer.md)
4. Using components from other CGC systems ([grr](https://github.com/lifting-bits/grr) and [pysememu](https://github.com/feliam/pysymemu))