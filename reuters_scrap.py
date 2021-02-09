# -*- coding: utf-8 -*-
"""reuters scrap

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e2Ovs7ejvRkn_M81ILtDu8bW97N17dKM
"""



from bs4 import BeautifulSoup
import requests 
import re
from datetime import date
import pandas as pd
today = date.today()
from google.colab import drive

drive.mount('/content/drive')

#categorias = ['technologynews', 'domesticnews', 'worldnews', 'businessnews', 'marketsNews', 'mcbreakingviews', 'lifestylemolt', 'politicsnews', 'ukdomestic', 'sciencenews', 'personalfinance']
categorias = ['worldnews', 'businessnews', 'marketsNews', 'mcbreakingviews', 'lifestylemolt', 'politicsnews', 'ukdomestic', 'sciencenews', 'personalfinance', 'environmentnews', 'rcomus_energy', 'bank-news', 'rcom-europe','com-media-telecoms']
#categorias = ['marketsNews', 'mcbreakingviews', 'lifestylemolt', 'politicsnews', 'sciencenews']
#categorias = ['mcbreakingviews', 'lifestylemolt', 'politicsnews', 'sciencenews']
def removeTN(text):
  regex = re.compile(r'[\n\r\t]')
  text = regex.sub("", text)
  return text

salvar_a_cada = 50
save = 0 
done = False
newsDict = {'content': [],'date': [],'author': [] , 'title': [], 'resume': [], 'link': [], 'categoria': [] }

for categoria in categorias:
  print(" ---- Categoria {}".format(categoria))
  for pagenum in range(1, 5000):

    if categoria == 'marketsNews':
      pagenum = 2530 + pagenum

    print(pagenum, end = ' ')
    if done:
      done = False
      break
    page = requests.get('https://www.reuters.com/news/archive/'+categoria+'?view=page&page='+str(pagenum)+'&pageSize=10')
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "story-content"}, )
    for div in range(len(mydivs)):
      try:
        #print("\n -- TITULO")
        titulo = mydivs[div].find('h3').get_text()
        titulo = removeTN(titulo)
        #print(titulo)
    
        date = mydivs[div].find("time").get_text()
        date = removeTN(date)

        if len(date.split(' ')) < 3:
          date = today.strftime("%b-%d-%Y")
          date = re.sub('-', ' ', date)
        datesplt = date.split(" ")

        if int(datesplt[2]) <= 2019:
          print("Chegamos em 2019...")
          done = True
          break

        #print("\n  --- DATA: {}".format(date))
        resumo = mydivs[div].find('p').get_text()
        resumo = removeTN(resumo)
        #print("--- RESUMO: {}".format(resumo))
        path = mydivs[div].find('a', href = True)
        link = 'https://www.reuters.com/'+path.attrs['href']
        #print('LINK {}'.format(link))

        articlePage = requests.get(link)
        article = BeautifulSoup(articlePage.content, 'html.parser')
        paragraphs = article.find_all('p', {'class': 'Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x'})
        author = article.find('p', {'class': 'Byline-byline-1sVmo ArticleBody-byline-10B7D'}).get_text()
        author = re.sub("By ", '', author)
        #print("----- AUTOR: {}".format(author))
        content = ' '
        for p in paragraphs:
          content = content + str(removeTN(p.get_text()))
      
        newsDict['content'].append(content)
        newsDict['date'].append(date)
        newsDict['link'].append(link)
        newsDict['author'].append(author)
        newsDict['title'].append(titulo)
        newsDict['resume'].append(resumo)
        newsDict['categoria'].append(categoria)
        save +=1
        if save == salvar_a_cada:
          save = 0
          df = pd.DataFrame.from_dict(newsDict)
          print("salvando... {} ".format(date))
          df.to_csv('/content/drive/My Drive/datasets/reuters/dataset_saved_reuters.csv')
      except:
        print("Erro... ", end = '' )

df = pd.DataFrame.from_dict(newsDict)
df.to_csv('/content/drive/My Drive/datasets/reuters/datasetreuters.csv')

df = pd.read_csv('/content/drive/My Drive/datasets/reuters/dataset_saved_reuters.csv')

df.shape

df.date[271]