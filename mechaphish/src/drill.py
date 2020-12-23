import driller 
import time 
import os
import errno 
import logging
import coloredlogs

log = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=log)

logging.getLogger("angr").setLevel(logging.WARNING)
logging.getLogger("cle").setLevel(logging.ERROR)

def drill(binary_path, fuzzer_dir, cores):
    log.info("Starting driller")

    queue_dirs = [os.path.join(fuzzer_dir, "fuzz-master", "queue")]
    for i in range(cores - 1):
        # yes i know this is stupidly coupled with how afl_manager spawns the secondary afl workers, dont @ me
        queue_dirs.append(os.path.join(fuzzer_dir, f"secondary-{i}", "queue"))

    driller_output_dir = os.path.join(fuzzer_dir, "driller", "queue")

    try:
        os.makedirs(driller_output_dir)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

    drilled = set()
    outputted = set()
    for outputted_filename in os.listdir(driller_output_dir):
        with open(os.path.join(driller_output_dir, outputted_filename), 'rb') as out:
            outputted.add(out.read())
    
    bitmap = None
    while True:
        try:
            with open(os.path.join(fuzzer_dir, "fuzz-master", "fuzz_bitmap"), 'rb') as bitmap_file:
                bitmap = bitmap_file.read()
            break
        except Exception:
            time.sleep(0.5)
    
    # Define drill_seed closure
    def drill_seed(seed):
        log.info(f"Drilling input {seed}")
        for _, new_seed in driller.Driller(binary_path, seed, bitmap).drill_generator():
            if new_seed not in outputted:
                x = "{:06d}".format(len(outputted))
                name = f"id:{x},driller"
                log.info(f"Outputting new seed {new_seed} to {name}")
                outputted.add(new_seed)
                with open(os.path.join(driller_output_dir, name), 'wb') as dest_file:
                    dest_file.write(new_seed)

    while True:
        log.info(f"Starting driller: drilled = {len(drilled)} | outputted = {len(outputted)}")
        for queue_dir in queue_dirs:
            for seed_filename in os.listdir(queue_dir):
                full_path = os.path.join(queue_dir, seed_filename)
                if full_path in drilled or not seed_filename.startswith("id:"):
                    # log.info(f"Skipping {full_path}")
                    continue
                
                # log.info(f"Processing {full_path}")
                try:
                    with open(full_path, "rb") as seed_file:
                        drilled.add(full_path)
                        seed = seed_file.read()
                        drill_seed(seed)
                        drill_seed(seed + seed[:4])
                except Exception:
                    continue
        log.info(f"Driller is done: drilled = {len(drilled)} | outputted = {len(outputted)}")
        time.sleep(20)

# testing only
if __name__ == "__main__":
    fuzzer_dir = "./tests/outputs/"
    # drill("./tests/rebuilt")
    drill("./tests/test", fuzzer_dir, 4)