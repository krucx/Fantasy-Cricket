from bs4 import BeautifulSoup
import requests
import re

def Get_text(link,innings):

    html_text = requests.get(link).text

    soup = BeautifulSoup(html_text,'lxml')
    f = []

    for i in range(1,innings+1):
            first_innings = soup.find('div',id='innings_'+str(i))
            scorecard = first_innings.find('div',class_ = 'cb-col cb-col-100 cb-ltst-wgt-hdr')

            rows = scorecard.find_all('div',class_ = 'cb-col cb-col-100 cb-scrd-itms')

            for row in rows:
                try:
                    name = row.a.text.strip()
                    f.append(name)

                    wicket = row.find('span',class_ = 'text-gray').text.strip()
                    f.append(wicket)

                    runs = row.find('div',class_ = 'cb-col cb-col-8 text-right text-bold').text.strip()
                    f.append(runs)

                    balls = row.find('div',class_ = 'cb-col cb-col-8 text-right').text.strip()
                    f.append(balls)

                    f.append('Ignore')
                    f.append('Ignore')
                    f.append('Ignore')
                except:
                    break
    return f

def getBowlerPts(bowler,players,wickets):
    i=0
    while i<len(bowler):
        if bowler[i].strip()=="b":
            players[bowler[i+1].strip()] = players.get(bowler[i+1].strip(),0) + 25
            wickets[bowler[i+1].strip()] = wickets.get(bowler[i+1].strip(),0) + 1
        elif bowler[i].strip()=="st":
            players[bowler[i+1].strip()] = players.get(bowler[i+1].strip(),0) + 10
        elif bowler[i].strip()=="run out":
            bnames = re.sub('[()]', '', bowler[i+1])
            bow = bnames.split('/')
            for j in bow:
                players[j.strip()] = players.get(j.strip(),0) + 10
        i+=1

def cleanDict(dict):
    newDict = {}
    for i in dict:
        if len(i.split())>1:
            if dict.get(' '.join(i.split()[1:]),-1000) == -1000:
                newDict[i]=dict[i]
            else:
                newDict[' '.join(i.split()[1:])] = dict[i]+dict[' '.join(i.split()[1:])]
        else:
            newDict[i]=dict[i]
    return newDict


def printDict(dict):
    text = []
    for i in dict:
        text.append([i,dict[i]])
    return text

def mom(link,players):
    mom_link = link.replace('live-cricket-scorecard','live-cricket-scores')
    html_text = requests.get(mom_link).text
    soup = BeautifulSoup(html_text,'lxml')
    try:
        x = soup.find("a",class_="cb-link-undrln").text.strip()
        if players.get(x,-1000) != -1000:
            players[x]+=15
    except:
        return


def openfile(f,innings,link):
    count=0
    bat_name=""
    players={}
    wickets={}
    for line in f:
      if count%7==0:
        bat_name = re.sub(r'\([^)]*\)', '', line)
        bat_name = bat_name.strip()
      elif count%7==1:
        bowler = re.split('(^c\s|\sb\s|^b\s|^st\s|\sst\s|^run out\s)',line)
        getBowlerPts(bowler,players,wickets)
      elif count%7==2:
        runs = int(line)
        players[bat_name] = players.get(bat_name,0) + runs*2 + 25*(runs>=50) + 25*(runs>=100)
      elif count%7==3:
        balls = int(line)
        players[bat_name] = players.get(bat_name,0) + (-balls)*(innings<=2) + (balls/2-runs)*(innings>2)
      count+=1
    new = {}
    for i in wickets:
        if wickets[i]>=3:
            players[i] = players[i] + 25
        if wickets[i]>=5:
            players[i] = players[i] + 25
    mom(link,players)
    new = cleanDict(players)
    text = printDict({k: v for k, v in sorted(new.items(), key=lambda item: item[1],reverse=True)})
    return text
