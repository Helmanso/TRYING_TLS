import time
import pyautogui
from selenium.webdriver.common.by import By

def handle_cloudflare_if_detected(driver):
    """
    Detects if Cloudflare verification is present and returns checkbox position if found
    
    Returns:
        dict: {
            'detected': bool,  # True if Cloudflare is detected
            'position': tuple or None  # (x, y) coordinates of checkbox if found
        }
    """
    text = driver.execute_script("return document.body.innerText").lower()
    bg_color = driver.execute_script("return window.getComputedStyle(document.body, null).getPropertyValue('background-color');")

    cloudflare_detected = (
        "verify you are human" in text or
        "needs to review the security" in text or
        "cloudflare" in text or
        "checking your browser" in text or
        "please wait while we check" in text or
        "rgb(0" in bg_color or
        "rgb(17" in bg_color or
        "#000" in bg_color
    )

    if cloudflare_detected:
        print("⚠️ Cloudflare verification detected. Attempting to handle...")
        # Wait for the checkbox to appear
        time.sleep(7)
        # Check only if we are still on the Cloudflare page or the website redirected without checkbox
        text = driver.execute_script("return document.body.innerText").lower()
        if "verify you are human" in text or "cloudflare" in text:
            # Click on the checkbox position
            click_at_position(241, 404)
            # sleep to allow Cloudflare to process the click
            time.sleep(4)
            return True
        else:
            print("⚠️ Cloudflare verification not detected after waiting.")
            return False
    else:
        print("⚠️ Cloudflare not detected or no checkbox found.")
        return False


def click_at_position(x, y):
    """
    Moves mouse to (x, y) and clicks
    """
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    print(f"🖱️ Clicked at ({x}, {y})")