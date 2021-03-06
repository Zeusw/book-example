# -*- coding:utf-8 -*-
# The class don't success static file
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])



    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith hearda cool online application todo.
        # She looked at the project home page.
        self.browser.get(self.live_server_url)

        # She noted that the title of the page and head include "To-Do" word
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Applications invited her to enter a todo
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She entered the "Buy peacock feathers" in the text box
        # Edith is interested in is the use of fly-fishing for bait
        inputbox.send_keys('Buy peacock feathers')

        # She pressed the Enter key, the page updated.
        # Todo table show "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Page and displays a text box, you can enter additional todi.
        # She entered the "Use peacock feathers to make a fly"
        # Edith things very organized
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # Page updated again, her list shows the two todo.
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # New users now called Francis visited the site

        ## We use a new browser session
        ## Edith confirm the information does not leak out from the cookie
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis Home Access
        # Do not see the list of pages Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis entered a new to-do, create a new list
        # He did not like Edith immense interest
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis won his only URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # This page does not list Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Two people are satisfied to go to bed
        # self.fail('Finish the test!')


        # [...]


    def test_layout_and_styling(self):
        # Edith access home
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She saw perfectly centered input box
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She created a list perple to see the input box remains perfectly centered
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
