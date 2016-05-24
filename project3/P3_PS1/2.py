#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports' function so that it returns a list of airport
codes, excluding any combinations like "All".
"""

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    soup = BeautifulSoup(page, "lxml")
    airports=soup.find(id="AirportList")
    for i,option in enumerate(airports.find_all("option")):
        if i <=1 or i == 15:
            pass
        else:
            data.append(option["value"])


    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()