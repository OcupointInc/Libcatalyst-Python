import time
import sys
import os
from collections import defaultdict

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r4 import CR4V4R4

sleep_time = 0.0005  # Reduced sleep time
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)
pll_ids = ["D", "C", "B", "A"]
LO_freq_mhz = 11000
NUM_TESTS = 500

cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

def reset_all_plls():
    for pll_id in pll_ids:
        cr4.pll_reset_enable(pll_id, 1)

def tune_pll(pll_id, LO_freq_mhz):
    cr4.tune_pll(pll_id, LO_freq_mhz)
    time.sleep(sleep_time)
    return cr4.read_is_locked()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_current_results(results, current_test, start_time):
    clear_console()
    elapsed_time = time.time() - start_time
    print(f"Current Test: {current_test} / {NUM_TESTS}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print("\nCurrent PLL Success Rates:")
    print("---------------------------")
    for pll_id in pll_ids:
        total_attempts = results[pll_id]["total_attempts"]
        successes = results[pll_id]["successes"]
        success_rate = (successes / total_attempts) * 100 if total_attempts > 0 else 0
        print(f"PLL {pll_id}: {success_rate:.2f}% ({successes}/{total_attempts})")

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

        if i % 5 == 0 or i == NUM_TESTS - 1:  # Update every 5 tests or on the last test
            print_current_results(results, i + 1, start_time)

    return results

def print_final_results(results, total_time):
    clear_console()
    print("\nFinal PLL Success Rates:")
    print("------------------------")
    for pll_id in pll_ids:
        total_attempts = results[pll_id]["total_attempts"]
        successes = results[pll_id]["successes"]
        success_rate = (successes / total_attempts) * 100 if total_attempts > 0 else 0
        print(f"PLL {pll_id}: {success_rate:.2f}% ({successes}/{total_attempts})")
    print(f"\nTotal execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    print("Starting PLL load test...")
    start_time = time.time()
    results = run_load_test()
    total_time = time.time() - start_time
    print_final_results(results, total_time)
    print("Load test completed.")