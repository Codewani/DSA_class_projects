LOGO = f"{'='*60}{'\n\u2732  Walmart | Save money. Live better.\n'}{'='*60}"
products = {
    # Groceries
    "groceries": [
        {
            "index": 0,
            "name": "Apple",
            "brand": "Fresh Farms",
            "price": 1.99,
            "quantity": 10
        },
        {
            "index": 1,
            "name": "Organic Almond Milk",
            "brand": "Almond Bliss",
            "price": 3.49,
            "quantity": 5
        },
        {
            "index": 2,
            "name": "Whole Wheat Bread",
            "brand": "Baker's Delight",
            "price": 2.49,
            "quantity": 8
        },
        {
            "index": 3,
            "name": "Bananas",
            "brand": "Tropical Farms",
            "price": 0.59,
            "quantity": 15
        },
        {
            "index": 4,
            "name": "Frozen Peas",
            "brand": "Green Valley",
            "price": 2.99,
            "quantity": 7
        }
    ],
    
    # Appliances
    "appliances": [
        {
            "index": 0,
            "name": "Blender",
            "brand": "Ninja",
            "price": 89.99,
            "quantity": 3
        },
        {
            "index": 1,
            "name": "Dishwasher",
            "brand": "Bosch",
            "price": 499.99,
            "quantity": 2
        },
        {
            "index": 2,
            "name": "Electric Kettle",
            "brand": "Hamilton Beach",
            "price": 24.99,
            "quantity": 10
        },
        {
            "index": 3,
            "name": "Microwave Oven",
            "brand": "Panasonic",
            "price": 129.99,
            "quantity": 4
        },
        {
            "index": 4,
            "name": "Coffee Maker",
            "brand": "Keurig",
            "price": 89.99,
            "quantity": 6
        }
    ],

    # Clothes
    "clothes": [
        {
            "index": 0,
            "name": "Cotton T-Shirt",
            "brand": "Hanes",
            "price": 14.99,
            "quantity": 20
        },
        {
            "index": 1,
            "name": "Jeans",
            "brand": "Levi's",
            "price": 49.99,
            "quantity": 12
        },
        {
            "index": 2,
            "name": "Running Shoes",
            "brand": "Nike",
            "price": 79.99,
            "quantity": 8
        },
        {
            "index": 3,
            "name": "Winter Jacket",
            "brand": "North Face",
            "price": 199.99,
            "quantity": 5
        },
        {
            "index": 4,
            "name": "Sweatpants",
            "brand": "Adidas",
            "price": 29.99,
            "quantity": 15
        }
    ]
}

def tabulate_products(products):
    for category, product_list in products.items():
        print(f"\n----------- {category.upper()} ----------")

        # Determine the maximum width for each column
        col_widths = {
            "Index": 5,    # Fixed width for index
            "Name": max(len(product["name"]) for product in product_list),
            "Brand": max(len(product["brand"]) for product in product_list),
            "Price": 8,    # Fixed width for price
            "Quantity": 8  # Fixed width for quantity
        }
        
        # Print the header row
        header = " | ".join(key.ljust(col_widths[key]) for key in col_widths)
        print(header)
        print("-" * len(header))  # Separator line

        # Print the product rows
        for product in product_list:
            row_data = {
                "Index": str(product["index"]),
                "Name": product["name"],
                "Brand": product["brand"],
                "Price": f"${product['price']:.2f}",
                "Quantity": str(product["quantity"])
            }
            
            row = " | ".join(row_data[key].ljust(col_widths[key]) for key in col_widths)
            print(row)

# Example usage:
tabulate_products(products)

# item_name = []
# item_price = []



# # Function to calculate tax (10.44%)
def calculate_tax(price):
    tax_rate = 10.44 / 100
    return round(price * tax_rate, 2)  # Rounds tax to 2 decimal places

