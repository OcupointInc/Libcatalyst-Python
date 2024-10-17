import time
import logging
from collections import defaultdict
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5

sleep_time = 0.0005  # Reduced sleep time

# Initialize driver and device
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

pll_ids = ["D", "C", "B", "A"]
LO_freq_mhz = 11000
NUM_TESTS = 500

cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

# Set up logging to handle stdout and flush immediately
logger = logging.getLogger('pll_load_test')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.propagate = False  # Prevent duplicate logs

def reset_all_plls():
    for pll_id in pll_ids:
        cr4.pll_reset_enable(pll_id, 1)

def tune_pll(pll_id, LO_freq_mhz):
    cr4.tune_pll(pll_id, LO_freq_mhz)
    time.sleep(sleep_time)
    return cr4.read_is_locked()

def print_current_results(results, current_test, start_time):
    elapsed_time = time.time() - start_time
    output = ["__CLEAR_CONSOLE__"]  # Special marker to clear console
    output.append(f"Current Test: {current_test} / {NUM_TESTS}")
    output.append(f"Elapsed Time: {elapsed_time:.2f} seconds")
    output.append("\nCurrent PLL Success Rates:")
    output.append("---------------------------")
    for pll_id in pll_ids:
        total_attempts = results[pll_id]["total_attempts"]
        successes = results[pll_id]["successes"]
        success_rate = (successes / total_attempts) * 100 if total_attempts > 0 else 0
        output.append(f"PLL {pll_id}: {success_rate:.2f}% ({successes}/{total_attempts})")
    logger.info("\n".join(output))

def run_load_test():
    results = defaultdict(lambda: defaultdict(int))
    start_time = time.time()

    for i in range(NUM_TESTS):
        reset_all_plls()

        for pll_id in pll_ids:
            if driver.read_gpio_pin("PLL_MISO"):
                reset_all_plls()
                time.sleep(sleep_time)

            success = tune_pll(pll_id, LO_freq_mhz)
            results[pll_id]["total_attempts"] += 1
            if success:
                results[pll_id]["successes"] += 1

            reset_all_plls()

        # Update every 10 tests or on the last test
        if i % 10 == 0 or i == NUM_TESTS - 1:
            print_current_results(results, i + 1, start_time)

    return results

def print_final_results(results, total_time):
    output = ["__CLEAR_CONSOLE__"]  # Special marker to clear console
    output.append("\nFinal PLL Success Rates:")
    output.append("------------------------")
    for pll_id in pll_ids:
        total_attempts = results[pll_id]["total_attempts"]
        successes = results[pll_id]["successes"]
        success_rate = (successes / total_attempts) * 100 if total_attempts > 0 else 0
        output.append(f"PLL {pll_id}: {success_rate:.2f}% ({successes}/{total_attempts})")
    output.append(f"\nTotal execution time: {total_time:.2f} seconds")
    logger.info("\n".join(output))

if __name__ == "__main__":
    logger.info("Starting PLL load test...")
    start_time = time.time()
    results = run_load_test()
    total_time = time.time() - start_time
    print_final_results(results, total_time)
    logger.info("Load test completed.")
