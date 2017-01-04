#image_scaper.py
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Root path directory the same on all machines
root_dir = os.path.dirname(os.path.realpath(__file__))

#Initialize selenium web driver using Chrome as the browser of choice
driver = webdriver.Chrome()

#Classification image page URLs (Thanks Adobe!!!)
pos_url = "http://stock.adobe.com/search?k=happy+people&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&&search_page="
neg_url = "http://stock.adobe.com/search?k=sad+people&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&search_page="

url_list = [{'folder':"pos", 'url':pos_url}, {'folder':"neg", 'url':neg_url}]

#Get images from page 1 to 100 (default amount given by Adobe)
for current_url in url_list:
    for page in range(1, 100):
        # Load page from URL
        driver.get(current_url['url'] + str(page))

        try:
	        # Delay web driver from searching for up to 10s to allow the page to fully load
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-results")))

        except:
        	#Print to the console if img container was not found on page
            print("Element not found on page " + str(page))

        finally:
            # Locate all of the images on the current page
            img_divs = driver.find_elements_by_xpath('//*[@id="search-results"]/div')
        
            for num, i in enumerate(img_divs):
	            #Extract the url
                img_src = i.find_element_by_tag_name("img").get_attribute("src")
            
                # Store current image locally
                urllib.request.urlretrieve(img_src, root_dir + "/training_images/" + current_url['folder'] + "/" + current_url['folder'] + "_" + str(page) + "_" + str(num) + ".jpg")

driver.close()
