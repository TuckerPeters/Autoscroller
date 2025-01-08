import pyautogui
import os

output_path = "/Users/tuckerpeters/AutoScrollerClaude/test_screenshot.png"

img = pyautogui.screenshot(output_path)
print(f"Screenshot saved to: {output_path}")

if os.path.exists(output_path):
    size = os.path.getsize(output_path)
    print(f"File exists at {output_path}, size = {size} bytes.")
    if size > 0:
        print("Screenshot capture succeeded!")
    else:
        print("Screenshot file is 0 bytes, something might be wrong.")
else:
    print("Screenshot file not found, check permissions or file path.")
