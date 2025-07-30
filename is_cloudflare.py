from datetime import time
import pyautogui
from selenium.webdriver.common.by import By

def is_cloudflare_waiting(driver):
    """
    Detects if Cloudflare verification is present and returns checkbox position if found
    
    Returns:
        dict: {
            'detected': bool,  # True if Cloudflare is detected
            'position': tuple or None  # (x, y) coordinates of checkbox if found
        }
    """
    try:
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
            # Try to get checkbox position
            time.sleep(5)  # Allow time for page to settle
            try:
                checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
                location = checkbox.location
                size = checkbox.size
                x = location['x'] + size['width'] / 2
                y = location['y'] + size['height'] / 2
                return {
                    'detected': True,
                    'position': (x, y)
                }
            except Exception as e:
                print(f"⚠️ Cloudflare detected but checkbox not found: {e}")
                return {
                    'detected': True,
                    'position': None
                }
        else:
            return {
                'detected': False,
                'position': None
            }
        

def handle_cloudflare_if_detected(driver):
    """
    Helper function to detect and handle Cloudflare verification
    
    Returns:
        bool: True if Cloudflare was detected and handled, False otherwise
    """
    result = is_cloudflare_waiting(driver)
    
    if result['detected']:
        print("🌩️ Cloudflare verification detected.")
        
        if result['position']:
            x, y = result['position']
            print(f"📍 Found checkbox at position ({x}, {y})")
            click_at_position(x, y)
            return True
        else:
            print("⚠️ Cloudflare detected but no checkbox found. Using fallback position.")
            # Use the hardcoded fallback position
            click_at_position(436.58984375, 407.0078125)
            return True
    
    return False

def click_at_position(x, y):
    """
    Moves mouse to (x, y) and clicks
    """
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    print(f"🖱️ Clicked at ({x}, {y})")