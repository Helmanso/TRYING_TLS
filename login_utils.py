from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from is_cloudflare import handle_cloudflare_if_detected, is_cloudflare_waiting, click_at_position

def perform_login(driver, email, password):
    """
    Reusable login function that handles the complete login process
    
    Args:
        driver: Selenium WebDriver instance
        email: Login email
        password: Login password
    
    Returns:
        bool: True if login was successful, False otherwise
    """
    try:
        print("🔐 Starting login process...")
        
        # Visit home page
        driver.get("https://fr.tlscontact.com/visa/ma/maCAS2fr/home")
        time.sleep(4)

        # Handle Cloudflare if present
        handle_cloudflare_if_detected(driver)

        # Click "Se connecter"
        try:
            login_button = driver.find_element(
                By.XPATH,
                "//a[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='se connecter']"
            )
            login_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"❌ Could not find login button: {e}")
            return False

        # Fill login form
        try:
            email_input = driver.find_element(By.ID, "username")
            email_input.clear()
            email_input.send_keys(email)
            
            password_input = driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(8)
            
            print("✅ Login completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error filling login form: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error during login process: {e}")
        return False

def perform_login_and_navigate_to_appointment(driver, email, password, appointment_url):
    """
    Perform login and navigate to appointment page
    
    Args:
        driver: Selenium WebDriver instance
        email: Login email
        password: Login password
        appointment_url: URL of the appointment page to navigate to
    
    Returns:
        bool: True if login and navigation was successful, False otherwise
    """
    try:
        # Perform login
        if not perform_login(driver, email, password):
            return False
        
        # Navigate to appointment page
        print("🌐 Navigating to appointment page...")
        driver.get(appointment_url)
        time.sleep(4)
        
        # Handle Cloudflare on appointment page if needed
        handle_cloudflare_if_detected(driver)
        
        print("✅ Successfully navigated to appointment page!")
        return True
        
    except Exception as e:
        print(f"❌ Error during login and navigation: {e}")
        return False