# # Function to handle shopping process
def shopping():
    cart = {}
    total_before_tax = 0
    while True:
        category = input("Enter a category (groceries, appliances, clothes): ").strip().lower()

        while category not in products:
            print("Invalid category. Please choose from groceries, appliances, or clothes.")
            category = input("Enter a category (groceries, appliances, clothes): ").strip().lower()
        
        print(f"\nHere are the {category} in our store: ")
        tabulate_products({f"{category}":products[category]})
        item = input("Enter the index of the item you want to buy or ('C'/'c') if you want to choose a different category: ")
        while (item != 'C' and item != 'c') and (not item.isdigit() or int(item) >= len(products[category])):
            print("\nINVALID ITEM INDEX. PLEASE ENTER A VALID INDEX")
            print(f"\nHere are the {category} in our store: ")
            tabulate_products({f"{category}":products[category]})
            item = input("Enter the index of the item you want to buy or ('C'/'c') if you want to choose a different category: ")

        if item == 'C' or item == 'c':
            continue
        item = int(item)

        quantity = input("Enter the quantity you want to buy: ")
        while not quantity.isdigit() or int(quantity) <= 0:
            print("\nInvalid quantity. Please enter a positive number.")
            quantity = input("Enter the quantity you want to buy: ")
        quantity = int(quantity)

        brand = products[category][item]["brand"]
        item_name = products[category][item]["name"]
        item_price = products[category][item]["price"]

        # calculate tax
        tax = calculate_tax(item_price)
        total_price_with_tax = item_price + tax
        previous_total = item_price * quantity

        if products[category][item]["quantity"] <= 0:
            print("Item is out of stock.")
            return
        elif quantity > products[category][item]["quantity"]:
            print("Insufficient quantity in stock.")
            return
        else:
            # Deduct item from stock
            products[category][item]["quantity"] -= quantity
            # total quantity with tax
            total_price_with_tax = total_price_with_tax * quantity
            total_before_tax += previous_total
            # Add item to cart with category
            cart[item_name] = {
                "price": total_price_with_tax,
                "brand": brand,
                "quantity": quantity,
                "category": category  # Add category to track items
            }
            print(f"\n{quantity} {item_name}(s) added to cart.")
            current_total = sum(item['price'] for item in cart.values())
            print(f"Current total: ${current_total:.2f}")

        ask_continue = input("Do you want to continue shopping? (yes/no): ").strip().lower()
        if ask_continue == "no":
            break
        elif ask_continue != "yes":
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

    # Print receipt
    print("\n" + "="*60)
    print("\u2732  Walmart Receipt")
    print("="*60)

    if not cart:
        print("No items purchased.")
    else:
        # Group items by category
        categorized_items = {"groceries": [], "appliances": [], "clothes": []}
        
        # Determine maximum widths for each column
        name_width = max(len(item) for item in cart.keys())
        brand_width = max(len(item['brand']) for item in cart.values())
        
        for item_name, details in cart.items():
            categorized_items[details['category']].append((item_name, details))

        # Print items by category
        for category in categorized_items:
            if categorized_items[category]:  # Only print categories that have items
                print(f"\n----------- {category.upper()} -----------")
                
                # Print header
                header = (
                    f"{'Item'.ljust(name_width)} | "
                    f"{'Brand'.ljust(brand_width)} | "
                    f"{'Quantity'.ljust(8)} | "
                    f"{'Price'.ljust(10)}"
                )
                print(header)
                print("-" * len(header))

                # Print items in this category
                for item_name, details in categorized_items[category]:
                    row = (
                        f"{item_name.ljust(name_width)} | "
                        f"{details['brand'].ljust(brand_width)} | "
                        f"{str(details['quantity']).ljust(8)} | "
                        f"${details['price']:.2f}".ljust(10)
                    )
                    print(row)

        # Print totals
        print("\n" + "="*60)
        print(f"Total price before tax: ${total_before_tax:.2f}")
        print(f"Total price after tax: ${current_total:.2f}")
        print(f"Tax amount: ${(current_total - total_before_tax):.2f}")
        print(f"Number of items purchased: {len(cart)}")
        print("="*60)
        print("Thank you for shopping with Walmart!")
        print("="*60)
        
shopping()
