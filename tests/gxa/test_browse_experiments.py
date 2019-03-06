import os
import unittest

from tests.utils.selenium_utils import get_urls_from_html_elements
from tests.utils.http_utils import get_request_status_code

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class BrowseExperiments(unittest.TestCase):
    test_all: bool
    url_to_test: str

    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1280, 1024)

        base_url = os.getenv('ATLAS_URL', 'https://www-test.ebi.ac.uk/gxa')

        if os.getenv('TEST_ALL_EXPERIMENTS') == 'yes':
            self.test_all = True
        else:
            self.test_all = False

        self.url_to_test = base_url + '/experiments'

    def test_experiment_links_in_table(self):
        driver = self.driver
        driver.get(self.url_to_test)

        if self.test_all:
            driver.find_element_by_name('experiments-table_length').send_keys('All')
        else:
            driver.find_element_by_name('experiments-table_length').send_keys('25')

        experiment_links = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View in Expression Atlas']"))
        )

        if self.test_all:
            self.assertGreaterEqual(len(experiment_links), 3000)
        else:
            self.assertGreaterEqual(len(experiment_links), 25)

        for url in get_urls_from_html_elements(experiment_links):
            with self.subTest(url=url):
                print('checking url', url)

                self.assertEqual(get_request_status_code(url), 200)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
