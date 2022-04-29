# author = Aishan Li
import matplotlib.pylab as plt
import numpy as np
import sqlite3
from cache import Tree

cities = ["None", "Seattle", "Ann Arbor", 
          "Detroit", "Washington", "San Francisco", 
          "Chicago", "Los Angeles"]

def showPicOne():
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()
    labels, b1, b2, b3, i = [], [], [], [], 1
    for row in cur.execute('''SELECT * FROM STATS;'''):
        labels.append(f'{i}: ' + row[1])
        b1.append(row[2])
        b2.append(row[3])
        b3.append(row[4])
        i += 1
    con.close()

    # color = ["#FF6666","#FFFF00","#99CC33","#0099CC", '#FF9966', "#0066CC", "#336699"]

    plt.figure(figsize=(13, 4))
    x = np.arange(len(labels))
    width = 0.25

    plt.bar(x - width, b1, width, label='1B', color = ["#FF6666"])
    plt.bar(x, b2, width, label='2B', color = ["#FFFF00"])
    plt.bar(x + width, b3, width, label='3B', color = ["#0099CC"])

    plt.ylabel('Rent')
    plt.title("Average apartment rent in cities")
    plt.xticks(x, labels=labels)
    plt.legend()

    plt.show()


def showPicTwo(city):
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()
    
    agent, count = [], []
    AgentOfCitySql = """
                        SELECT A2.AGENT, COUNT (*)
                        FROM APARTS A1, AGENTS A2
                        WHERE A1.CITY = ? AND A1.AID = A2.AID
                        GROUP BY A2.AGENT
                     """
    for row in cur.execute(AgentOfCitySql, (city,)):
        if row[0] == 'None': continue
        agent.append(row[0])
        count.append(row[1])
    con.close()

    Z = zip(count, agent)
    Z = sorted(Z, reverse=True)
    count, agent = zip(*Z)
    count, agent = list(count), list(agent)

    count_top, agent_top = count, agent
    if len(agent) > 10:
        count_top = count[0:10] + [sum(count[10:])]
        agent_top = agent[0:10] + ["Other"]

    explode = [0.2]*len(agent_top)
    plt.figure(figsize=(10, 6))
    plt.pie(count_top, labels = agent_top, autopct='%.2f%%', explode=explode)
    plt.show()

if __name__ == '__main__':
    print("Welcome to the apartment system!")
    showPicOne()

    print("City code: 1.Seattle 2.Ann Arbor 3.Detroit 4.Washington 5.San Francisco 6.Chicago 7.Los Angeles")
    city = cities[int(input("Which city do you want to live? Type the number of the city. \n"))]
    showPicTwo(city)

    agent = input("Which real estate do you prefer? Type the company name or no. \n")
    has_pet = input("Are you looking for dog/cat-frendly apartments? Please type yes or no. \n")

    sql_str =   f"""SELECT *
                    FROM APARTS A1, AGENTS A2
                    WHERE A1.AID = A2.AID AND A1.CITY = "{city}" """
    
    if agent != "no":     sql_str += ("AND A2.AGENT = \"" + agent + "\" ")
    if has_pet == "yes":  sql_str += "AND (A1.Dog_Friendly = 1 OR A1.Cat_Friendly = 1)"
    sql_str += ";"

    # Cache the content using a Binary Search Tree struction.
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()
    root = Tree()
    root.val = 2000
    for row in cur.execute(sql_str):
        node = Tree(*row)
        node.printNode()
        root.insert(node)
    con.close()

    # Show the data to the user.
    root.traverse()
    while True:
        low, high = input("Input your expected range of each apartment's mean price as <low>,<high>: \n").split(",")
        root.traverse_in_range(int(low), int(high))
        exit = input("Do you want to exit? If not, you can choose the range again. Type yes or no please. \n")
        if exit == "yes": break
