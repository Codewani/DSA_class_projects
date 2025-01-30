item_name = []
item_price = []

def validation():
    budget = 100

    while budget > 0:
        item = input("\nEnter item's name: ").strip()
        try:
            price = int(input("Enter item's price: "))
            if price > budget:
                print(f"\nYou don't have enough money left. Your remaining budget is {budget}$. Go to Cart.")
                continue
        except ValueError:
            print("\nPlease enter a valid numeric value for the price.")
            continue

        budget -= price
        item_name.append(item)
        item_price.append(price)

        print(f"\nYou have {budget}$ left in your wallet.")

        if budget == 0:
            print("\nYour budget is fully used up.")
            break

        prompt = input("\nDo you want to continue shopping (Yes/No): ").lower().strip()

        while prompt != "yes"and prompt != "no":
            print("\nEnter a valid response (Yes/No).")
            prompt = input("\nDo you want to continue shopping (Yes/No): ").lower().strip()

        if prompt == "no":
            break

    print("\nThank you for shopping with Walmart!")
    print("\nItems Purchased:")
    for i in range(len(item_name)):
        print(f"{item_name[i]} - ${item_price[i]}")

    print(f"\nFinal remaining budget: {budget}$")


validation()

def tax(price):
    try:
        return (0.1044 * price)
    except:
        return -1

#automated tests
def test_tax_function():
    assert tax("a") == -1
    assert tax("ben") == -1
    assert float(tax(100)) == float(10.44)
    print("all test cases passed")

test_tax_function()
