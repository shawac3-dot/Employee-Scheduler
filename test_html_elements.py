from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestEmployees(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_employees(self):
        driver = self.driver
        driver.get("http://10.48.229.139")  # Replace with your app's URL

        # Check for the presence of all 10 test employees
        for i in range(10):
            employee_id = f'EMP{i:03d}'
            name = f'Test Employee {i}'
            
            # Verify Employee ID is in page
            assert employee_id in driver.page_source, f"Test employee ID {employee_id} not found in page source"
            # Verify Name is in page
            assert name in driver.page_source, f"Test employee name {name} not found in page source"

        print("Test completed successfully. All 10 test employees were verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
