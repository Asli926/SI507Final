# SI507Final

### Required Python Packages
requests, sqlite3, numpy, BeautifulSoup, matplotlib

### Getting Started
```
$ python3 UserInteract.py
Welcome to the apartment system!
```

### Interactive Process
```
City code: 1.Seattle 2.Ann Arbor 3.Detroit 4.Washington 5.San Francisco 6.Chicago 7.Los Angeles
Which city do you want to live? Type the number of the city. 
$ 2

Which real estate do you prefer? Type the company name or no.
$ Village Green

Are you looking for dog/cat-frendly apartments? Please type yes or no.
$ yes

Address: Pheasant Run Apartments, Ann Arbor, MI
Price: from 1 to 1 with bedrooms 1B - 2B
Real estate: Village Gree
The apartment has the following amenities: Dog Friendly, Cat Friendly, Dishwasher, Parking -----------------------------------
...

Input your expected range of each apartment's mean price as <low>,<high>:
$ 1,1000
Address: Pheasant Run Apartments, Ann Arbor, MI
Price: from 1 to 1 with bedrooms 1B - 2B
Real estate: Village Green
The apartment has the following amenities: Dog Friendly, Cat Friendly, Dishwasher, Parking

Do you want to exit? If not, you can choose the range again. Type yes or no please.
$ yes
```

See the report for the pipeline and figures.

### Data Structure & Data
#### Data Structure - Tree
Construct a **binary search tree** according to the average price of each apartment, so that the searching results can be shown in different orders or in a certain range quickly based on the users' needs.
```python
# cache.py
class Tree:
	# the constructor
    def __init__(self, pid=0, addr = "", price_l=0, price_h=0, bed_l=0, bed_h=0, 
                 dog=False, cat=False, in_uni=False, dishwasher=False, park=False, 
                 fitness=False, city="", aid=0, aid2=0, agent=""):
        self.addr = addr
        self.val = price_l + (price_h - price_l)/2 # mid_price
				(......)
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
... ...
```
#### Data
##### Database Screenshot
![avatar](https://github.com/Asli926/SI507Final/blob/main/db.png)
##### Data Cached Screenshot
The data is printed as shown in Interactive Process Part using the `printNode` function in cache.py