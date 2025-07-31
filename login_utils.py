from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from is_cloudflare import handle_cloudflare_if_detected

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from is_cloudflare import handle_cloudflare_if_detected

def perform_login(driver, email, password, timeout=15):
    """
    Reusable login function that handles the complete login process

    Args:
        driver: Selenium WebDriver instance
        email: Login email
        password: Login password
        timeout: Max wait time for elements (default 15 seconds)

    Returns:
        bool: True if login was successful, False otherwise
    """
    try:
        print("🔐 Starting login process...")

        driver.get("https://fr.tlscontact.com/visa/ma/maCAS2fr/home")

        # Wait for page to finish loading
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        handle_cloudflare_if_detected(driver)

        # Wait for and click "Se connecter"
        try:
            login_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='se connecter']"
                ))
            )
            login_button.click()
        except TimeoutException:
            print("❌ 'Se connecter' button not found or not clickable.")
            return False
        

        # Wait for login form
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        try:
            email_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "password"))
            )

            print(email_input, password_input)
            email_input.clear()
            email_input.send_keys(email)

            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            # Wait for login to complete
            # Optional: wait for something that confirms you're logged in
            print("⏳ Waiting for login to complete...")
            WebDriverWait(driver, timeout).until(
                lambda d: "Veuillez voir ci-dessous tous les groupes que vous avez créés" in d.page_source
                      or "Welcome to the TLScontact visa application website for France" in d.page_source
            )

            print("✅ Login successful.")
            return True

        except (TimeoutException, NoSuchElementException) as e:
            print(f"❌ Error filling login form: {e}")
            return False

    except Exception as e:
        print(f"❌ Error during login process: {e}")
        return False
