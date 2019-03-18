def get_url_from_html_element(html_element):
    return html_element.get_attribute('href')


def get_urls_from_html_elements(html_elements):
    return set(get_url_from_html_element(element) for element in html_elements)