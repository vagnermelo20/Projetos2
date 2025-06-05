from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException
)
import time


def send_whatsapp_messages(contacts, message, new_contact=None, new_contact_name=None):

    """Send WhatsApp messages to multiple contacts."""
    try:
        # Set up WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 20)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("Please scan the QR code (30 seconds)...")
        time.sleep(30)  # Wait for user to scan QR

        # Register new contact if needed
        if new_contact:
            if new_contact not in contacts:
                success = register_contact(driver, wait, new_contact, new_contact_name)
                if success:
                    contacts.append(new_contact)

        # Send messages
        for contact in contacts:
            send_message(driver, wait, contact, message)

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()


def register_contact(driver, wait, phone, name):
    """Optional: Register a new contact. Currently a placeholder."""
    print(f"Registering new contact (not implemented): {name} - {phone}")
    # Placeholder for contact registration functionality
    return True


def send_message(driver, wait, contact, message, max_retries=3):
    """Send message to a single contact with retry handling."""
    retries = 0

    while retries < max_retries:
        try:
            # Click the search box
            search_box = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            search_box.click()
            time.sleep(1)

            # Clear previous text manually (some React apps need this trick)
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.DELETE)
            time.sleep(1)

            # Type the contact number or name and press ENTER
            search_box.send_keys(contact)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)

            # Wait for message input to load
            msg_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            ))

            # Type and send message
            msg_box.send_keys(message)
            msg_box.send_keys(Keys.ENTER)
            print(f"✅ Sent to {contact}")
            time.sleep(3)
            return True

        except StaleElementReferenceException:
            print(f"⚠️ Stale element (retry {retries + 1}/{max_retries})")
            retries += 1
            time.sleep(2)

        except (NoSuchElementException, TimeoutException) as e:
            print(f"❌ Could not send to {contact}: {str(e)}")
            return False

    print(f"❌ Max retries reached for {contact}")
    return False


