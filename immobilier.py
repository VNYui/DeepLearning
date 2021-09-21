from pathlib import Path
from bs4 import BeautifulSoup 
import requests

class Scraper:
  def __init__(self, url):
      self.url = url
      self.req = requests.get(self.url)
      self.soup = BeautifulSoup(self.req.content, "html5lib")
      self.id = self.get_id()
      self.title = self.get_title(self.id)
      self.price = self.get_rent(self.id)
      self.msquare = self.get_msquare(self.id)
      self.result()

  def result(self):
    for title, id,price,surface in zip(self.title,self.id, self.price,self.msquare):
      print(f"{title},{id},{price},{surface}")

  def get_id(self):
    #HTML CONTENT -> BS4 OBJECT
    data_id = []
    #RETRIEVE DATA ID FOR ANNOUNCE
    for x in self.soup.find_all(id='blocListAnnonces'):
      for y in x.find_all(id='listAnnonces'):
        for item in y.find_all(attrs={"data-id": True}):
          data_id.append(item['data-id'])
    return list(set(data_id))
  
  def get_rent(self, id):
    prices = []
    for x in id:
      for div_data in self.soup.find_all(attrs={'data-id': x }):
        for blocdesc in div_data.find_all('div', class_='annBlocDesc'):
          for price in blocdesc.find_all('span', class_='annPrix'):
            prices.append(price.text.strip())
    return prices

  def get_msquare(self,id):
    msquare = []
    for x in id:
      for div_data in self.soup.find_all(attrs={'data-id': x }):
        for crit in div_data.find_all('span', class_='annCriteres'):
          for y in crit.find_all('div'):
            msquare.append(y.text.strip())   

            
    return msquare
  def get_title(self,id):
    title = []
    for x in id:
      for div_data in self.soup.find_all(attrs={'data-id': x }):
        for crit in div_data.find_all('div', class_='annBlocDesc'):
          for span in crit.find_all('span', class_='annTitre'):
            title.append(span.text.strip())
    return title
if __name__ == '__main__':
    scraper = Scraper('https://www.ouestfrance-immo.com/immobilier/location/appartement/la-roche-sur-yon-85-85191/')

#
"""
bin_driver = Path.cwd() / 'driver/chromedriver.exe'
options = Options() 
options.binary_location = bin
bin_brave = "C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave.exe"
driver = webdriver.Chrome()
driver.get("https://www.leboncoin.fr/recherche?category=10&locations=La%20Roche-sur-Yon_85000__46.672_-1.42739_8296")
sleep(10) 

"""