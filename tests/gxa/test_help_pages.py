import os
import unittest

from tests.utils.selenium_utils import get_urls_from_html_elements
from tests.utils.http_utils import get_request_status_code

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HelpPages(unittest.TestCase):
    base_url: str
    help_page_uri: str
    faq_page_uri: str

    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1280, 1024)

        self.base_url = os.getenv('ATLAS_URL', 'https://www-test.ebi.ac.uk/gxa')

        self.help_page_uri = '/help/index.html'
        self.faq_page_uri = '/FAQ.html'

    def test_side_nav_links(self):
        driver = self.driver
        url_to_test = self.base_url + self.help_page_uri

        driver.get(url_to_test)

        links = (driver
                 .find_element_by_id('main-content-area')
                 .find_element_by_tag_name('ul')
                 .find_elements_by_tag_name('a'))

        for url in get_urls_from_html_elements(links):
            with self.subTest(url=url):
                print('checking url', url)
                self.assertEqual(get_request_status_code(url), 200)

    def test_main_body_links(self):
        driver = self.driver
        url_to_test = self.base_url + self.help_page_uri

        driver.get(url_to_test)

        links = (driver
                 .find_element_by_id('main-content-area')
                 .find_element_by_class_name('columns')
                 .find_elements_by_tag_name('a'))

        # Testing both internal and external (e.g. GitHub, Bioconductor) links
        for url in get_urls_from_html_elements(links):
            with self.subTest(url=url):
                print('checking url', url)
                self.assertEqual(get_request_status_code(url), 200)

    def test_faq_links(self):
        driver = self.driver
        url_to_test = self.base_url + self.faq_page_uri

        driver.get(url_to_test)

        links = (driver
                 .find_element_by_id('main-content-area')
                 .find_element_by_class_name('columns')
                 .find_elements_by_tag_name('a'))

        for url in get_urls_from_html_elements(links):
            # JSTOR detects the requests are not coming from a human...
            if "jstor.org" not in url:
                with self.subTest(url=url):
                    print('checking url', url)
                    self.assertEqual(get_request_status_code(url), 200)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
