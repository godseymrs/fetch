
from selenium.webdriver.common.by import By

class Locators:
    LEFT_CELL_0 = (By.ID, "left_0")
    BTN_WEIGH = (By.ID, "weigh")
    BTN_RESET = (By.XPATH, "//button[contains(text(),'Reset')]")
    RESULTS_LIST = (By.XPATH, "//div[@class='game-info']//li")
