import pytest, time
from locators import Locators
from test_data import Test_Data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def reset(browser):
    """Click the reset button and wait for the first cell on left to empty."""
    browser.find_element(*Locators.BTN_RESET).click()
    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.text_to_be_present_in_element(Locators.LEFT_CELL_0, "")
    )

def compare(group1, group2):
    """Compares the total weight of two groups.
        -1 = Group1 is lighter
        1 = Group1 is heavier
        0 = groups are equal"""

    weight_group1 = sum(group1)
    weight_group2 = sum(group2)

    if weight_group1 < weight_group2:
        return -1
    elif weight_group1 > weight_group2:
        return 1
    else:
        return 0

def weigh(browser, minimum_result_count=1):
    """Click weigh, wait for the results to load, get the results, and determine & return the operator"""

    # Click weigh
    browser.find_element(*Locators.BTN_WEIGH).click()

    # Wait for results
    WebDriverWait(browser, Test_Data.DELAY).until(EC.presence_of_element_located((Locators.RESULTS_LIST)))
    WebDriverWait(browser, 20).until(lambda browser: len(browser.find_elements(By.XPATH, "//div[@class='game-info']//li")) >= int(minimum_result_count))
    print("Weighing...")

    # Grab last result
    most_recent = get_latest_result(browser)
    print("Last result: " + str(most_recent))

    # Extract the operator & return
    status = determine_operator(most_recent)
    print("Determined result: " + str(status))
    return status

def determine_operator(string_value):
    """Extract =, <, or > from the given string."""
    if "=" in string_value:
        print("Found =, returning 0")
        return 0
    elif "<" in string_value:
        print("Found <, returning -1")
        return -1
    else: # >
        print("Found >, returning 1")
        return 1

def input_cell_value(browser, pos=0, num=0, left=True):
    """Input a given num into a cell based on its pos(ition) & panel
    Numbers are left to right, top to bottom, 0-8
    """

    # Create the object ID based on which panel & position
    if left:
        cell_id = "left_" + str(pos)
    else:
        cell_id = "right_" + str(pos)

    # Click and enter value.
    cell = browser.find_element(By.ID, cell_id)
    cell.click()
    cell.send_keys(str(num))
    print("Entered " + str(num) + " in " + str(cell_id))

def get_latest_result(browser):
    """Get all the results and return the latest one."""
    results_list = browser.find_elements(*Locators.RESULTS_LIST)
    results_count = len(results_list)

    # There should be at least 1.
    assert results_count > 0

    print("Get Latest Result: " + str(results_list[results_count-1].text))
    return results_list[results_count-1].text

def get_lighter_position(result, group):
    """ Based on the group comparison result, return the unique value.
    """
    print("Get Lighter Group: " + str(group))
    print("Get Lighter Result: " + str(result))

    # Determine which is the unique weight.
    if result == 0: # Equal, so last object in group
        final = group[2]  # The different object is the third one
    elif result == -1:  # <, so first item in group
        final = group[0]
    else: # >, so second item in group.
        final = group[1]
    return final