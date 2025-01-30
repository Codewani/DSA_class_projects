def tax(price):
    try:
        return (0.1044 * price)
    except:
        return -1

#automated tests
def test_tax_function():
    assert tax("a") == -1
    assert tax("ben") == -1
    assert round(tax(100), 2) == float(10.44)
    assert round(tax(1000), 1) == float(104.4)
    print("all test cases for tax function passed")

test_tax_function()
