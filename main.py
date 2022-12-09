import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse

# define section
OS = 0 if (sys.platform == "linux") else 0 if (sys.platform == "darwin") else 1 if (sys.platform == "win32") else 0

more =  [
    'en',
    'jp',
    'fa',
    'eu'
]

cl = more[0]

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
if (len(sys.argv) > 1) :
    argv_user = ""
    for i in range(1, len(sys.argv)) :
        argv_user += sys.argv[i] + " "

    query = argv_user[:-1]
else :
    query = input("Enter the Content : ")
url_search = f"https://{cl}.wikipedia.org/w/index.php?search={query}&title=Special:Search&profile=advanced&fulltext=1&ns0=1&searchToken=7637hhwf6zvrreb4qxzqjusdb"

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
sel = input("\nEnter Selection (default 1): ") or 1
num = 0
for i4 in Datas['SEARCH'] :
    i4 = Datas['SEARCH'].split(":")
    try :
        if str(int(sel) - 1) == i4[num] :
            Datas['SELECTION'] = str(i4[num + 1])
            break
        else :
            num += 2
    except IndexError :
        print("choos a correct one !")
        sys.exit()
        break

def Read(Name, BodySave) :
    if (OS == 0) :
        os.system(f'less Articles/"Article {Name}.txt"')
    elif (OS == 1) :
        os.system("cls")
        print(BodySave)
    
def GetArticleValue(NameAR) :
    BodySave = ""
    BodyList = []
    query = NameAR
    text = ""
    Savename = query
    # I added this line for encoding Japanese routes
    query = urllib.parse.quote(query, encoding='utf-8')
    url = f"http://{cl}.wikipedia.org/wiki/{query}"
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
    sel = True if input("Do You Want to Save Article ? [y,n] ") == "y" else False
    SaveArticle(Savename, BodySave)
    # its a glitch def :)
    # ShellArticle(NameAR, BodySave)
    Read(NameAR, BodySave)
    if (sel == False) :
        os.remove(f"Articles/Article {NameAR}.txt")
GetArticleValue(Datas['SELECTION'])
