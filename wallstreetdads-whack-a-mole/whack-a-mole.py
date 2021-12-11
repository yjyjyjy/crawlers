import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pandas as pd


def scan_scam(driver):
    driver.get("https://opensea.io/")
    time.sleep(5)
    searchbox = driver.find_element_by_xpath("//input[@type='search']")
    searchbox.send_keys("wallstreet dad")
    searchbox.send_keys(Keys.RETURN)
    urls = []
    for i in range(20):
        target_list = driver1.find_elements_by_xpath("//a[contains(@class, 'AssetCardFooter--collection-name')]")
        urls += [tar.get_attribute("href") for tar in target_list]
        body = driver1.find_element_by_css_selector("body")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
    urls = pd.Series(urls)
    urls = urls.unique()
    # filter the bad guys only
    target_df = pd.DataFrame(urls, columns=["url"])
    target_df = pd.DataFrame(urls, columns=["url"])
    target_df["collection_name"] = target_df.url.apply(lambda x: x.split("/")[-1])
    target_df = target_df[
        (target_df.collection_name.str.contains("wall"))
        & (target_df.collection_name.str.contains("st"))
        & (target_df.collection_name.str.contains("dad"))
        & (target_df.collection_name != "wallstreetdads")
    ]
    target_df["reported"] = False
    old_list = pd.read_csv("report_log.csv")
    target_df = target_df[~target_df.url.isin(list(old_list.url))]
    target_df = pd.concat([old_list, target_df], axis=0)
    return target_df


def find_input_box(driver, label, element):
    lab = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '{}')]".format(label)))
    )
    box = lab.find_element_by_xpath("../{}".format(element))
    return box


def box_input(driver, label, text):
    box = find_input_box(driver, label, "input")
    box.click()
    box.send_keys(text)


def option_select(driver, label, option):
    box = find_input_box(driver, label, "a")
    box.click()
    time.sleep(2)
    option = WebDriverWait(driver2, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '{}')]".format(option)))
    )
    option.click()
    time.sleep(1)


def report_scam(driver, url):
    driver.get("https://support.opensea.io/hc/en-us/requests/new")
    time.sleep(5)
    option_select(driver, label="How can we help?", option="Trust & Safety Report")
    time.sleep(2)
    box_input(driver, label="Your email address", text="junyu@wallstreetdads.com")
    box_input(driver, label="Subject", text="Reporting bad players stealing our art and scamming our fans")
    time.sleep(1)
    option_select(driver, label="Type of report", option="Fraudulent activity")
    box_input(
        driver, label="URL to item/collection you wish to report", text="https://opensea.io/collection/wallstdadsnft"
    )
    box_input(
        driver,
        label="URL to legitimate asset or works, on or off OpenSea (proof of authorship)",
        text="https://opensea.io/collection/wallstreetdads",
    )
    complaint = """
    We are www.wallstreetdads.com with over 70k members on our Discord and have NOT opened up our general sales minting yet and have NOT revealed our art.
    The fraud collection took art from our website and discord and are trying to sell them.
    Official website: https://www.wallstreetdads.com
    Official collection: https://opensea.io/collection/wallstreetdads
    This collection is clearly a rip off of our art and try to scam our community. Please help taking them down.
    """
    driver.switch_to.frame(driver.find_element_by_id("request_description_ifr"))
    ## Insert text via xpath ##
    elem = driver.find_element_by_xpath("/html/body/p")
    elem.send_keys(complaint)
    ## Switch back to the "default content" (that is, out of the iframes) ##
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(5)


driver1 = webdriver.Chrome()
driver2 = webdriver.Chrome()
while True:
    print(datetime.datetime.now())
    target_df = scan_scam(driver1)
    for url in list(target_df.url[target_df.reported == False]):
        report_scam(driver=driver2, url=url)
        target_df.reported[target_df.url == url] = True
    target_df.to_csv("report_log.csv", index=False)
