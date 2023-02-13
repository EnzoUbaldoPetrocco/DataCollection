from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import requests
import time
from unidecode import unidecode
from datetime import datetime as dt
from PIL import Image
import io


def check_and_download(labels, download_path, element):
    global count
    image_url = element.get_attribute("src")
    if image_url and 'http' in image_url:  # check if we can download the image
        bool_down = False
        for lbl in labels:
            if lbl in unidecode(element.get_attribute('alt').casefold()):  # check if the image caption contains word label in a case and accent insensitive way
                bool_down = bool_down or True# check if the image caption contains word label in a case and accent insensitive way
        if bool_down:
            download_image(download_path, image_url, f'image_{count}.jpeg')
            count += 1

def scroll_down(wd, delay, times):
    for i in range(times):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10*delay)

def scroll_up(wd, delay, times):
    for i in range(times):
        wd.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        time.sleep(delay)

def download_image(down_path, url, file_name, image_type='JPEG',verbose=True):
    try:
        time = dt.now()
        curr_time = time.strftime('%H:%M:%S')
        #Content of the image will be a url
        img_content = requests.get(url).content
        #Get the bytes IO of the image
        img_file = io.BytesIO(img_content)
        #Stores the file in memory and convert to image file using Pillow
        image = Image.open(img_file)
        image = image.convert('RGB')
        file_pth = down_path + file_name

        with open(file_pth, 'wb') as file:
            image.save(file, image_type)

        if verbose == True:
            print(f'The image: {file_pth} downloaded successfully at {curr_time}.')
    except Exception as e:
        print(f'Unable to download image from Google Photos due to\n: {str(e)}')

def manage_loading(driver, delay):
    scroll_down(driver, delay, 5)
    next_page_button=driver.find_element(By.CLASS_NAME, "mye4qd")
    next_page_button.click()
    driver.implicitly_wait(5*delay)


n = input('Enter the number of images related to download: (default = 55) ') 
if n == '0' or not n:
    n = 55
else:
    n = int(n)
m = input('Enter the number of images to scroll: (default = 30) ')
if m == '0' or not m:
    m = 55
else:
    m = int(n)
query = input('Enter the query: ')
print('Enter labels that must be present in the description of the image. \nFirst the number of labels you want to enter:')
n_labels = input(f' (default = {query}) ')
labels = []
labels.append(query)
if not n_labels:
    n_labels = 0
else:
    n_labels = int(n_labels)
for i in range(n_labels):
    labels.append(input('Enter the label: '))
download_path = input('Enter the path where you want to download the image: ')
delay = 0.3
# create Selenium web driver instance
driver = webdriver.Chrome()

# navigato to google images and search for the desired query
driver.get("https://www.google.it/imghp")

accept=True
if accept:
    accept_button =  driver.find_elements("xpath","""//*[@id="L2AGLb"]/div""")
    accept = False
    try:
        accept_button[0].click()
    except:
        raise ValueError("Can't push the button")

driver.implicitly_wait(delay)

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)

# scrool through the search results 
# and click on an image to view the related images

scroll_down(driver, delay, 3)
scroll_up(driver, delay, 3)
main_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
if download_path[-1] != '/':
    download_path = download_path + '/' 
if not os.path.exists(download_path):
            print(f'Making directory: {str(download_path)}')
            os.makedirs(download_path)
count = 0
for i in range(m):
    try:
        main_images[i].click()
    except:
        try:
            scroll_down(driver, delay, 3)
            scroll_up(driver, delay, 3)
            main_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
            main_images[i].click()
        except:
            try:
                manage_loading(driver, delay)
                continue
            except:
                print('END OF IMAGES, TRY LESS IMAGES')
                break
    main_image = main_images[i]
    driver.implicitly_wait(3*delay)

    lat_bar = driver.find_element(By.CLASS_NAME, 'WSABTc.a0XzNd')
    lat_bar.click()

    scroll_down(driver, delay, 3)
    scroll_up(driver, delay, 3)

    suggested_images = driver.find_element(By.CLASS_NAME, 'MkRxHd.MIdC8d.jwwPNd')
    url_sugg_page = suggested_images.get_attribute('href')

    try:
        driver.get(url_sugg_page)
        driver.implicitly_wait(delay)
    except:
        print('doesn''t open')
        continue

    scroll_down(driver, delay, 3)
    scroll_up(driver, delay, 3)

    sug_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")

    for sug_image in sug_images[0:n]:
        try:
            check_and_download(labels, download_path, sug_image)
        except:
            try:
                manage_loading(driver, delay)
                continue
            except:
                print('END OF IMAGES, TRY LESS IMAGES')
                break

    driver.back()
driver.quit()

