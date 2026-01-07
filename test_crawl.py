import unittest
from crawl import (
    normalize_url, 
    get_h1_from_html, 
    get_first_paragraph_from_html, 
    get_urls_from_html, 
    get_images_from_html,
    extract_page_data
)

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_urls = [
            ('https://blog.boot.dev/path/', 'blog.boot.dev/path'),
            ('https://blog.boot.dev/path', 'blog.boot.dev/path'),
            ('http://BLOG.boot.dev/path/', 'blog.boot.dev/path'),
            ('http://BLOG.boot.dev/path', 'blog.boot.dev/path'),
        ]

        for item in input_urls:
            input_url = item[0]
            expected = item[1]
            actual = normalize_url(input_url)
            self.assertEqual(actual, expected)

    def test_h1_from_html_h1_exists(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = 'Test Title'
        self.assertEqual(actual, expected)

    def test_h1_from_html_no_h1(self):
        input_body = '<html><body><p>Test Text</p></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ''
        self.assertEqual(actual, expected)

    def test_h1_from_html_h1_with_whitespace(self):
        input_body = '<html><body><h1>   Test Text  </h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = 'Test Text'
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_with_main(self):
        input_body = '''
        <html>
            <body>
                <p>Outside paragraph.</p>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body>
        </html>
        '''
        actual = get_first_paragraph_from_html(input_body)
        expected = 'Main paragraph.'
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_without_main(self):
        input_body = '''
        <html>
            <body>
                <p>Outside paragraph.</p>
            </body>
        </html>
        '''
        actual = get_first_paragraph_from_html(input_body)
        expected = 'Outside paragraph.'
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_without_paragraph(self):
        input_body = '''
        <html>
            <body>
                <main>
                    <h1>Title</h1>
                </main>
            </body>
        </html>
        '''
        actual = get_first_paragraph_from_html(input_body)
        expected = ''
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_absolute(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev']
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev/path/one']
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_and_relative(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev/path/one', 'https://other.com/path/one']
        self.assertEqual(actual, expected)
        
    def test_get_urls_from_html_no_anchors(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev/logo.png']
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev/logo.png']
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute_and_relative(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://cdn.boot.dev/banner.jpg" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ['https://blog.boot.dev/logo.png','https://cdn.boot.dev/banner.jpg']
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = 'https://blog.boot.dev'
        input_body = '<html><body></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic2(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body><main>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </main></body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_section(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html><body>
            <nav><p>Navigation paragraph</p></nav>
            <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["h1"], "Main Title")
        self.assertEqual(actual["first_paragraph"], "Main paragraph content.")

    def test_extract_page_data_missing_elements(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
