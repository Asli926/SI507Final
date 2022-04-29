# encoding = utf - 8
# author = Aishan Li

import os
import re
from bs4 import BeautifulSoup
import sqlite3
import numpy as np

price_range_pattern = re.compile(r"(\d+,*\d+) - (\d+,*\d+)")
single_price_pattern = re.compile(r"(\d+)")
beds_pattern = re.compile(r"(\d|Studio)\s*-\s*(\d)\s+Bed")
single_bed_pattern = re.compile(r"(\d)")

property_map = {"Dog Friendly": "Dog Friendly", "Cat Friendly": "Cat Friendly",
                "In Unit Washer & Dryer": "In Unit Washer & Dryer",
                "Dishwasher": "Dishwasher", "Parking": "Parking",
                "Fitness Center": "Fitness Center"}

property_list = ["Dog Friendly", "Cat Friendly", "In Unit Washer & Dryer",
                 "Dishwasher", "Parking", "Fitness Center"]
            
city_map_r = {"ann-arbor-mi": "Ann Arbor", "san-francisco-ca": "San Francisco", 
              "chicago-il": "Chicago", "detroit-mi": "Detroit", "seattle-wa": "Seattle", 
              "los-angeles-ca": "Los Angeles", "washington-dc": "Washington"}

def processRawHtml(city, page_num):
    with open(os.path.join("data", city, page_num + ".html"), mode='r', encoding='utf-8') as f:
        html_str = f.read()

    soup = BeautifulSoup(html_str, 'html.parser')
    builk_info, agent_info = [], []
    for li in soup.find_all("li", attrs={"class" : "mortar-wrapper"}):
        soup2 = BeautifulSoup(str(li), 'html.parser')
        
        apart = soup2.find_all("div", attrs={"class": "content-wrapper"})[0]
        apart_info_dict = {"city": city_map_r[city]}

        top_content = apart.contents[1]
        if top_content.text: 
            top_list = top_content.text.split('\n')
            apart_info_dict["price_range"] = top_list[2]
            apart_info_dict["beds"] = top_list[3]
        else:
            continue

        content = apart.contents[3]
        if "aria-label" in content.attrs: loc = content.attrs["aria-label"]
        else:                             loc = "None"

        apart_info_dict["location"] = loc
        properties = content.text.split('\n')
        for property in properties:
            if property in property_list:
                apart_info_dict[property] = True

        info = convert_apart_dict(apart_info_dict)
        builk_info.append(info)

        agent = "None"
        if soup2.find_all("div", attrs={"class": "property-logo"}):
            agent = soup2.find_all("div", attrs={"class": "property-logo"})[0].attrs['aria-label']
        agent_info.append([agent])
        
    return builk_info, agent_info


def convert_apart_dict(info_dict):
    res = [info_dict["location"]]

    price_match = price_range_pattern.search(info_dict["price_range"])
    # print(info_dict["price_range"])
    if price_match:
        low = price_match.group(1)
        high = price_match.group(2)
    else:
        price_match = single_price_pattern.search(info_dict["price_range"])
        if price_match:
            low = high = price_match.group(1)
        else:
            low = high = '0'

    bed_match = beds_pattern.search(info_dict["beds"])
    if bed_match:
        small = bed_match.group(1)
        large = bed_match.group(2)
    else:
        bed_match = single_bed_pattern.search(info_dict["beds"])
        if bed_match:
            small = large = bed_match.group(1)
        elif info_dict["beds"] == "Studio":
            small = large = 1

    res.extend([int_p(low), int_p(high), int_b(small), int_b(large)])

    for p in property_list:
        res.append(p in info_dict)
    
    res.append(info_dict["city"])

    return res


def int_p(price):
    return int("".join(price.split(",")))


def int_b(bed):
    if bed == "Studio":
        return 1
    else:
        return int(bed)
    

def createTable():
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()

    sql_file = open("BuildApartments.sql")
    sql_as_string = sql_file.read()
    cur.executescript(sql_as_string)

    con.commit()
    con.close()


def saveBuilk(builk_info, agent_info, con):
    cur = con.cursor()
    cur.executemany('INSERT or IGNORE INTO AGENTS VALUES (NULL, ?)', agent_info)
    for i,agent in enumerate(agent_info): 
        for row in cur.execute('SELECT AID FROM AGENTS WHERE AGENT = (?)', (agent[0],)):
            builk_info[i].append(row[0])
            break
    cur.executemany('''
        INSERT INTO APARTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', builk_info)


def saveOneCity(city_code, total_page):
    con = sqlite3.connect('Apartments.db')
    for p in range(1, total_page):
        builk_info, agent_info = processRawHtml(city_code, str(p))
        saveBuilk(builk_info, agent_info, con)
    con.commit()
    con.close()


if __name__ == '__main__':
    # createTable()
    saveOneCity("washington-dc", 29)
    print("success")

    # chicago-il 29, san-francisco-ca 29, detroit 26,  
    # Seattle 29, Washington 29, Los Angeles 29 (after +1)
