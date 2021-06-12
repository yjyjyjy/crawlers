import os
import time
import jsonlines
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

OUTPUT_FILE = 'freelancers.jsonl'
if os.path.exists(OUTPUT_FILE):
  os.remove(OUTPUT_FILE)

driver = webdriver.Firefox()
driver.get('https://www.upwork.com/') # go to website

WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(@class,'login-link')]"))).click()
userbox = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@id='login_username']")))
userbox.click()
userbox.send_keys('yangjunyu')
userbox.send_keys(Keys.RETURN)

pwbox = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@id='login_password']")))
pwbox.click()
pwbox.send_keys('happy2dai')
pwbox.send_keys(Keys.RETURN)

avatar = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//img[contains(@class,'nav-user-avatar')]")))
avatar.click()

WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//div[contains(text(),'Water Bear LLC')]"))).click()

time.sleep(3)

search_box = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, "//div[@id='nav-main']//input[contains(@class, 'nav-search-catalog-input')]")))
search_box.click()
search_box.send_keys('personal assistant')
search_box.send_keys(Keys.RETURN)

time.sleep(3)
locale_search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='facetCard-2']//input")))
time.sleep(1)
locale_search_box.click()
time.sleep(1)
locale_search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='facetCard-2']//input")))
locale_search_box.send_keys('California')
time.sleep(1)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "//strong[contains(text(), 'California')]"))).click()

def check_page(driver):
    time.sleep(3)
    cards = driver.find_elements_by_xpath("//div[contains(@class, 'up-card-section')]")
    for card in cards:
        name_button = card.find_element_by_xpath(".//button[@itemprop='name']")
        name_text = name_button.text
        titles = card.find_elements_by_xpath(".//p[contains(@class, 'freelancer-title')]")
        title = titles[0].text if len(titles)>0 else ''
        city = card.find_element_by_xpath(".//span[@itemprop='locality']").text
        salary = card.find_element_by_xpath(".//span[@data-v-2aaa2a81='']").text
        ss = card.find_elements_by_xpath(".//span[@class='up-job-success-text']")
        success = ss[0].text if len(ss)>0 else ''
        tt = card.find_elements_by_xpath(".//span[contains(@class,'top-rated-badge-status')]")
        top_rated = len(tt)>0

        if (city == 'Oakland') | (city == 'Berkeley') | (city == 'San Francisco'):
            driver.execute_script("arguments[0].scrollIntoView();", name_button) # scroll the viewport to the element 
            ActionChains(driver).move_to_element(name_button).key_down(Keys.COMMAND).click(name_button).key_up(Keys.COMMAND).perform()
            time.sleep(0.5)
            cur = driver.current_window_handle
            chwd = driver.window_handles
            driver.switch_to.window(chwd[-1])
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h1")))
            freelancer = {
                'name':name_text,
                'title': title,
                'city':city,
                'salary':salary,
                'success':success,
                'top_rated':top_rated,
                'url':driver.current_url
                }
            # write out to the jsonl file
            with jsonlines.open(OUTPUT_FILE, mode='a') as writer:
                writer.write(freelancer)
            driver.close()
            driver.switch_to.window(cur)
            time.sleep(0.5)

while True:
    try:
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='up-pagination']")))
        pagination = driver.find_element_by_xpath("//ul[@class='up-pagination']").find_elements_by_xpath(".//li[@class='pagination-link']")
        check_page(driver)

        if (pagination[-1].find_element_by_xpath('button').get_attribute('disabled') == 'true'):
            break
        pagination[-1].click()
    except:
        time.sleep(60)
        driver.refresh()
    
