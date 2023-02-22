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
from selenium.webdriver.chrome.options import Options

french_labels = ['french', 'lamp', 'france',
'lamps', 'european', 'art deco', 'liberty', 
'abat-jour', 'bouillotte', 'francese', 'francesi',
 'lampada', 'lampade', 'europea', 'europee']

chinese_labels = ['chinese', 'lamp', 'china',
'lamps', 'oriental', 'asian', 'antique', 
'porcelain', 'bouillotte', 'cinese', 'cinesi',
 'lampada', 'lampade', 'lantern', 
 'lanterns', 'lanterna', 'lanterne', 'orientale',
 'orientali', 'asiatica', 'asiatiche', 'asiatico',
 'antico', 'porcellana']

turkish_labels = ['turkish', 'turkey', 'lamp', 'lamps', 
'traditional', 'arabic', 'arabian', 'oriental', 'table',
'mosaic', 'antique', 'turca', 'turche', 'lampada', 
'lampade', 'tradizionale', 'araba', 'orientale', 'tavolo', 
 'antico']

indian_carpet_labels = ['indian', 'home', 'decor', 'carpet',
  'indiano', 'casa', 'traditional','rug', 'rugs',
  'tappeto', 'tappeti' ]

japanese_carpet_labels = ['japanese', 'home', 'decor', 'carpet',
  'giapponese', 'casa', 'traditional','rug', 'rugs',
  'tappeto', 'tappeti' ]

scandinavian_carpet_labels = ['scandinavian', 'home', 'decor', 'carpet',
  'scandinavo', 'casa', 'traditional','rug', 'rugs',
  'tappeto', 'tappeti' ]

class Scraping:
    def check_and_download(self, labels, download_path, element, context=' '):
        image_url = element.get_attribute("src")
        if image_url and 'http' in image_url:  # check if we can download the image
            bool_down = False
            inherence_words = str(unidecode(element.get_attribute('alt').casefold())).split(' ')
            for word in inherence_words:
                for lbl in labels:
                    if lbl == word:  # check if the image caption contains word label in a case and accent insensitive way
                        bool_down = bool_down or True# check if the image caption contains word label in a case and accent insensitive way
            if bool_down:
                print(self.download_image)
                self.download_image(download_path, image_url, f'image_{context}_{self.count}.jpeg')
                self.count += 1

    def scroll_down(self, wd, delay, times):
        for i in range(times):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(8*delay)

    def scroll_up(self, wd, delay, times):
        for i in range(times):
            wd.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
            time.sleep(delay)

    def download_image(self, down_path, url, file_name, image_type='JPEG',verbose=True):
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

    def next_page(self, driver, delay):
        self.scroll_down(driver, delay, 8)
        next_page_button=driver.find_element(By.CLASS_NAME, "mye4qd")
        next_page_button.click()
        driver.implicitly_wait(5*delay)

    def __init__(self):
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
        delay = 0.55

        standard_ds = input('Are you searching for any specific dataset?:'+
        '\n- Chinese lamp;\n- French lamp;\n- Turkish lamp;\n' +
        '- Indian carpet;\n- Japanese carpet;\n- Scandinavian carpet;\n' +
        'Enter only the nationality')
        if standard_ds == 'Chinese' or standard_ds == 'chinese':
            for i in chinese_labels:
                labels.append(i)
        elif standard_ds == 'French' or standard_ds == 'french':
            for i in french_labels:
                labels.append(i)
        elif standard_ds == 'Turkish' or standard_ds == 'turkish':
            for i in turkish_labels:
                labels.append(i)
        elif standard_ds == 'Indian' or standard_ds == 'indian':
            for i in indian_carpet_labels:
                labels.append(i)
        elif standard_ds == 'Japanese' or standard_ds == 'japanese':
            for i in japanese_carpet_labels:
                labels.append(i)
        elif standard_ds == 'Scandinavian' or standard_ds == 'scandinavian':
            for i in scandinavian_carpet_labels:
                labels.append(i)

        query_strings = query.split(' ')
        context = query_strings[0]
        if len(query_strings)>1:
            for string in query_strings[1:len(query_strings)]:
                context = context + string
        print(labels)
        # create Selenium web driver instance
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-gpu-blocklist")
        chrome_options.add_argument("--enable-webgl-developer-extensions")
        chrome_options.add_argument("--enable-webgl-draft-extensions")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_options=chrome_options)
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

        self.scroll_down(driver, delay, int(m/10))
        self.scroll_up(driver, delay, int(m/10))
        main_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
        if download_path[-1] != '/':
            download_path = download_path + '/' 
        if not os.path.exists(download_path):
                    print(f'Making directory: {str(download_path)}')
                    os.makedirs(download_path)
        self.count = 0
        for i in range(m):
            try:
                main_images[i].click()
            except:
                try:
                    self.scroll_down(driver, delay, 3)
                    self.scroll_up(driver, delay, 3)
                    main_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
                    main_images[i].click()
                except:
                    try:
                        self.next_page(driver, delay)
                        main_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
                        driver.back()
                        main_images[i].click()
                        continue
                    except:
                        print('END OF IMAGES, TRY LESS IMAGES')
                        continue
            main_image = main_images[i]
            driver.implicitly_wait(3*delay)

            lat_bar = driver.find_element(By.CLASS_NAME, 'WSABTc.a0XzNd')
            lat_bar.click()

            self.scroll_down(driver, delay, int(m/10))
            self.scroll_up(driver, delay, int(m/10))

            suggested_images = driver.find_element(By.CLASS_NAME, 'MkRxHd.MIdC8d.jwwPNd')
            url_sugg_page = suggested_images.get_attribute('href')

            try:
                driver.get(url_sugg_page)
                driver.implicitly_wait(delay)
            except:
                print('doesn''t open')
                continue

            self.scroll_down(driver, delay, int(n/10))
            self.scroll_up(driver, delay, int(n/10))

            sug_images = driver.find_elements(By.CLASS_NAME, "Q4LuWd")

            for sug_image in sug_images[0:min(len(sug_images),n)]:
                try:
                    self.check_and_download(labels, download_path, sug_image, query)
                except:
                    continue

            driver.back()
        driver.quit()

