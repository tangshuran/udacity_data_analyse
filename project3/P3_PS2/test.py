import requests
from bs4 import BeautifulSoup
#html_page = "D:\github\udacity_data_analyse\project3\P3_PS2/Data_Elements.html"

#f=BeautifulSoup(html_page.text)
def extract_carriers(page):
    data = []
    soup = BeautifulSoup(page.text,'html.parser')
    carriers=soup.find(id="CarrierList")
    for i,option in enumerate(carriers.find_all("option")):
        if i <=2:
            pass
        else:
            data.append(option["value"])
    return data
def extract_airports(page):
    data = []
    soup = BeautifulSoup(page.text,'html.parser')
    airports=soup.find(id="AirportList")
    for i,option in enumerate(airports.find_all("option")):
        if i <=1 or i == 15:
            pass
        else:
            data.append(option["value"])
    return data
def ee():
    print "ee"
if __name__ == "__main__":
    html_page=requests.request("get","http://www.transtats.bts.gov/Data_Elements.aspx?Data=2")
    ee()