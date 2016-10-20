# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_it_worked(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('TaskBuster Django Tutorial', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

class HomeNewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("TaskBuster", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgba(200, 50, 255, 1)")
