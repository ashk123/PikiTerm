import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse

# Config (I make a config file soon)
inform_conf = False

# define section
VER = "1.9"
INST_PATH = "/home/ashkan/code/python/wiki/V2/pikiTerm"
OS = 0 if (sys.platform == "linux") else 0 if (sys.platform == "darwin") else 1 if (sys.platform == "win32") else 0
Language = 1
# 1 = EN
# 2 = JP
# 3 = FA
# 4 = EU
HELP = """pikiTerm Help --
--------------------------------
[!] What is pikiTerm ?
    pikiTerm is a wikipedia reader on terminal

[+] Run
    python3 main.py
    OR
    python3 main.py <content>

[+] Version
    python3 main.py -v
    OR
    python3 main.py --version

2022 ashk123/Eiko
-----------------------------"""

more =  [
    'en',
    'jp',
    'fa',
    'eu'
]

cl = more[Language - 1]

def SaveArticle(Name, Value, sa) :
    if (sa == False and OS == 1) :
        return False
    if not os.path.exists(f"{INST_PATH}/Articles") :
        os.mkdir(f"{INST_PATH}/Articles")
    with open(f"{INST_PATH}/Articles/Article {Name}.txt", "w", encoding="utf-8") as ar_file :
        ar_file.write(Value)
        ar_file.close()
    return True

def CheckArg(data) :
    els = ["--", "==", '-', '=']

    if (data == "-v" or data == "--version") :
        print(f"pikiTerm 2022 V{VER}")
        sys.exit()
    elif (data == "-h" or data == "--help") :
        print(HELP)
        sys.exit()
    else :
        for i in els :
            if (i in data) :
                print("Enter a valid content !")
                sys.exit()

Datas = {'SEARCH':'', 'TITLE':'', 'BODY':'', 'SELECTION':''}
if (len(sys.argv) > 1) :
    CheckArg(sys.argv[1])
    argv_user = ""
    for i in range(1, len(sys.argv)) :
        argv_user += sys.argv[i] + " "

    query = argv_user[:-1]
else :
    try :
        query = (input("Enter the Content : ") or False)
    except KeyboardInterrupt :
        print("\nyou cancel the proccess !")
        sys.exit()
if (query == False) :
    print("Enter valid content !")
    sys.exit()
elif (query == "q") :
    sys.exit()
url_search = f"https://{cl}.wikipedia.org/w/index.php?search={query}&title=Special:Search&profile=advanced&fulltext=1&ns0=1&searchToken=7637hhwf6zvrreb4qxzqjusdb"

res = requests.get(url_search)
soup = BeautifulSoup(res.text, "html.parser")
for i in range(5) :
    tag_span = soup.find("a", {'data-serp-pos':f'{str(i)}'})
    if (tag_span == None) :
        print("I finde anything !")
        sys.exit()
    date_inform = soup.find("div", "mw-search-result-data").get_text().split(",")[1];
    date_form = " -" + date_inform
    Datas['SEARCH'] += str(i)+":"+tag_span.get_text() + (date_form if (inform_conf == True) else "") + ":"

i2 = Datas['SEARCH'].split(":")
num = 0
for i3 in range(len(i2)) :
    try :
        print(str(int(i2[num]) + 1) + " -> " + i2[num + 1])
        num += 2
    except :
        pass
try :
    sel = input("\nEnter Selection (default 1): ") or 1
except KeyboardInterrupt :
    print("\nyou cancel the proccess !")
    sys.exit()
num = 0
if (sel == "q") :
    sys.exit()
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
    # Linux and MacOS
    if (OS == 0) :
        os.system(f'less {INST_PATH}/Articles/"Article {Name}.txt"')
    # Windows
    elif (OS == 1) :
        os.system("cls")
        print(BodySave)
    
def GetArticleValue(NameAR) :
    BodySave = ""
    BodyList = []
    query = NameAR
    text = ""
    Savename = query
    # I added this line for encoding Japanese or other routes
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
    sel = True if (input("Do You Want to Save Article [y,N]: ") or "n") == "y" else False
    SaveArticle(Savename, BodySave, sel)
    # its a glitch def :)
    # ShellArticle(NameAR, BodySave)
    Read(NameAR, BodySave)
    if (sel == False and OS == 0) :
        os.remove(f"{INST_PATH}/Articles/Article {NameAR}.txt")
GetArticleValue(Datas['SELECTION'])
