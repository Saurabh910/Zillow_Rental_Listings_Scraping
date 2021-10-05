# Importing modules
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# Constants
x = ""
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSda-fQTvhTl5FE65VObTl_h51zPk1KhVcDVwUQ1B_6jq-Y3Eg/viewform?usp=sf_link"
ZILLOW_LINK = f"https://www.zillow.com/san-francisco-ca/rentals/1-_beds/{x}?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.609407992296134%2C%22north%22%3A37.94080354598875%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A1235192%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
CHROME_DRIVER = YOUR_CHROMEDRIVER_PATH

# Headers to avoid captcha
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"
headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE
}


# Zillow site specific: The content of this list helps to navigate pages on zillow. ["", "2_p", "3_p", etc]
def pages(no_of_pages):
    page_var = []
    for i in range(1, no_of_pages + 1):
        if i == 1:
            page_var.append("")
        else:
            page_var.append(f"{i}_p")
    return page_var


listing_links = []
addresses = []
rent_prices = []
pages_to_nav = pages(int(input("How many pages to scrap? ")))

for item in pages_to_nav:
    x = item
    html = requests.get(ZILLOW_LINK, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    all_links = soup.select("div.list-card-info a.list-card-link")
    for link in all_links:
        try:
            href = link["href"]
        except TypeError:
            listing_links.append("None")
        else:
            if "http" not in href:
                listing_links.append(f"https://www.zillow.com{href}")
            else:
                listing_links.append(href)

    all_addresses = soup.select(".list-card-info address")
    for add in all_addresses:
        addresses.append(add.getText())

    all_price = soup.select("div.list-card-price")
    for price in all_price:
        rent_prices.append(price.getText())

driver = webdriver.Chrome(CHROME_DRIVER)
form = driver.get(FORM_LINK)
time.sleep(3)

# Form specific
for (a, b, c) in zip(addresses, rent_prices, listing_links):
    Q1 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    Q2 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    Q3 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    Q1.send_keys(a)
    Q2.send_keys(b)
    Q3.send_keys(c)
    submit.click()
    time.sleep(1)
    submit_another_response = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response.click()