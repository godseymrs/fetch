import pytest, time
from locators import Locators
from test_data import Test_Data
from selenium import webdriver
from test_functions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_website(browser):
    # I've kept print statements in as proof of the process for validation purposes & screenshot. I would remove these before committing for real work.

    # Browser check for sanity
    browser.get(Test_Data.URL)
    assert browser.title == Test_Data.BROWSER_TITLE

    # Divide the objects into three groups
    group1 = [0,1,2]
    group2 = [3,4,5]
    group3 = [6,7,8]

    # Input group 1 & 2 in left & right panes
    input_cell_value(browser, pos=0, num=group1[0], left=True)
    input_cell_value(browser, pos=1, num=group1[1], left=True)
    input_cell_value(browser, pos=2, num=group1[2], left=True)
    input_cell_value(browser, pos=0, num=group2[0], left=False)
    input_cell_value(browser, pos=1, num=group2[1], left=False)
    input_cell_value(browser, pos=2, num=group2[2], left=False)
    print("Initial values inputted.")

    # Weight the values, fetch results, and reset.
    result = weigh(browser, 1)
    print("1st weigh result is: " + str(result))
    reset(browser)

    if result == 0:
        print("Results are equal.")
        # The lighter object is in group3. Weigh 2 of the objects in group3.

        input_cell_value(browser, pos=0, num=group3[0], left=True)
        input_cell_value(browser, pos=0, num=group3[1], left=False)
        print("2nd values inputted (equal).")

        # Weight the values, fetch results, and reset.
        result = weigh(browser, 2)
        print("2nd results are (equal): " + str(result))
        reset(browser)

        # Determine which is the unique weight.
        final = get_lighter_position(result, group3)
        print("Final value (equal): " + str(final))

    else:
        print("Results are not equal.")
        # The different object is in group1 or group2

        # Convenience, save to variable for readability.
        if result == 1: # group 1 > group 2
            heavier_group = group1
            lighter_group = group2
        else: # group 1 < group2
            heavier_group = group2
            lighter_group = group1

        print("Heavier Set: " + str(heavier_group))
        print("Lighter Set: " + str(lighter_group))

        # Weigh two objects from the lighter group (looking for the lightest object)
        input_cell_value(browser, pos=0, num=lighter_group[0], left=True)
        input_cell_value(browser, pos=0, num=lighter_group[1], left=False)
        print("2nd values inputted (unequal).")

        # Weigh and reset.
        result = weigh(browser, 2)
        print("2nd result is (unequal): " + str(result))
        print("Lighter group is: " + str(lighter_group))
        reset(browser)

        # Determine which is the unique weight.
        final = get_lighter_position(result, lighter_group)
        print("Final (unequal): " + str(final))

    print("Clicking: " + str(final))
    browser.find_element(By.ID, "coin_" + str(final)).click()

    # Validate and handle the alert.
    print("Alert Check")
    alert = Alert(browser)

    alert_text = Alert(browser).text
    print("Alert: " + str(alert_text))
    assert alert_text == "Yay! You find it!"

    alert.accept()