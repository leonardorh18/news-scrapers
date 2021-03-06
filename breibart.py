# -*- coding: utf-8 -*-
"""breibart

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lzWVotDgJWvaOK7_j1tjeo-b7a3WPTaO
"""

from bs4 import BeautifulSoup
import requests 
import re
from datetime import date
import pandas as pd
today = date.today()
from google.colab import drive

drive.mount('/content/drive')

"""## pra valer"""

def removeTN(text):
  regex = re.compile(r'[\n\r\t]')
  text = regex.sub("", text)
  return text

#categorias = ['politics','entertainment', 'the-media', 'economy','tech','sports', 'europe','latin-america']
#categorias = ['the-media', 'economy','tech','sports', 'europe','latin-america']
categorias = ['tech','sports', 'europe','latin-america']
newsDict = {'content': [],'date': [],'author': [] , 'resume': [], 'link': [], 'categoria': [] }

salvar_a_cada = 30
save = 0 
done = False
show = False
for categoria in categorias:
  print("CATEGORIA --- ", categoria)
  for pagenum in range(1,1000):
    if done:
      done = False
      break
    try:
      page = requests.get('https://www.breitbart.com/'+categoria+'/page/'+str(pagenum)+'/')
      soup = BeautifulSoup(page.content, 'html.parser')
      mydivs = soup.findAll("div", {"class": "tC"}, )
      for div in range(len(mydivs)):
        path = mydivs[div].find('a', href = True)
        link = 'https://www.breitbart.com'+path.attrs['href']
        
        #print("LINK --- {}".format(link))

        articlePage = requests.get(link)
        article = BeautifulSoup(articlePage.content, 'html.parser')

        DateAndAuthor = article.find('div', {'class':'header_byline'})
        date = DateAndAuthor.time.get_text()
        date = date.split(" ")
        if int(date[2]) <= 2019:
          print("chegou em 2019...")
          done = True
          break
        date = date[1]+" "+date[0]+" "+date[2]
        
        author = DateAndAuthor.a.get_text()
        
        resume = article.find('p', {'class':'subheading'})
        resume = removeTN(resume.get_text())

        content = article.find('div', {'class':'entry-content'})
        text = content.find_all('p')
        fullText = ''
        for t in range(1, len(text)):
          fullText +=  removeTN(text[t].get_text())
        
        newsDict['content'].append(fullText)
        newsDict['date'].append(date)
        newsDict['author'].append(author)
        newsDict['resume'].append(resume)
        newsDict['link'].append(link)
        newsDict['categoria'].append(categoria)
        #print(fullText)
        if show:
          
          print("Autor: {} e Data: {}".format(author, date))
          print("Resumo --- {}".format(resume))
          

        save+=1
        if save == salvar_a_cada:
          save =  0
          df = pd.DataFrame.from_dict(newsDict)
          print("salvando... {} ".format(date))
          df.to_csv('/content/drive/My Drive/datasets/breibart/dataset_saved_breibart.csv')
    except:
      print("Erro ", end = '')
      continue