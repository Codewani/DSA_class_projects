# List to store item names and prices
item_name = []
item_price = []



# Function to calculate tax (10.44%)
def calculate_tax(price):
    tax_rate = 10.44 / 100
    return round(price * tax_rate, 2)  # Rounds tax to 2 decimal places

# Function to handle shopping process
def shopping():
    budget = 100  # Budget Constraint 

    while budget > 0:
        
        item = input("\nEnter item's name: ").strip() # Get item name

        # Get valid price input
        while True:
            try:
                price = float(input("Enter item's price: "))  # Convert to float for decimals
                if price <= 0: # We want only positive price for the items
                    print("Price must be a positive number. Try again.")
                    continue
                break  # Exit loop if valid
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        # Calculate tax
        tax = calculate_tax(price)
        total_price_with_tax = price + tax

        # Check budget constraint
        if total_price_with_tax > budget:
            print(f"You don't have enough budget. Your remaining budget is ${budget:.2f}.")
            print("Try adding a cheaper item or go to checkout.")
            continue  # Prompt user again

        # Deduct from budget and store item
        budget -= total_price_with_tax
        item_name.append(item)
        item_price.append(price)

        # Print tax separately
        print(f"\n{item} added!")
        print(f"Price: ${price:.2f}")
        print(f"Tax: ${tax:.2f}")  # Prints tax before adding to total
        print(f"Total after tax: ${total_price_with_tax:.2f}")
        print(f"Remaining budget: ${budget:.2f}")

        # Ask if user wants to continue shopping
        prompt = input("\nDo you want to continue shopping? (Yes/No): ").strip().lower()
        while prompt not in ["yes", "no"]:
            print("Enter a valid response (Yes/No).")
            prompt = input("Do you want to continue shopping? (Yes/No): ").strip().lower()

        if prompt == "no":
            break  # Stop shopping

    # Print receipt
    print("\nThank you for shopping with Walmart!")
    if not item_name:
        print("No items purchased.")
    else:
        print("\nReceipt:")
        for i in range(len(item_name)):
            print(f"{item_name[i]} - ${item_price[i]:.2f}")
        
        total_before_tax = sum(item_price)
        total_after_tax = total_before_tax + sum(calculate_tax(price) for price in item_price)

        print(f"\nTotal price before tax: ${total_before_tax:.2f}")
        print(f"Total price after tax: ${total_after_tax:.2f}")
        print(f"Number of items purchased: {len(item_name)}")
        print(f"Final remaining budget: ${budget:.2f}")

# Running shopping function
shopping()
