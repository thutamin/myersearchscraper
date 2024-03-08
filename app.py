from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return 'Hello from Min!'

@app.route('/searchScrape',methods=["Get","POST"])
def search_scrape():
    search_keyword = request.form.get("searchKeyword")
    console.log(f"Keyword: {keyword}" )

    chrome_options = webdriver.ChromeOptions()

    # to run the script locally, comment out the line below.
    path = os.environ.get("CHROMEDRIVER_PATH")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # to run the script locally, uncomment the line below. Don't forget to set up your chrome driver
    # chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

    # to visualize the scraping process comment out the linebelow
    chrome_options.add_argument("--headless")


    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--window-size=1920,1080')

    browser = webdriver.Chrome(executable_path=path,options=chrome_options)
    wait = WebDriverWait(browser, 5)
    browser.get("https://www.myer.com.au/")

    search_field = browser.find_element(By.XPATH,'//*[@id="search-input-desktop"]')
    search_field.send_keys(search_keyword)
    search_field.send_keys(Keys.ENTER)

    keywordFound = False
    try:
        searchResult = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@data-automation='search-result']")))
        keywordFound = True
    except Exception as e:
        searchResult = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@data-automation='no-results-query']")))

    if not keywordFound:
        return jsonify({'error':f"No product is associated with keyword: {search_keyword}"}),404

    scraped_products = []

    def scrape_products():
        browser.refresh()
        products = browser.find_elements(By.XPATH,"//*[@data-automation='product-grid-item']")
        for product in products:
            product_name = product.find_element(By.XPATH,".//p[@data-automation='product-name']").text.strip()
            brand_name = product.find_element(By.XPATH,".//p[@data-automation='product-brand']").text.strip()
            image_url = product.find_element(By.XPATH,".//img[@data-automation='product-image']").get_attribute("src")
            original_price = product.find_element(By.XPATH,".//p[@data-automation='product-price-was']").text.strip()
            product_dict={
                "name":product_name,
                "brand":brand_name,
                "image":image_url,
                "price":original_price
            }
            scraped_products.append(product_dict)

    scrape_products()

    # To do - get data from all pages associated with the search keyword
    # next_button_present = False
    # try:
    #     next_button = browser.find_element(By.XPATH,"//a[@data-automation='paginateNextPage']")
    #     next_button_present = True
    # except:
    #     next_button_present = False
    # print(f"Next Button present: {next_button_present}")
    # while(next_button_present):
    #     next_button.click()
    #     scrape_products()
    #
    #     try:
    #         next_button = browser.find_element(By.XPATH, "//a[@data-automation='paginateNextPage']")
    #         next_button_present = True
    #     except:
    #         next_button_present = False
    #     print(f"Next Button present: {next_button_present}")

    print(len(scraped_products))
    return jsonify(scraped_products),200



    # For debuggin purposes
    # print(f"Keyword Found: {keywordFound}")
    # breakpoint()




if __name__ == '__main__':
    app.run()
