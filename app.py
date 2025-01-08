import time
import pyautogui
import random
import math

def prompt_for_mouse_position(prompt_text):
    """
    Pauses execution, shows a prompt in the terminal,
    and waits for you to press ENTER. 
    Returns the mouse's (x, y) position at that moment.
    """
    input(f"{prompt_text}\nPress ENTER when ready...")
    return pyautogui.position()

def capture_manual_region():
    """
    1) Asks user for top-left corner of the region.
    2) Asks user for bottom-right corner of the region.
    3) Returns (left, top, width, height).
    """
    top_left = prompt_for_mouse_position("Move your mouse to the TOP-LEFT corner of the region.")
    bottom_right = prompt_for_mouse_position("Move your mouse to the BOTTOM-RIGHT corner of the region.")

    left = min(top_left[0], bottom_right[0])
    top = min(top_left[1], bottom_right[1])
    width = abs(bottom_right[0] - top_left[0])
    height = abs(bottom_right[1] - top_left[1])

    print(f"[INFO] Selected region: left={left}, top={top}, width={width}, height={height}")
    return (left, top, width, height)

def move_mouse_to_center(region):
    """
    Moves the mouse to the center of the given region tuple: (left, top, width, height).
    """
    left, top, width, height = region
    center_x = left + width // 2
    center_y = top + height // 2
    print(f"[INFO] Moving mouse to center: ({center_x}, {center_y})")
    pyautogui.moveTo(center_x, center_y, duration=0.3)

def random_pause_long(chance=0.2, min_pause=2.0, max_pause=5.0):
    """
    With probability `chance`, pause for a random duration [min_pause, max_pause].
    Emulates a user looking away or pausing significantly.
    """
    if random.random() < chance:
        pause_time = random.uniform(min_pause, max_pause)
        print(f"[HUMAN] Long random pause: {pause_time:.2f}s")
        time.sleep(pause_time)

def random_pause_short(chance=0.3, min_pause=0.3, max_pause=1.2):
    """
    With probability `chance`, pause for a random short duration [min_pause, max_pause].
    This emulates slight hesitations mid-scroll.
    """
    if random.random() < chance:
        pause_time = random.uniform(min_pause, max_pause)
        print(f"[HUMAN] Short random pause: {pause_time:.2f}s")
        time.sleep(pause_time)

def humanlike_scroll(
    pixels_to_scroll: float,
    base_click_size: float = 120.0,
    min_increments: int = 25,
    max_increments: int = 70,
    short_pause_chance=0.3,
    long_pause_chance=0.1
):
    """
    Perform a single "human-like" scroll that covers `pixels_to_scroll` px total.
    
    - Uses a "slow start, speed up, slow down" pattern via a cosine wave.
    - Number of increments is random between min_increments and max_increments.
    - Each increment has its own random sub-step time (so speeds vary).
    - Mid-scroll random short pauses happen, plus a small chance for a longer pause.
    - total scroll duration is randomly chosen between ~0.3s to ~3s.
    """

    # random number of increments
    increments = random.randint(min_increments, max_increments)
    
    # random total time for this entire scroll
    total_time = random.uniform(0.3, 3.0)

    # We'll generate a half-cosine wave from t=0..1
    # speed(t) = 0.5 * (1 - cos(pi * t)), which goes from 0..1
    # Then we multiply it by total_clicks_needed to see how many clicks to do at each step.

    def speed_function(t):
        return 0.5 * (1 - math.cos(math.pi * t))

    # total number of "clicks" we need
    total_clicks_needed = pixels_to_scroll / base_click_size

    # Precompute the speed array so we can see how we ramp up and down
    speeds = []
    for i in range(increments + 1):
        t_i = i / increments
        speeds.append(speed_function(t_i))

    clicks_done = 0.0

    print(f"[HUMAN] Starting a ~{pixels_to_scroll:.0f}px scroll over ~{total_time:.2f}s "
          f"in {increments} increments. (Clicks needed ~{total_clicks_needed:.2f})")

    for i in range(1, increments + 1):
        # fraction of total in this step
        fraction_step = speeds[i] - speeds[i-1]
        step_clicks = fraction_step * total_clicks_needed
        
        # We'll randomize how we round
        # slightly to avoid consistent rounding patterns
        if random.random() < 0.5:
            actual_clicks = int(math.floor(step_clicks))
        else:
            actual_clicks = int(math.ceil(step_clicks))

        # each sub-step is negative => scroll down
        for _ in range(actual_clicks):
            pyautogui.scroll(-1)

        # vary the sub-step duration to add inconsistency
        # total_time / increments is average, multiply by random factor
        step_duration = (total_time / increments) * random.uniform(0.5, 1.5)
        time.sleep(step_duration)

        clicks_done += actual_clicks
        
        # random short mid-scroll pause
        random_pause_short(chance=short_pause_chance, min_pause=0.3, max_pause=1.0)
        
        # random chance for a longer pause
        random_pause_long(chance=long_pause_chance, min_pause=2.0, max_pause=5.0)

    print(f"[HUMAN] Finished sub-scroll. Estimated scrolled ~{clicks_done * base_click_size:.0f}px")

def scroll_to_new_page(
    region,
    coverage=0.95,
    scale=1.0
):
    """
    1) Calculate total pixels to scroll to move ~95% of the region (times scale).
    2) Scroll that distance using the "humanlike_scroll" function, 
       with random speed variations and pauses.
    """
    region_height = region[3]
    # ~95% of the region, scaled
    pixels_to_scroll = coverage * region_height * scale  

    print(f"[INFO] Target scroll: {pixels_to_scroll:.1f} px (coverage={coverage}, scale={scale})")
    humanlike_scroll(pixels_to_scroll=pixels_to_scroll)

def main():
    # 1) Prompt for region
    region = capture_manual_region()
    move_mouse_to_center(region)

    # 2) Prompt for scale
    scale_str = input("Enter a scroll scale factor (e.g. 1, 10, 100): ")
    try:
        scroll_scale = float(scale_str)
    except ValueError:
        scroll_scale = 1.0

    print("[INFO] Starting infinite, heavily humanized scrolling loop...")

    while True:
        coverage = 0.95
        # Small chance to do partial scroll
        if random.random() < 0.15:
            coverage = random.uniform(0.5, 0.9)

        scroll_to_new_page(region, coverage=coverage, scale=scroll_scale)

        # after finishing the scroll, a random "looking around" wait
        # from maybe 3 to 8 seconds
        wait_time = random.uniform(3.0, 8.0)
        print(f"[INFO] Next scroll in ~{wait_time:.1f}s.\n")
        time.sleep(wait_time)

if __name__ == "__main__":
    # FAILSAFE: move mouse to top-left corner of screen to raise an exception.
    pyautogui.FAILSAFE = True

    try:
        main()
    except pyautogui.FailSafeException:
        print("[FAILSAFE] Mouse moved to top-left corner. Exiting.")
    except KeyboardInterrupt:
        print("[KEYBOARD INTERRUPT] Exiting script.")
    finally:
        print("[INFO] Done.")
