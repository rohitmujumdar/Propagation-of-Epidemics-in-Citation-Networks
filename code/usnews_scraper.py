import requests
from bs4 import BeautifulSoup

newheaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64)'
}

baseurl = 'https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings'

page1 = requests.get(baseurl, headers = newheaders) # change headers or get blocked 
soup = BeautifulSoup(page1.text, 'lxml')
res_tab = soup.find('div', {'id' : 'resultsMain'}) # find the results' table

for a,univ in enumerate(res_tab.findAll('a', href = True)): # parse universities' names
    if a < 10: # there are 10 listed universities per page
        print(univ.text)