from bs4 import BeautifulSoup
import requests
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib

# for offline debugging (comment out lines 7 and 8)
# soup = BeautifulSoup(open('test3.html'),"html.parser")

counter = 0
for link in open('links.txt', 'r').readlines():
    ## Set up beautiful soup
    print link
    rq = requests.get(link.strip())
    soup = BeautifulSoup(rq.text, "html.parser")
    ingredients = soup.find_all("div", {"id" : "ingredients_list"})
    ingredients_list = []
    amount_list = []
    ## Servings
    servings = soup.find_all("h3", {"class": "servings_title"})
    servings_list = [x.replace("\n","") for x in servings[0].text.strip().split("\n") if x.replace("\n","") != u'']
    print [x.encode('utf-8') for x in servings_list]
    if len(servings_list) == 2:
        serving = servings_list[1]

    ## Recipe Title
    title = soup.find("h1", {"class": "recipe-title fn clearfix"}).text.strip()

    ## Ingredients
    for divs in ingredients[0].find_all("div", {"class": "ingredient_name"}):
        ingredients_list.append(divs.text.strip())
    for divs in ingredients[0].find_all("div", {"class": "ingredient_quantity amount"}):
        amount_list.append(divs.text.strip())

    ## Printing (debug)
    
    filename = title + ".txt"
    with open(filename, 'w') as w:
        # write title
        w.write(title.encode('utf-8') + "\n")
        # write servings
        if len(servings_list) == 2:
            w.write(serving.encode('utf-8') + "\n")
            w.write("--------------" + "\n")
        # write ingredients and respective amounts
        for i in range(len(ingredients_list)):
            w.write(ingredients_list[i].encode('utf-8') + " " + amount_list[i].encode('utf-8') + "\n")
        w.write("--------------" + "\n")
        # write instructions
        i = 1 #numbering for instructions
        for inst in soup.find_all("p", {"class": "step_text"}):
            w.write(str(i) + "." + inst.text.strip().encode('utf-8') + "\n")
            i+=1
        w.write("\n")
    counter += 1


    ## Get Images
    photo_url = soup.find_all("img", {"class", "analytics_tracking photo large_photo_clickable"})[0]['src']
    urllib.urlretrieve(photo_url, title + '.jpg')
    #url = urlopen()
