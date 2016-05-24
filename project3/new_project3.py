# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET 
import pprint as pp
import re
from collections import defaultdict
import codecs
import json
import os
from dateutil import parser
import gc
file_path=r'D:\github\udacity_data_analyse\project3\report/new-york_new-york.osm'
capital=re.compile(r'^[A-Z]$')
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
direction=["S","W","N","E"]
expected_types = ["Street", "Avenue", "Boulevard", "Drive",
            "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Circle",
            "Cove", "Highway", "Park", "Way", "South",'Green','Loop','North','Plaza','West','Terrace','Walk','East','Crescent',"Center",'Broadway','Roadbed','Path']
mapping={
'CIRCLE':"Circle",
'ROAD':"Road",
'Rd':"Road",
'St':"Street",
'St.':"Street",
'street':"Street",
"ST":"Street",
'Streeet':"Street",
'Steet':"Street",
'STREET':"Street",
'avenue':"Avenue",
'AVENUE':"Avenue",
'Ave':"Avenue",
'Ave.':"Avenue",
'Ave,':"Avenue",
'AVenue':"Avenue",
'DRIVE':"Drive",
'Tirnpike':"Turnpike",
'Turnlike':"Turnpike",
'Tunrpike':"Turnpike",
'Tunpike':"Turnpike",
'Tpke':"Turnpike",
"S":"South",
'SOUTH':"South",
"N":"North",
"W":"West",
"E":"East",
'LANE':"Lane"
}
def audit_street_type(street_types, street_name):
    """
    Adds potentially problematic street names to
    list 'street_types'
    """
    m = street_type_re.search(street_name)
    word_list=street_name.split()
    n=capital.match(word_list[-1])
    if m:
        street_type = m.group()
        if street_type not in expected_types:
            try:
                if word_list[-2]=="Avenue" and n:
                    pass
                else:
                    street_types[street_type].add(street_name)
            except IndexError:
                pass
def audit_postcode(file_path):
    osm_file = open(file_path, "r")
    parser = ET.iterparse(osm_file, events=("start",))
    problematic_postcode = {}
    for event, elem in parser:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode":
                    try:
                        int(tag.attrib['v'])
                    except ValueError:
                        if tag.attrib['v'] in problematic_postcode:
                            problematic_postcode[tag.attrib['v']] += 1
                        else:
                            problematic_postcode[tag.attrib['v']] = 1
    return problematic_postcode

def is_street_name(tag):
    return (tag.attrib['k'] == "addr:street")
def audit(file_path):
    """
    Returns unexpected street types with a dictset
    """
    osm_file = open(file_path, "r")
    street_types = defaultdict(set)
    parser = ET.iterparse(osm_file, events=("start",))
    for event, elem in parser:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types
def count_tags(filename):
    data = {}
    for each in ET.iterparse():
        if each.tag in data:
            data[each.tag] += 1
        else:
            data[each.tag] = 1
    return data
def update_name(name, mapping):
    word_list=name.split()
    if word_list[-1] in mapping:
        word_list[-1]=mapping[word_list[-1]]
    if word_list[-1] in direction and word_list[-2] !="Avenue":
        word_list[-1]=mapping[word_list[-1]]
    name=" ".join(word_list)
    return name
def mapping_name(elem):
    for tag in elem.iter("tag"):
        if is_street_name(tag):
            tag.attrib["v"]=update_name(tag.attrib["v"],mapping)
    return elem
    elem.clear()
def update_postcode(elem):
    for tag in elem.iter("tag"):
        if tag.attrib['k'] == "addr:postcode":
            try:
                int(tag.attrib['v'])
            except ValueError:
                tag.attrib['v']=tag.attrib['v'].strip("NY ")
    return elem
    
def find_addr_keys(tree):
    root=tree.getroot()
    keys_list=set()
    for elem in root.getchildren():
        if elem.getchildren():
            for tag in elem.getchildren():
                if tag.tag=="tag":
                    if "addr:" in tag.attrib["k"]:
                        keys_list.add(tag.attrib["k"].strip("addr:"))    
    return keys_list
    
