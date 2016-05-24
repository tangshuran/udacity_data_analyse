from bs4 import BeautifulSoup
html_page = "D:\github\udacity_data_analyse\project3\P3_PS2/Dat.html"
def extract_carriers(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html)
        carriers=soup.find(id="CarrierList")
        for i,option in enumerate(carriers.find_all("option")):
            if i <=2:
                pass
            else:
                data.append(option["value"])
    return data
ww=extract_carriers(html_page)
