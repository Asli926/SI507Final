# author = Aishan Li
import sqlite3
import numpy as np

cities = ["Seattle", "Ann Arbor", "Detroit",  "Washington",
          "San Francisco", "Chicago", "Los Angeles"]

# linear interpolation, return [bed1, bed2, bed3]
def processPrice(p_l, p_h, b_l, b_h):
    fp, xp = [p_l, p_h], [b_l, b_h]
    res = np.interp([1, 2, 3], xp, fp)
    res[b_h:] = [0] * (3 - b_h) # If the information not included, set it to zero
    return list(res)

# store average price of different cities with respect to 1Bedroom, 2Bedrooms, 3Bedrooms
if __name__ == '__main__':
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()
    
    # city : price
    for c in cities:

        price_total = {"b1":0, "b2":0, "b3":0}
        aparts_num = {"b1":0, "b2":0, "b3":0}
        for row in cur.execute('''
                                    SELECT PRICE_LOW, PRICE_HIGH, BED_LOW, BED_HIGH
                                    FROM APARTS A
                                    WHERE A.CITY = ?
                               ''', (c,)):
            li = processPrice(*row)
            # Exclude the situation that bed price equals zero (No such information)
            for i, price in enumerate(li):
                if price != 0:
                    price_total["b" + f"{i+1}"] += price
                    aparts_num["b" + f"{i+1}"] += 1

        b1 = int(price_total['b1']/aparts_num['b1'])
        b2 = int(price_total['b2']/aparts_num['b2'])
        b3 = int(price_total['b3']/aparts_num['b3'])

        cur.execute('''
                        INSERT INTO STATS VALUES (NULL, ?, ?, ?, ?) 
                    ''', (c, b1, b2, b3))
        
    con.commit()
    con.close()
