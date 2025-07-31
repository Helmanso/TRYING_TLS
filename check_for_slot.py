from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, random
from is_cloudflare import handle_cloudflare_if_detected
from login_utils import perform_login
import requests

APPOINTMENT_URL = "https://fr.tlscontact.com/appointment/ma/maCAS2fr/21725397"

def fetch_account_in_browser(driver):
    js_code = """
    return fetch("https://fr.tlscontact.com/api/account", {
        method: "GET",
        headers: {
            "Accept": "application/json, text/plain, */*"
        },
        credentials: "include"
    }).then(res => res.json()).catch(err => ({ error: err.toString() }));
    """
    return driver.execute_script(js_code)


def fetch_slots_in_browser(driver):
    js_code = """
    return fetch("https://fr.tlscontact.com/services/customerservice/api/tls/appointment/ma/maCAS2fr/table?client=fr&formGroupId=21725397&appointmentType=prime%20time&appointmentStage=appointment", {
        method: "GET",
        headers: {
            "Accept": "application/json, text/plain, */*"
        },
        credentials: "include"
    }).then(res => {
        if (res.status === 401) {
            return { error: "Session expired (401)", status: 401 };
        }
        if (res.status === 403) {
            return { error: "Forbidden (403)", status: 403 };
        }
        if (!res.ok) {
            return { error: `HTTP ${res.status}: ${res.statusText}`, status: res.status };
        }
        return res.json();
    }).catch(err => ({ error: err.toString() }));
    """
    return driver.execute_script(js_code)


def check_for_slot(driver, email=None, password=None):
    """
    Check for available slots with automatic session recovery
    
    Args:
        driver: Selenium WebDriver instance
        email: Login email (required for session recovery)
        password: Login password (required for session recovery)
    """
    driver.get(APPOINTMENT_URL)
   
    handle_cloudflare_if_detected(driver)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    
    while True:
        try:
            print(f"\n⏰ Checking at {time.strftime('%H:%M:%S')}")

            # 2. Check available slots
            slot_data = fetch_slots_in_browser(driver)

            if "error" in slot_data:
                if "status" in slot_data and slot_data["status"] == 401:
                    print("🔑 Session expired (401). Attempting to re-login...")
                    if email and password:
                        # Use shared login function for session recovery
                        login_success = perform_login(
                            driver, email, password
                        )
                        
                        if login_success:
                            WebDriverWait(driver, 10).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            # Navigate back to the appointment page
                            driver.get(APPOINTMENT_URL)
                            handle_cloudflare_if_detected(driver)
                            WebDriverWait(driver, 10).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            # Re-check for slots
                            print("🔄 Session recovered successfully!")
                            continue  # Skip this iteration and try again
                      
                elif "status" in slot_data and slot_data["status"] == 403:
                    # Reload the page if forbidden
                    print("🚫 Forbidden (403). Reloading page...")
                    driver.refresh()
                    handle_cloudflare_if_detected(driver)
                    WebDriverWait(driver, 10).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                    continue  # Retry fetching slots after refresh
                else:
                    print(f"❌ Error fetching slots: {slot_data['error']}")
            elif not slot_data:
                print("⚠️ No slot data received.")
            else:
                # Check for valid slots (status 1 means available)
                available_slots = []
                for date, times in slot_data.items():
                    for time_str, status in times.items():
                        if status == 1:
                            available_slots.append((date, time_str))

                if available_slots:
                    for date, time_str in available_slots:
                        print(f" - {date} at {time_str}")
                    
                    # Check cloudflare again before booking
                    handle_cloudflare_if_detected(driver)
                    # Book the first available slot
                    success = handle_slot_booking(driver, available_slots[0])
                    if success:
                        return True
               
              # Wait before next check
            delay = random.uniform(10, 30)
            print(f"⏳ Waiting {delay:.1f} seconds before next check...")
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(random.uniform(20, 40))


def handle_slot_booking(driver, slot):
    """
    Handle the booking process for a found slot
    
    Args:
        driver: Selenium WebDriver instance
        slot: Tuple of (date, time_str) for the slot to book
    
    Returns:
        bool: True if booking was successful, False otherwise
    """
    date, time_str = slot
    
    try:
        print(f"📅 Booking slot on {date} at {time_str}...")
        result = book_slot_in_browser(driver, date, time_str)
        
        if "error" in result:
            print(f"❌ Error booking slot: {result['error']}")
            return False
        else:
            print("✅ Slot booked successfully!")
            driver.save_screenshot("slot_found.png")
            return True
            
    except Exception as e:
        print(f"❌ Exception during booking: {e}")
        driver.save_screenshot("booking_error.png")
        return False



def book_slot_in_browser(driver, date, time_str):
    js_code = f"""
    return fetch("https://fr.tlscontact.com/services/customerservice/api/tls/appointment/book?client=fr&issuer=maCAS2fr&formGroupId=21725397&timeslot={date}%20{time_str}&appointmentType=prime%20time&accountType=INDI&lang=fr-fr", {{
        method: "POST",
        headers: {{
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }},
        credentials: "include"
    }}).then(res => res.json()).catch(err => ({{ error: err.toString() }}));
    """
    result = driver.execute_script(js_code)
    return result