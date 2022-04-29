# encoding = utf - 8
# author = Aishan Li
import sqlite3

class Tree:
    def __init__(self, pid=0, addr = "", price_l=0, price_h=0, bed_l=0, bed_h=0, 
                 dog=False, cat=False, in_uni=False, dishwasher=False, park=False, 
                 fitness=False, city="", aid=0, aid2=0, agent=""):
        self.addr = addr
        self.price_l = price_l
        self.price_h = price_h
        self.val = price_l + (price_h - price_l)/2 # mid_price
        self.bed_l = bed_l
        self.bed_h = bed_h
        self.dog = dog
        self.cat = cat
        self.in_uni = in_uni
        self.dishwasher = dishwasher
        self.park = park
        self.fitness = fitness
        self.agent = agent

        self.left = None
        self.right = None
    
    def insert(self, node):
        if node.val < self.val:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)
    
    def amenties_to_string(self):
        amenties = []
        if self.dog:        amenties.append("Dog Friendly")
        if self.cat:        amenties.append("Cat Friendly")
        if self.in_uni:     amenties.append("In Unit Washer&Dryer")
        if self.dishwasher: amenties.append("Dishwasher")
        if self.park:       amenties.append("Parking")
        if self.fitness:    amenties.append("Fitness")
        return ", ".join(amenties)
    

    def printNode(self):
        if self.price_l == 0:
            print("No results!")
            return
        print("Address: " + self.addr)
        print(f"Price: from {self.price_l} to {self.price_h} with bedrooms {self.bed_l}B - {self.bed_h}B")
        print(f"Real estate: {self.agent}")
        print("The apartment has the following amenities: ", end = "")
        print(self.amenties_to_string())
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    

    # traverse in pre-order
    def traverse(self):
        if self.left: self.left.traverse()
        self.printNode()
        if self.right: self.right.traverse()


    # traverse within a certain range
    def traverse_in_range(self, low, high):
        if self.val < low:
            if self.right: self.right.traverse_in_range(low, high)
            else:          return
        elif self.val > high:
            if self.left: self.left.traverse_in_range(low, high)
            else:         return
        else:
            if self.left: self.left.traverse_in_range(low, high)
            self.printNode()
            if self.right: self.right.traverse_in_range(low, high)
        

if __name__ == '__main__':
    # some examples, not used
    con = sqlite3.connect('Apartments.db')
    cur = con.cursor()
    root = Tree()
    c = cur.execute("SELECT AVG(PRICE_LOW), AVG(PRICE_HIGH) FROM CHICAGO;")
    for c0,c1 in c:
        root.val = (c0 + c1) / 2
        break
    for row in cur.execute("SELECT * FROM CHICAGO WHERE Dog_Friendly == 1;"):
        node = Tree(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
        root.insert(node)
    con.close()
