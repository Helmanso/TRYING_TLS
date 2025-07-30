from dotenv import load_dotenv
import os
from init import init_browser_and_login
from check_for_slot import check_for_slot

load_dotenv()
EMAIL = os.getenv("TLS_USERNAME")
PASSWORD = os.getenv("TLS_PASSWORD")

driver = init_browser_and_login(EMAIL, PASSWORD)
if driver:
    print("🔍 Checking for available slots...")
    slot_available = check_for_slot(driver, EMAIL, PASSWORD)
    
    if slot_available:
        print("🎉 Slot is available! Please check the screenshot 'possible_slot.png'.")
    else:
        print("❌ No slots available at the moment.")
    
    driver.quit()
else:
    print("❌ Failed to initialize the browser or login.")