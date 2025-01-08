# Autoscroller

Human-Like Auto Scroll Script
A Python script that scrolls a user-defined region of the screen in a human-like manner, supporting multiple speed modes: slow, medium, fast, and ultra.

Features
Manual region selection: Prompt to click top-left and bottom-right on screen.
Mouse move: Moves cursor to the center of that region.
Human-like scroll in slow, medium, or fast modes.
Ultra mode for extremely rapid scrolling (around 2000px/s).
Random pauses and “accelerate/decelerate” patterns for more natural movement (non-ultra).
Infinite loop: Continually scroll with intervals between each scroll.
Safety: Move your mouse to the top-left corner or press Ctrl+C to exit.
Requirements
Python 3.6+
PyAutoGUI
bash
Copy code
pip install pyautogui
macOS (or another OS that supports PyAutoGUI).
If on macOS, you must grant Terminal (or your IDE) Accessibility and Screen Recording permissions under System Settings → Privacy & Security.
Setup Instructions
Clone or Download this repository.
Install dependencies:
bash
Copy code
pip install pyautogui
Run the Script:
bash
Copy code
python main.py
(Replace main.py with whatever you named the script.)
Usage
Select Region:

The script will prompt you to move your mouse to the top-left corner of the desired region (e.g., a mirrored iPhone screen) and press ENTER.
Then it asks for the bottom-right corner similarly.
Choose Mode:

slow
medium
fast
ultra
Example:

bash
Copy code
Choose a scroll mode: slow, medium, fast, or ultra.
Enter your choice (slow/medium/fast/ultra): fast
slow: Longer, gentler scroll.
medium: Default moderate pace.
fast: Faster scrolling, but still “human-like.”
ultra: Bulk or “blast” scrolling at ~2000px/s.
Script Behavior:

Once you choose a mode, the script scrolls that region in an infinite loop.
It randomly pauses 3–8 seconds between scrolls.
It also occasionally does partial coverage (e.g., 50–90% of the region height) instead of the full 95%.
Stopping:

Press Ctrl + C in the terminal to raise KeyboardInterrupt.
Or move your mouse to the top-left corner of your screen to trigger PyAutoGUI’s FailSafe.
Notes & Tips
Accessibility and Screen Recording:
On macOS Ventura or later, go to System Settings → Privacy & Security → Accessibility and Screen Recording to add and enable the Terminal or IDE you’re using. Then restart that app.
Adjusting Speeds:
If you want to tweak slow, medium, or fast speeds further, open the code in the main() function, find the scroll_presets dictionary, and adjust the (dist_scale, time_scale) values.
Pauses:
Inside functions like random_pause_short or random_pause_long, you can change the chance values, or the min_pause/max_pause durations, if you want fewer or more frequent pauses.
Ultra:
“Ultra” is specifically set to a bulk scroll approach, ignoring the usual “human-like” increments. This blasts through the screen quickly.
If you need it even faster, you can increase desired_speed_pps or the chunk_clicks.
Disclaimer
This code is intended for demonstration and testing. Use responsibly in compliance with any platform’s terms of service or guidelines.
