import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


log_path = 'logs/log_file.log'
service_log_path = 'logs/service_log.log'


@pytest.fixture(scope="function")
def setup_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def test_cell_size(setup_driver):
    driver = setup_driver
    driver.get('http://localhost:5001')  # Assuming your Flask app is running on this URL

    # Get the size of the first cell before any move
    cell_before = driver.find_element(By.CSS_SELECTOR, "td:nth-child(1)").size

    # Make a move (you can simulate this by clicking on the cell or using the API directly)
    driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) button").click()

    # Get the size of the first cell after the move
    cell_after = driver.find_element(By.CSS_SELECTOR, "td:nth-child(1)").size

    # Assert that the size remains the same
    assert cell_before == cell_after
