from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import pickle
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def test_firefox_session():
    driver = webdriver.Firefox(executable_path="./geckodriver")
    driver.quit()

def return_false(driver):
    return False

# test_firefox_session()

driver = webdriver.Firefox(executable_path="./geckodriver")

# WebDriverWait(driver, timeout=10).until(return_false)
url = "https://identity.flickr.com/login?redir=https%3A%2F%2Fwww.flickr.com%2Fphotos%2F123456789%40N00%2Ffavorites"
driver.get(url)

do_import_cookies = False
if do_import_cookies:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)


do_login = True
if do_login:
    driver.set_window_size(1200, 1000)
    driver.implicitly_wait(10)
    driver.find_element_by_id("login-email").send_keys("mail@gmail.com")
    driver.find_element(By.CSS_SELECTOR, ".mt-5").click()
    driver.find_element_by_id("login-password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, ".mt-5").click()

do_accept_cookies = True
if do_accept_cookies:
    iframe_accept_cookies = driver.find_element_by_xpath("//*[contains(@id, 'pop-frame')]")
    driver.switch_to.frame(iframe_accept_cookies)
    driver.find_element(By.LINK_TEXT, "Save and Exit").click()
    driver.find_element(By.ID, "gwt-debug-close_id").click()
    driver.switch_to.default_content()

views = driver.find_elements_by_class_name("photo-list-photo-view")
current_view = 0
for view in views:
    ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .click(view) \
        .key_up(Keys.CONTROL) \
        .perform()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.close()

# driver.quit()
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
