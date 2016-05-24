import requests
from bs4 import BeautifulSoup
html_page = "D:\github\udacity_data_analyse\project3\P3_PS2/Data Elements.html"
f=open(html_page,"r")
#html_page=requests.request("get","http://www.transtats.bts.gov/Data_Elements.aspx?Data=2")
#soup = BeautifulSoup(html_page.text,'html.parser')
soup=BeautifulSoup(f)
form=soup.find(id="CarrierList")