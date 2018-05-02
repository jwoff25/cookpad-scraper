from bs4 import BeautifulSoup
import requests

#for offline debugging (comment out lines 7 and 8)
soup = BeautifulSoup(open('test3.html'),"html.parser")

## Set up beautiful soup
#rq = requests.get("https://cookpad.com/recipe/1519175")
#soup = BeautifulSoup(rq.text, "html.parser")
ingredients = soup.find_all("div", {"id" : "ingredients_list"})
ingredients_list = []
amount_list = []
## Servings
servings = soup.find_all("h3", {"class": "servings_title"})
servings_list =  [x.replace("\n","") for x in servings[0].text.strip().split("\n") if x.replace("\n","") != u'']
serving = servings_list[1]

## Recipe Title
title = soup.find("h1", {"class": "recipe-title fn clearfix"}).text.strip()

## Ingredients
for divs in ingredients[0].find_all("div", {"class": "ingredient_name"}):
    ingredients_list.append(divs.text.strip())
for divs in ingredients[0].find_all("div", {"class": "ingredient_quantity amount"}):
    amount_list.append(divs.text.strip())

## Printing (debug)
with open('trial1.txt', 'w') as w:
    # write title
    w.write(title.encode('utf-8') + "\n")
    # write servings
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