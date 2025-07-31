import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_utils import perform_login


def init_browser_and_login(email, password):
    """
    Initialize browser and perform login using shared login logic
    
    Args:
        email: Login email
        password: Login password
    
    Returns:
        driver: Selenium WebDriver instance (logged in)
    """
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options)
    
    # Use shared login function
    login_success = perform_login(driver, email, password)
    
    if not login_success:
        print("❌ Login failed during initialization")
        driver.quit()
        return None

    return driver
