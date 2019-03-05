import os
import unittest

from tests.utils.selenium_utils import get_urls_from_html_elements
from tests.utils.http_utils import get_request_status_code

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowseExperiments(unittest.TestCase):
    url_to_test: str

    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1280, 1024)

        base_url = os.getenv('ATLAS_URL', 'https://www-test.ebi.ac.uk/gxa')

        self.url_to_test = base_url + '/help/index.html'

    def test_side_nav_links_return_200(self):
        driver = self.driver
        driver.get(self.url_to_test)

        links = (driver
                 .find_element_by_id('main-content-area')
                 .find_element_by_tag_name('ul')
                 .find_elements_by_tag_name('a'))

        for url in get_urls_from_html_elements(links):
            with self.subTest(url=url):
                print('checking url', url)
                self.assertEqual(get_request_status_code(url), 200)

    def test_main_body_links_return_200(self):
        driver = self.driver
        driver.get(self.url_to_test)

        links = (driver
                 .find_element_by_id('main-content-area')
                 .find_element_by_class_name('columns')
                 .find_elements_by_tag_name('a'))

        # Testing both internal and external (e.g. GitHub, Bioconductor) links
        for url in get_urls_from_html_elements(links):
            with self.subTest(url=url):
                print('checking url', url)
                self.assertEqual(get_request_status_code(url), 200)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
