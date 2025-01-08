import time
import pyautogui
import random
import math

def prompt_for_mouse_position(prompt_text):
    input(f"{prompt_text}\nPress ENTER when ready...")
    return pyautogui.position()

def capture_manual_region():
    top_left = prompt_for_mouse_position("Move mouse to the TOP-LEFT corner of the region.")
    bottom_right = prompt_for_mouse_position("Move mouse to the BOTTOM-RIGHT corner of the region.")

    left = min(top_left[0], bottom_right[0])
    top = min(top_left[1], bottom_right[1])
    width = abs(bottom_right[0] - top_left[0])
    height = abs(bottom_right[1] - top_left[1])

    print(f"[INFO] Region: left={left}, top={top}, width={width}, height={height}")
    return (left, top, width, height)

def move_mouse_to_center(region):
    left, top, width, height = region
    cx = left + width // 2
    cy = top + height // 2
    print(f"[INFO] Moving mouse to center: ({cx}, {cy})")
    pyautogui.moveTo(cx, cy, duration=0.3)

def random_pause_long(chance=0.05, min_pause=2.0, max_pause=5.0):
    if random.random() < chance:
        pause_time = random.uniform(min_pause, max_pause)
        print(f"[HUMAN] Long pause: {pause_time:.2f}s")
        time.sleep(pause_time)

def random_pause_short(chance=0.2, min_pause=0.3, max_pause=1.0):
    if random.random() < chance:
        pause_time = random.uniform(min_pause, max_pause)
        print(f"[HUMAN] Short pause: {pause_time:.2f}s")
        time.sleep(pause_time)

def humanlike_scroll(
    pixels_to_scroll: float,
    base_click_size: float,
    total_time: float,
    short_pause_chance=0.3,
    long_pause_chance=0.1
):
    """
    Standard "human-like" approach using a half-cosine curve 
    broken into increments. Great for normal speeds, 
    but can be slow overhead for extreme speeds.
    """

    increments = random.randint(25, 70)
    total_clicks_needed = pixels_to_scroll / base_click_size

    def speed_function(t):
        return 0.5 * (1 - math.cos(math.pi * t))

    speeds = [speed_function(i / increments) for i in range(increments + 1)]

    print(f"[HUMAN] (Normal) Scrolling ~{pixels_to_scroll:.0f}px over ~{total_time:.2f}s, increments={increments}")

    clicks_done = 0
    start_t = time.time()
    for i in range(1, increments + 1):
        fraction_step = speeds[i] - speeds[i-1]
        step_clicks = fraction_step * total_clicks_needed
        
        if random.random() < 0.5:
            actual_clicks = int(math.floor(step_clicks))
        else:
            actual_clicks = int(math.ceil(step_clicks))

        # Instead of single clicks, we do them one by one
        for _ in range(actual_clicks):
            pyautogui.scroll(-1)

        step_duration = (total_time / increments) * random.uniform(0.7, 1.3)
        time.sleep(step_duration)

        clicks_done += actual_clicks
        
        random_pause_short(chance=short_pause_chance)
        random_pause_long(chance=long_pause_chance)

    end_t = time.time()
    scrolled_px = clicks_done * base_click_size
    elapsed = end_t - start_t
    print(f"[HUMAN] Finished. ~{scrolled_px:.0f}px scrolled, took {elapsed:.2f}s\n")

def ultra_fast_scroll(
    pixels_to_scroll: float,
    desired_speed_pps=2100
):
    """
    Bulk scroll approach aiming for ~2000px/s or faster.
    We do big chunks in rapid succession with minimal or no sleep.
    """
    base_click_size = 1.0  # macOS default
    total_clicks_needed = pixels_to_scroll / base_click_size

    chunk_clicks = 15  # ~1800 px per chunk if 120 px/click
    total_chunks = math.ceil(total_clicks_needed / chunk_clicks)
    time_needed = pixels_to_scroll / desired_speed_pps

    if time_needed < 0.05:
        time_needed = 0.05

    chunk_delay = time_needed / total_chunks

    print(f"[ULTRA] Trying to scroll ~{pixels_to_scroll:.0f} px at ~{desired_speed_pps} px/s, total_chunks={total_chunks}, chunk_delay={chunk_delay:.4f}s")

    start_t = time.time()
    scrolled_clicks = 0
    for i in range(total_chunks):
        pyautogui.scroll(-chunk_clicks)  # negative => downward
        scrolled_clicks += chunk_clicks
        if chunk_delay > 0:
            time.sleep(chunk_delay)

    scrolled_px = scrolled_clicks * base_click_size
    end_t = time.time()
    elapsed = end_t - start_t

    print(f"[ULTRA] Actually scrolled ~{scrolled_px:.0f}px in {elapsed:.2f}s (~{scrolled_px/elapsed:.0f} px/s)\n")

def scroll_to_new_page(region, coverage=0.95, dist_scale=1.0, time_scale=1.0, mode="normal"):
    """
    We route between "normal" (humanlike) scrolling 
    or "ultra" (bulk approach) to achieve very high speed.
    """
    left, top, width, height = region
    pixels_to_scroll = coverage * height * dist_scale

    base_time = random.uniform(1.0, 3.0)
    total_time = base_time * time_scale

    if mode == "ultra":
        desired_speed = 2000
        ultra_fast_scroll(
            pixels_to_scroll=pixels_to_scroll,
            desired_speed_pps=desired_speed
        )
    else:
        base_click_size = 120.0
        humanlike_scroll(
            pixels_to_scroll=pixels_to_scroll,
            base_click_size=base_click_size,
            total_time=total_time
        )

def main():
    # Adjusted "slow", "medium", and "fast" to better compensate,
    # without touching "ultra" (which remains exactly as you set).
    scroll_presets = {
        "slow":    (1.0, 2.5, "normal"),  # more time_scale to slow it down further
        "medium":  (1.0, 1.2, "normal"),  # slightly slower than default to compensate
        "fast":    (2.0, 0.6, "normal"),  # faster, but not as extreme as ultra
        "ultra":   (2.0, 0.08, "ultra"),  # unchanged
    }

    region = capture_manual_region()
    move_mouse_to_center(region)

    print("Choose a scroll mode: slow, medium, fast, or ultra.")
    choice = input("Enter your choice (slow/medium/fast/ultra): ").strip().lower()
    
    if choice not in scroll_presets:
        choice = "medium"

    dist_scale, time_scale, mode = scroll_presets[choice]
    print(f"[INFO] mode={mode}, dist_scale={dist_scale}, time_scale={time_scale}")

    while True:
        coverage = 0.95
        if random.random() < 0.15:
            coverage = random.uniform(0.5, 0.9)

        scroll_to_new_page(
            region, 
            coverage=coverage, 
            dist_scale=dist_scale, 
            time_scale=time_scale, 
            mode=mode
        )

        wait_time = random.uniform(3.0, 8.0)
        print(f"[INFO] Next scroll in ~{wait_time:.1f}s\n")
        time.sleep(wait_time)

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    try:
        main()
    except pyautogui.FailSafeException:
        print("[FAILSAFE] Top-left corner reached. Exiting.")
    except KeyboardInterrupt:
        print("[KEYBOARD INTERRUPT] Exiting.")
    finally:
        print("[INFO] Done.")
