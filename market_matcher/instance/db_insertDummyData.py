import random
import sqlite3

conn = sqlite3.connect('market_matcher.db')
cursor = conn.cursor()

# Brands list
brands = ["BlueFarm", "AquaFresh", "SunBites", "EarthTaste", "GoldMark", "PureChoice", "QuickJoy", "NatureBox",
          "StarFoods", "GreenField"]

products = [
    ("Tomato", "Vegetable"),
    ("Milk", "Dairy"),
    ("Meat", "Meat"),
    ("Bread", "Bakery"),
    ("Soap", "Cleaning"),
    ("Butter", "Dairy"),
    ("Eggs", "Dairy"),
    ("Salt", "Seasoning"),
    ("Pepper", "Seasoning"),
    ("Sugar", "Bakery"),
    ("Water", "Beverage"),
    ("Cheese", "Dairy"),
    ("Yogurt", "Dairy"),
    ("Juice", "Beverage"),
    ("Coffee", "Beverage"),
    ("Tea", "Beverage"),
    ("Shampoo", "Cleaning"),
    ("Chicken", "Meat"),
    ("Rice", "Grain"),
    ("Noodles", "Grain"),
    ("Spaghetti", "Grain"),
    ("Olive Oil", "Oil"),
    ("Toothpaste", "Cleaning"),
    ("Apples", "Fruit"),
    ("Bananas", "Fruit"),
    ("Potatoes", "Vegetable"),
    ("Onions", "Vegetable"),
    ("Toilet Paper", "Cleaning"),
    ("Biscuits", "Bakery"),
    ("Cookies", "Bakery"),
    ("Cake", "Bakery"),
    ("Wine", "Beverage"),
    ("Beer", "Beverage"),
    ("Fish", "Seafood"),
    ("Beef", "Meat"),
    ("Lettuce", "Vegetable"),
    ("Corn", "Grain"),
    ("Carrots", "Vegetable"),
    ("Peas", "Vegetable"),
    ("Pineapple", "Fruit"),
    ("Cherries", "Fruit"),
    ("Mangoes", "Fruit"),
    ("Pears", "Fruit"),
    ("Oranges", "Fruit"),
    ("Peaches", "Fruit"),
    ("Strawberries", "Fruit"),
    ("Cereal", "Grain"),
    ("Oats", "Grain"),
    ("Chips", "Snack"),
    ("Salsa", "Seasoning"),
    ("Tuna", "Fish"),
    ("Sardines", "Fish"),
    ("Jam", "Spread"),
    ("Honey", "Spread"),
    ("Chocolate", "Snack"),
    ("Ice Cream", "Dairy"),
    ("Frozen Pizza", "Frozen"),
    ("Grapes", "Fruit"),
    ("Lemon", "Fruit"),
    ("Lime", "Fruit")
]

markets = ["Market A", "Market B", "Market C", "Market D", "Market E"]

# Market Groups
group1 = ["Market A", "Market C"]
group2 = ["Market B"]
group3 = ["Market D", "Market E"]

market_groups = group1 + group2 + group3

# Delete all items from the table
cursor.execute("DELETE FROM product;")

# Loop to generate the INSERT statements
# Loop to generate the INSERT statements
for product, category in products:
    chosen_market = random.choice(markets)

    # Determine the market group based on the selected market
    if chosen_market in group1:
        market_group = "Wal-Smart"
    elif chosen_market in group2:
        market_group = "Wal-Is-InMart"
    elif chosen_market in group3:
        market_group = "Mara-IsMara"
    else:
        market_group = None  # Just in case, though this shouldn't occur with the data provided

    brand = random.choice(brands)
    price = round(random.uniform(0.99, 19.99), 2)

    query = f"""
            INSERT INTO product (product_name, market, price, category, brand, market_group) 
            VALUES ('{product}', '{chosen_market}', {price}, '{category}', '{brand}', '{market_group}');
            """
    cursor.execute(query)

conn.commit()
conn.close()