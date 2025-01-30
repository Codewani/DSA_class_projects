def tax(price):
    try:
        return price + (0.1044 * price)
    except:
        return -1

#automated tests
def test_tax_function():
    assert tax("a") == -1
    assert tax("ben") == -1
    assert float(tax(100)) == float(110.44)
    print("all test cases passed")

test_tax_function()
