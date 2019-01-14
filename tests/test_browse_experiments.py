import os
import unittest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class BrowseExperiments(unittest.TestCase):

    url_to_test: str

    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1280, 1024)

        base_url = os.getenv('ATLAS_URL', 'https://www-test.ebi.ac.uk/gxa')

        self.url_to_test = base_url + '/experiments'

    def test_experiments_return_200(self):
        driver = self.driver
        driver.get(self.url_to_test)

        # driver.find_element_by_name('experiments-table_length').send_keys('25')
        driver.find_element_by_name('experiments-table_length').send_keys('All')

        experiment_links = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View in Expression Atlas']"))
        )

        self.assertGreaterEqual(len(experiment_links), 3000)

        for url in self.get_urls_from_html_elements(experiment_links):
            with self.subTest(url=url):
                print('checking url', url)
                self.check_status_code_is_200(url)

    def get_url_from_html_element(self, html_element):
        return html_element.get_attribute('href')

    def get_urls_from_html_elements(self, html_elements):
        return [self.get_url_from_html_element(element) for element in html_elements]

    def check_status_code_is_200(self, url):
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