def shape_element(element):
    obj={}
    created={}
    address={}
    node_refs=[]
    lat=0.
    lon=0.
    address_keys=["street","postcode","housenumber","city","state","country"]
    created_keys=["version","changeset","timestamp","user","uid"]
    if element.tag == "node" or element.tag == "way" :
        for attrib in element.attrib:
            if attrib in created_keys:
                if attrib=="timestamp":
                    datestamp=parser.parse(element.attrib[attrib])
                    created[attrib]=datestamp
                    created["year"]=datestamp.year
                    date_string=str(datestamp.year)+"."+str(datestamp.month)+"."+str(1)
                    created["month"]=parser.parse(date_string)           
                else:
                    created[attrib]=element.attrib[attrib]
            elif attrib=="lat":
                lat=float(element.attrib[attrib])
            elif attrib=="lon":
                lon=float(element.attrib[attrib])
        if element.getchildren():
            element=mapping_name(update_postcode(element))
            for tag in element.getchildren():
                if tag.tag=="nd":
                    node_refs.append(tag.attrib["ref"])
                if tag.tag=="tag":
                    if "addr:" in tag.attrib["k"] and tag.attrib["k"].strip("addr:") in address_keys:
                        address[tag.attrib["k"].strip("addr:")]=tag.attrib["v"]
        if created:
            obj["created"]=created
        if address:
            obj["address"]=address
        if lat !=0. or lon!=0.:
            obj["position"]=[lat,lon]
        if node_refs:
            obj["node_refs"]=node_refs
        obj["type"]=element.tag
        obj["id"]=element.attrib["id"]                          
        return obj
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            element = shape_element(element)
            if element:
                element["created"]["timestamp"]=str(element["created"]["timestamp"])
                element["created"]["month"]=str(element["created"]["month"])
                data.append(element)
                if pretty:
                    fo.write(json.dumps(element, indent=2)+"\n")
                else:
                    fo.write(json.dumps(element) + "\n")
                element.clear()
    return data
#def insert_data_into_mongodb(element,collection):
#    collection.insert(element)
def find_some_element(file_path):
    with open(file_path,"r") as f:
        for _, element in ET.iterparse(f):
            if element.getchildren():
                for tag in element.getchildren():
                    if tag.attrib['k'] == "addr:postcode":
                        return element
                        break
    
if __name__ == '__main__':
    # In this part, i tried to import the data with insert, but error always occur. then i use mongoimport
    
    #for _,elem in ET.iterparse(file_path):
    #    document=shape_element(elem)
    #    if document:
    #        db.map_collection.insert(document)
    #        elem.clear()
    #some_node=db.map_collection.find_one({'id': '26769784'})
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.udacity_db
    size1=os.path.getsize(file_path)
    size2=os.path.getsize(file_path+".json")
    print file_path,"------","{0:.2f}".format(float(size1)/1024**2)+" MB"
    print file_path+".json","------","{0:.2f}".format(float(size2)/1024**2)+" MB"
    group_by_year=db.map_collection.aggregate([{"$match":{"created.year":{"$exists":1}}},{"$group":{"_id":"$created.year", "count":{"$sum":1}}},{"$sort":{"_id":-1}}])
    group_by_city=db.map_collection.aggregate([{"$match":{"address.city":{"$exists":1}}},{"$group":{"_id":"$address.city", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":10}])
    group_by_month=db.map_collection.aggregate([{"$match":{"created.month":{"$exists":1}}},{"$group":{"_id":"$created.month", "count":{"$sum":1}}},{"$sort":{"_id":-1}}])
    db.map_collection.find().count()#Number of documents
    db.map_collection.find({"type":"node"}).count()#Number of nodes
    db.map_collection.find({"type":"way"}).count()#Number of ways
    len(db.map_collection.distinct("created.user"))#Number of unique users
    for user in db.map_collection.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}]):
        print user # top1 contributor
    for a in db.map_collection.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}]):
        print a #number of user who only post once
        


