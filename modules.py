import os
import requests
from bs4 import BeautifulSoup


def images_search(for_search):
    print("ass")
    word = ""
    
    for w in for_search:
        word += w + " "


    url = "https://www.google.com/search?q=" + word + "&tbm=isch"
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    
    # url_imgs = []
    
    for raw_img in soup.find_all("img"):
        
        try:
            os.mkdir(settings.IMAGES_DIR)
        except FileExistsError:
            pass

        print("качаю")
        link = raw_img.get("src")
        # проверка на ссылку
        if "http" in link:
            
            os.system("wget -O " + settings.IMAGES_DIR + "/" + str(random.randint(1, 1000000)) + ".jpeg " + link)
            # os.rename(os.listdir(settings.IMAGES_DIR)[-1], settings.IMAGES_DIR + "/" + link + ".jpeg")
            print("скачал")
        
        # скачать всего 10 штук
        if len(os.listdir(settings.IMAGES_DIR)) == 10:
            break