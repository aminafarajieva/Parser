import requests
from bs4 import BeautifulSoup
import re
import itertools
import csv

url = 'https://www.kivano.kg/noutbuki'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
# типа пагинация ;)
lastpage = soup.find('li',class_='last') 
for v in range(1,int(lastpage.text)+1):
    response = requests.get(url+'?page='+str(v))
    soup = BeautifulSoup(response.text, 'lxml')
    names = soup.find_all('div', class_='listbox_title')
    links = soup.find_all('a', attrs={'href': re.compile("^/product/view/")})
    description = soup.find_all('div', class_='product_text pull-left')
    descrip = [i.text.split('\n') for i in description]
    descr = []
    for i in descrip:
        descr.append(i[4])
    # запись на csv
    p = open('kivano.csv','a')
    fieldnames = ['names on page '+str(v),'links on page '+str(v),'descriptions on page '+str(v)] 
    writer = csv.DictWriter(p, fieldnames=fieldnames)
    writer.writeheader()
    for i,j,k in zip(names,links,descr):
        writer.writerow({'names on page '+str(v):i.text,'links on page '+str(v):"https://www.kivano.kg"+j.get('href'),'descriptions on page '+str(v):k})
