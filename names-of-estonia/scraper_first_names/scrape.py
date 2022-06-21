from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("https://www.eesti.ee/portaal/rrteenus.nimede_stat")

time.sleep(30)

assert "Nimede" in driver.title
elem = driver.find_element_by_name("enimi")
elem.clear()
elem.send_keys("Johannes")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()