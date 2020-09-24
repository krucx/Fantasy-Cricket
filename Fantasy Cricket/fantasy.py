from tkinter import *
from tkinter import filedialog
import re

root = Tk()
root.title("Fantasy Gaming")

players={}

def getBowlerPts(bowler):
  i=0
  while i<len(bowler):
    if bowler[i].strip()=="b":
      players[bowler[i+1].strip()] = players.get(bowler[i+1].strip(),0) + 25
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
      if dict.get(i.split()[-1],-1000) == -1000:
        newDict[i]=dict[i]
      else:
        newDict[i.split()[-1]] = dict[i]+dict[i.split()[-1]]
    else:
      newDict[i]=dict[i]
  return newDict


def printDict(dict):
  text = []
  text.append("{:<30}\t{:<5}\n\n".format('players','points'))
  for i in dict:
    text.append("{:<30}\t{:<5}\n".format(i,dict[i]))
  return ''.join(text)

def clear():
  my_label.pack_forget()

def openfile():
  root.filename = filedialog.askopenfilename(title="Select a file",filetypes=(("txt files","*.txt"),("all files","*.*")))
  count=0
  bat_name=""
  players={}
  with open(root.filename,'r') as f:
    lines = f.readlines()
    for line in lines:
      if count%7==0:
        bat_name = re.sub(r'\([^)]*\)', '', line)
        bat_name = bat_name.strip()
      elif count%7==1:
        bowler = re.split('(^c\s|\sb\s|^b\s|^st\s|^run out\s)',line)
        getBowlerPts(bowler)
      elif count%7==2:
        runs = int(line)
        players[bat_name] = players.get(bat_name,0) + runs*2 + 25*(runs>=50) + 25*(runs>=100)
      elif count%7==3:
        balls = int(line)
        players[bat_name] = players.get(bat_name,0) - balls
      count+=1
  new = {}
  new = cleanDict(players)
  text = printDict({k: v for k, v in sorted(new.items(), key=lambda item: item[1],reverse=True)})
  global my_label
  my_label = Label(root,text=text)
  my_label.pack()
  
my_btn = Button(root,text="open file",command=openfile)
my_btn.pack()
btn1 = Button(root,text="clear",command=clear)
btn1.pack()

root.mainloop()
