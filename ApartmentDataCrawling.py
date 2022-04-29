# encoding = utf - 8
# author = Aishan Li

import os
import requests
from Constants import APARTMENT_SITE
import time

city_map_a = {"Ann Arbor": "ann-arbor-mi", "San Francisco": "san-francisco-ca", "Chicago": "chicago-il",
            "Detroit": "detroit-mi", "Seattle": "seattle-wa", "Los Angeles": "los-angeles-ca", 
            "Washington": "washington-dc"}

def get_raw_html(city, page_num):
    link = f"{APARTMENT_SITE}/{city}/{page_num}/"
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
        "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"'''
    }

    response = requests.get(link, headers=header)

    os.makedirs(os.path.join("data", city), exist_ok=True)

    with open(os.path.join("data", city, page_num + ".html"), mode='w', encoding="utf-8") as f:
        f.write(response.content.decode("utf-8") )


if __name__ == '__main__':
    for i in range(1, 29):
        time.sleep(1)
        get_raw_html(city_map_a["Los Angeles"], str(i))

    # chicago-il 29, san-francisco-ca 29, detroit 26,  
    # Seattle 29, Washington 29, Los Angeles 29 (after +1)

