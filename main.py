import os
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize logging
log_file = 'automated_logs.txt'
login_complete = False  # Boolean to track login status

# Clear any previous records
open(log_file, 'w').close()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', handlers=[
    logging.FileHandler(log_file),
    logging.StreamHandler()
])

# Start webdriver
driver = webdriver.Chrome()

def wait_for_element(driver, by, value, timeout=10):
    """Function to properly handle clicks to ensure there are no errors."""
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

def check_response_code(url):
    """Function to check the HTTP response code."""
    response = requests.get(url)
    if response.status_code == 200: # Error Checking implementation
        driver.get(url)
        logging.info(f"HTTP response code for {url}: {response.status_code}")
    else:
        if login_complete:
            post_article() # If login is already completed then post article
        else:
            login() # Else login 

def login():
    """Function to handle the login process."""
    global login_complete
    
    start_time = time.time()

    # Check HTTP response code for the main page
    check_response_code('https://atg.party')

    response_time = time.time() - start_time

    logging.info(f"Page loaded in {response_time:.2f} seconds")

    # Login
    login_button = wait_for_element(driver, By.XPATH, '/html/body/div[5]/header/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div[1]/div/div/p/span')
    login_button.click()

    email_input = wait_for_element(driver, By.ID, 'email_landing')
    email_input.click()
    email_input.send_keys('wiz_saurabh@rediffmail.com')

    password_input = wait_for_element(driver, By.ID, 'password_landing')
    password_input.send_keys('Pass@123')
    password_input.send_keys(Keys.RETURN)

    time.sleep(3)

    login_complete = True
    post_article()

def post_article():
    """Function to handle posting an article."""
    check_response_code('https://atg.party/article')

    # Enter Title
    title_input = wait_for_element(driver, By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div/div/div[1]/div/textarea')
    title_input.click()
    title_input.send_keys('Python Automation')

    # Enter description
    description_input = wait_for_element(driver, By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div/div/div[2]/div/div/div/div[1]/div/div/div')
    description_input.click()
    description_input.send_keys('Posted automatically using Selenium')

    # Upload cover image
    cover_image_input = driver.find_element(By.ID, 'cover_image')
    cover_image_path = os.path.abspath('automate.jpg')
    cover_image_input.send_keys(cover_image_path)

    time.sleep(6)  # Wait for all details to be uploaded

    # Click on POST
    post_button = wait_for_element(driver, By.ID, 'hpost_btn')
    post_button.click()

    time.sleep(5)  # Final wait before everything loads perfectly

    logging.info(f"Article posted successfully. New page URL: {driver.current_url}")

    driver.quit()

# Start the process
login()
