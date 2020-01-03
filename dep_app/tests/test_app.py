'''Unittests module'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os


class TestApplication(unittest.TestCase):
	'''Unittests for application, using selenium'''

	@classmethod
	def setUpClass(cls):
		ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
		cls.driver = webdriver.Firefox(executable_path=os.path.join(ROOT_DIR, 'geckodriver'))
		cls.driver.maximize_window()
		cls.driver.get('http://127.0.0.1:5000/')

	def test_departments(self):
		'''Test of header link to departments list'''
		self.assertTrue(self.driver.find_element(By.XPATH, '/html/body/div/div/table'))

	def test_employees(self):
		'''Test for header link to employees list'''
		self.driver.find_element(By.XPATH, '/html/body/header/nav/div/a').click()
		self.assertTrue(self.driver.find_element(By.XPATH, '/html/body/div/div/table'))

	def test_department_and_employee(self):
		'''Test for other cases on the site'''

		# test addition of the department
		self.driver.find_element(By.CLASS_NAME, 'add_button').click()
		input = self.driver.find_element(By.ID, 'title')
		input.send_keys('Test')
		self.driver.find_element(By.ID, 'submit').click()

		# test previously added department
		self.driver.find_element_by_partial_link_text('Test').click()
		title = self.driver.find_element(By.CLASS_NAME, 'str-title')
		self.assertEqual(title.text, 'Test')

		self.driver.find_element(By.CLASS_NAME, 'add_button').click()

		# fill test employee form
		name = self.driver.find_element(By.ID, 'name')
		name.send_keys('Test employee')
		dob = self.driver.find_element(By.ID, 'dob')
		dob.send_keys('1900-01-01')
		salary = self.driver.find_element(By.ID, 'salary')
		salary.send_keys('110')
		self.driver.find_element(By.ID, 'submit').click()

		# test for editing employee
		self.driver.find_element_by_partial_link_text('Test employee').click()
		self.driver.find_element(By.CLASS_NAME, 'edit-button').click()
		name = self.driver.find_element(By.ID, 'name')
		name.clear()
		name.send_keys('Modified employee')
		self.driver.find_element(By.ID, 'submit').click()

		# navigate back to test department
		self.driver.find_element(By.XPATH, '/html/body/header/nav/div/form/a').click()
		self.driver.find_element_by_partial_link_text('Test').click()
		test_name = self.driver.find_element(By.XPATH, '/html/body/div/div/table/tbody/tr[2]/td[1]/a')
		self.assertEqual(test_name.text, 'Modified employee')

		# test deletion of the department
		self.driver.find_element(By.CLASS_NAME, 'delete-button').click()
		try:
			self.driver.find_element_by_partial_link_text('Test').click()
		except NoSuchElementException:
			self.assertTrue(True)
		else:
			self.assertTrue(False)

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()


if __name__ == '__main__':
	unittest.main()
