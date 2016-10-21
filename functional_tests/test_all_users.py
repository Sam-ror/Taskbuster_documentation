# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
from datetime import date
from django.utils import formats

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_it_worked(self):
        activate('en')
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

    def get_full_url(self, namespace, lang):
        activate(lang)
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        lang = 'en'
        self.browser.get(self.get_full_url("home", lang))
        self.assertIn("TaskBuster", self.browser.title)

    def test_h1_css(self):
        lang = 'en'
        self.browser.get(self.get_full_url("home", lang))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgba(85, 85, 85, 1)")

    def test_home_files(self):
        activate('en')
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)

    def test_internationalization(self):
        for lang, h1_text in [('en', 'Welcome to TaskBuster!'),
                                    ('ca', 'Benvingut a TaskBuster!')]:
            print ("Let's talk about %s." % lang)
            self.browser.get(self.get_full_url("home", lang))
            h1 = self.browser.find_element_by_tag_name("h1")
            self.assertEqual(h1.text, h1_text)

    def test_localization(self):
        today = date.today()
        for lang in ['en', 'ca']:
            self.browser.get(self.get_full_url("home", lang))
            local_date = self.browser.find_element_by_id("local-date")
            non_local_date = self.browser.find_element_by_id("non-local-date")
            self.assertEqual(formats.date_format(today, use_l10n=True),
                                  local_date.text)
            self.assertEqual(today.strftime('%Y-%m-%d'), non_local_date.text)


    def test_time_zone(self):
        for lang in ['en', 'ca']:
            self.browser.get(self.get_full_url("home", lang))
            tz = self.browser.find_element_by_id("time-tz").text
            utc = self.browser.find_element_by_id("time-utc").text
            ny = self.browser.find_element_by_id("time-ny").text
            self.assertNotEqual(tz, utc)
            self.assertNotIn(ny, [tz, utc])
