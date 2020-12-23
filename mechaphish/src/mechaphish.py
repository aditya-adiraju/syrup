from drill import drill
import subprocess
import threading
import time 
import os
import errno
import logging
import coloredlogs
from io import StringIO

from config import logging_config
logging.config.dictConfig(logging_config)
log = logging.getLogger(__name__)

# spawns afl-fuzz and prints output
def spawn_afl(input_path, output_path, binary_path, mode, secondary_id = None):
    log = logging.getLogger("afl_master")
    cmd = ["afl-fuzz", "-i", input_path, "-o", output_path] 
    if mode == "QEMU":
        cmd.append("-Q")
    else:
        raise Exception("Not implemented")
    
    if secondary_id == None:
        cmd.append("-M")
        cmd.append("fuzz-master")
    else:
        cmd.append("-S")
        cmd.append(secondary_id)

    cmd.append(binary_path)
    log.info(f"Starting AFL with command: '{cmd}'")
    afl = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    if secondary_id != None:
        # wait without printing any output
        afl.wait() 

    line = ""
    for c in iter(lambda: afl.stdout.read(1), b''):
        try:
            c = c.decode()
            if c == "\n":
                log.info(line)
                line = ""
            else:
                line+= c
        except:
            pass
# Runs afl-fuzz in the selected mode, and checks for outputs
def afl_manager(binary_path, minimized_crashes_output_path, input_path, output_path, cores, mode = "QEMU"):
    afl_main_thread = threading.Thread(target=spawn_afl, args = [input_path, output_path, binary_path, mode])
    afl_main_thread.daemon = True
    afl_main_thread.start()

    afl_secondary_threads = []
    for i in range(cores - 1):
        s = threading.Thread(target=spawn_afl, args = [input_path, output_path, binary_path, mode, f"secondary-{i}"])
        s.daemon = True
        s.start()
        afl_secondary_threads.append(s)
    
    total_crashes = len(os.listdir(minimized_crashes_output_path)) + 1 # +1 because the afl crash folder has an extra readme file
    crash_folder = os.path.join(output_path, "fuzz-master", "crashes")
    while True:
        try:
            os.listdir(crash_folder)
            break
        except Exception:
            log.info("Waiting for crashes folder to exist")
            time.sleep(0.5)

    while True:
        # check for crashes
        log.info("Checking for crashes to minimize")
        crashes = os.listdir(crash_folder)
        if len(crashes) > total_crashes:
            for crash in crashes:
                if crash == "README.txt":
                    continue
                out_filename = os.path.join(minimized_crashes_output_path, f"crash-{total_crashes}-min")
                log.info(f"Minimizing crash {crash} to {out_filename}")
                tmin_cmd = ["afl-tmin", "-i", os.path.join(crash_folder, crash), "-o", out_filename, binary_path]
                subprocess.run(tmin_cmd)
                total_crashes += 1
        time.sleep(60)

def analyze(binary_path, input_path, output_path, cores = 4, use_llvm_lift = False, lifter = None, use_dyninst = False):
    phish_output_path = os.path.join(output_path, "mechaphish")
    min_crashes_path = os.path.join(phish_output_path, "crashes")
    # make folder for mechaphish to output its final results
    try:
        os.makedirs(phish_output_path)
        os.makedirs(min_crashes_path)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

    log.info(f"Starting analysis of {binary_path}")
    log.info("Starting")
    # start afl
    afl_thread = threading.Thread(target=afl_manager, args=[binary_path, min_crashes_path, input_path, output_path, cores])
    afl_thread.daemon = True
    afl_thread.start()

    # start driller
    drill_thread = threading.Thread(target=drill, args=[binary_path, output_path, cores])
    drill_thread.daemon = True
    drill_thread.start()

    # wait forever
    while True:
        time.sleep(10000)

if __name__ == "__main__":
    #analyze("./tests/tests/test", "./tests/mecha_in", "./tests/mecha_out")
    #analyze("./tests/emojidb_test/emojidb", "./tests/emojidb_test/input", "./tests/emojidb_test/output")
    #analyze("./tests/picoctf_tests/overflow_0/vuln", "./tests/mecha_in", "./tests/mecha_out")
    analyze("./tests/picoctf_tests/overflow_2/overflow_2", "./tests/picoctf_tests/overflow_2/input", "./tests/picoctf_tests/overflow_2/output")