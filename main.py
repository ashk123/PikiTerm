import requests
from bs4 import BeautifulSoup
import os

def SaveArticle(Name, Value) :
    #try
    if not os.path.exists("Articles") :
        os.mkdir("Articles")
    with open(f"Articles/Article {Name}.txt", "w", encoding="utf-8") as ar_file :
        ar_file.write(Value)
        ar_file.close()
    return True
    # except :
      #  return False
        
Datas = {'SEARCH':'', 'TITLE':'', 'BODY':'', 'SELECTION':''}
query = input("Enter the Content : ")
url_search = f"https://en.wikipedia.org/w/index.php?search={query}&title=Special:Search&profile=advanced&fulltext=1&ns0=1&searchToken=7637hhwf6zvrreb4qxzqjusdb"

res = requests.get(url_search)
soup = BeautifulSoup(res.text, "html.parser")
for i in range(5) :
    tag_span = soup.find("a", {'data-serp-pos':f'{str(i)}'})
    Datas['SEARCH'] += str(i)+":"+tag_span.get_text() + ":"

i2 = Datas['SEARCH'].split(":")
num = 0
for i3 in range(len(i2)) :
    try :
        print(str(int(i2[num]) + 1) + " -> " + i2[num + 1])
        num += 2
    except :
        pass


sel = input("\nEnter Selection : ")
num = 0
for i4 in Datas['SEARCH'] :
    i4 = Datas['SEARCH'].split(":")
    if str(int(sel) - 1) == i4[num] :
        Datas['SELECTION'] = str(i4[num + 1])
        break
    else :
        num += 2

def Read(Name) :
    # id you have a linux or mac machine you can run this line ( or anything system that can run linux tools on windows machine )
    os.system(f'less Articles/"Article {Name}.txt"')

def GetArticleValue(NameAR) :
    BodySave = ""
    BodyList = []
    query = NameAR
    text = ""
    url = f"http://en.wikipedia.org/wiki/{query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tag_h1 = soup.find("h1", {'id':'firstHeading'})
    bodytext = soup.find_all('p')
    try :
        Datas['TITLE'] = tag_h1.get_text()
    except :
        Datas['TITLE'] = NameAR
    BodySave += f"Title : {Datas['TITLE']}\nBody :"
    for i in bodytext :
        BodySave += i.get_text()
    #print(BodySave)
    #sel = input("Do You Want to Save Article ? [y,n] ")
    #if sel == "y" :
    SaveArticle(query, BodySave)
     #   print("Your Article is Save .")
    #elif sel == "n" :
     #   print("your article Was not Save .")
    # its a glitch def :)
    # ShellArticle(NameAR, BodySave)
    Read(NameAR)
GetArticleValue(Datas['SELECTION'])
