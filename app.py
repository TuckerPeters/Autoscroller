import time
import pyautogui
import random
import math

def prompt_for_mouse_position(prompt_text):
    input(f"{prompt_text}\nPress ENTER when ready...")
    return pyautogui.position()

def capture_manual_region():
    """
    1) Asks user for the TOP-LEFT corner of the region.
    2) Asks user for the BOTTOM-RIGHT corner of the region.
    3) Returns (left, top, width, height).
    """
    top_left = prompt_for_mouse_position("Move mouse to the TOP-LEFT corner of the region.")
    bottom_right = prompt_for_mouse_position("Move mouse to the BOTTOM-RIGHT corner of the region.")

    left = min(top_left[0], bottom_right[0])
    top = min(top_left[1], bottom_right[1])
    width = abs(bottom_right[0] - top_left[0])
    height = abs(bottom_right[1] - top_left[1])

    print(f"[INFO] Region selected: left={left}, top={top}, width={width}, height={height}")
    return (left, top, width, height)

def move_mouse_to_center(region):
    left, top, width, height = region
    cx = left + width // 2
    cy = top + height // 2
    print(f"[INFO] Moving mouse to center: ({cx}, {cy})")
    pyautogui.moveTo(cx, cy, duration=0.3)

def ultra_fast_scroll(pixels_to_scroll: float, desired_speed_pps=2100):
    """
    Bulk scroll approach aiming for ~2000px/s or faster.
    We do big chunks in rapid succession with minimal or no sleep.
    """
    base_click_size = 1.0  # On macOS, each scroll(-1) is 1 'click' in PyAutoGUI
    total_clicks_needed = pixels_to_scroll / base_click_size

    chunk_clicks = 15
    total_chunks = math.ceil(total_clicks_needed / chunk_clicks)
    time_needed = pixels_to_scroll / desired_speed_pps

    if time_needed < 0.05:
        time_needed = 0.05

    chunk_delay = time_needed / total_chunks

    print(f"[ULTRA] Trying to scroll ~{pixels_to_scroll:.0f} px at ~{desired_speed_pps} px/s, "
          f"total_chunks={total_chunks}, chunk_delay={chunk_delay:.4f}s")

    start_t = time.time()
    scrolled_clicks = 0
    for _ in range(total_chunks):
        pyautogui.scroll(-chunk_clicks)  # negative => downward
        scrolled_clicks += chunk_clicks
        if chunk_delay > 0:
            time.sleep(chunk_delay)

    scrolled_px = scrolled_clicks * base_click_size
    end_t = time.time()
    elapsed = end_t - start_t

    print(f"[ULTRA] Actually scrolled ~{scrolled_px:.0f}px in {elapsed:.2f}s "
          f"(~{scrolled_px/elapsed:.0f} px/s)\n")

def scroll_one_page_ultra(region, coverage=0.95):
    """
    Ultra approach. coverage is fraction of region height scrolled each iteration.
    Multiply by 2.0 to scroll further than just coverage% of region.
    """
    left, top, width, height = region
    pixels_to_scroll = coverage * height * 2.0  # 2x region for bigger jumps

    ultra_fast_scroll(
        pixels_to_scroll=pixels_to_scroll,
        desired_speed_pps=2000
    )

def start_ultra_scroll_loop(region):
    """
    1) Moves mouse to region center
    2) Infinite loop with ultra scrolling, random waits
    """
    move_mouse_to_center(region)

    while True:
        coverage = 0.95
        # 15% chance partial coverage
        if random.random() < 0.15:
            coverage = random.uniform(0.5, 0.9)

        scroll_one_page_ultra(region, coverage=coverage)

        wait_time = random.uniform(3.0, 8.0)
        print(f"[INFO] Next scroll in ~{wait_time:.1f}s\n")
        time.sleep(wait_time)

def main():
    # 1) Capture region
    region = capture_manual_region()

    # 2) Wait 10 seconds before starting
    print("[INFO] Waiting 10 seconds before starting the ultra scrolling...")
    time.sleep(10)

    # 3) Start infinite ultra scrolling
    start_ultra_scroll_loop(region)

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    try:
        main()
    except pyautogui.FailSafeException:
        print("[FAILSAFE] Mouse moved to top-left corner. Exiting.")
    except KeyboardInterrupt:
        print("[KEYBOARD INTERRUPT] Exiting.")
    finally:
        print("[INFO] Done.")
