import time
import sys
import os
import json
from collections import defaultdict

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r4 import CR4V4R4

sleep_time = 0.01
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)
pll_ids = ["D", "C", "B", "A"]
LOs = [10000, 12000, 14000]
NUM_TESTS = 100

def reset_all_plls():
    for pll_id in pll_ids:
        cr4.reset_pll(pll_id)

def power_down_all_plls():
    for pll_id in pll_ids:
        cr4.power_off_pll(pll_id)

def tune_pll(pll_id, LO_freq_mhz):
    cr4.tune_pll(pll_id, LO_freq_mhz)
    time.sleep(sleep_time)
    is_locked = cr4.read_is_locked()
    return is_locked

def run_load_test():
    results = defaultdict(lambda: defaultdict(int))

    for test in range(NUM_TESTS):
        print(f"Running test {test + 1}/{NUM_TESTS}")
        reset_all_plls()

        for pll_id in pll_ids:
            LO_freq_mhz = 10000
            # Check to make sure it's not locked currently
            is_locked = driver.read_gpio_pin("PLL_MISO")
            if is_locked:
                print(f"Error: PLL {pll_id} is locked before tuning")
                reset_all_plls()
                continue

            # Tune the PLL
            success = tune_pll(pll_id, LO_freq_mhz)
            results[pll_id]["total_attempts"] += 1
            if success:
                results[pll_id]["successes"] += 1
            #    print(f"PLL {pll_id} {LO_freq_mhz} MHz locked")
            #else:
            #    print(f"PLL {pll_id} {LO_freq_mhz} MHz failed to lock")

            cr4.reset_pll(pll_id)

    return results

def calculate_success_rates(results):
    for pll_id in results:
        total_attempts = results[pll_id]["total_attempts"]
        successes = results[pll_id]["successes"]
        success_rate = (successes / total_attempts) * 100 if total_attempts > 0 else 0
        results[pll_id]["success_rate"] = round(success_rate, 2)

def save_results_to_json(results, filename="pll_load_test_results.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    print("Starting PLL load test...")
    results = run_load_test()
    calculate_success_rates(results)
    save_results_to_json(results)
    print("Load test completed.")