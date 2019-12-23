'''Unittests module'''
import unittest
import requests
from dep_app.rest.api import app

url = 'http://0.0.0.0:8000'


def generate_department():
	'''Function, which makes post request to departments resource for further testing'''

	data = {'title': 'unittest'}
	r = requests.post(url + '/department', data=data)
	response = r.json()
	return response, r.status_code, data


class TestRestDepartments(unittest.TestCase):
	'''
	Unittests for CRUD operations with department table in rest api
	'''

	def setUp(self):
		self.app = app.test_client()

	def test_post(self):
		'''Post method test for departments'''
		data = {'title': 'unittest'}
		r = self.app.post('/department', data=data)
		res = r.json
		self.assertEqual(res['title'], data['title'])
		self.app.delete('/department/by_id/{}'.format(res['id']))

	def test_get(self):
		'''Get method test for departments'''
		r = self.app.get('/department')
		self.assertEqual(200, r.status_code)
		r = self.app.get('/department/by_title/{}'.format('unittest'))
		self.assertEqual(200, r.status_code)
		r = self.app.get('/department/by_id/{}'.format(1))
		self.assertEqual(200, r.status_code)

	def test_put(self):
		'''Put method test for departments'''
		data = {'title': 'unittest'}
		r = self.app.post('/department', data=data)
		res = r.json
		post = {'title': 'AAA', 'id': res['id']}
		r = self.app.put('/department', data={'title': 'AAA', 'id': res['id']})
		response = r.json
		self.assertEqual(response['title'], post['title'])
		self.assertEqual(r.status_code, 200)
		self.app.delete('/department/by_id/{}'.format(res['id']))

	def test_delete(self):
		'''Delete method test for departments'''
		data = {'title': 'unittest'}
		r = self.app.post('/department', data=data)
		res = r.json
		r = self.app.delete('/department/by_id/{}'.format(res['id']))
		self.assertEqual(r.status_code, 200)


#
#
# class TestRestEmployees(unittest.TestCase):
# 	'''
# 	Unittests for CRUD operations with Employees table in rest api
# 	'''
#
# 	def test_post(self):
# 		'''Post method test for employees'''
# 		res, _, _ = generate_department()
# 		data = {'name': 'unittest', 'dob': '1000-10-10', 'salary': 1, 'dep_id': res['id']}
# 		r = requests.post(url + '/employee', data=data)
# 		self.assertEqual(r.status_code, 201)
# 		requests.delete(url + '/department/by_id/{}'.format(res['id']))
#
# 	def test_get(self):
# 		'''Get method test for employees'''
# 		r = requests.get(url + '/employee')
# 		self.assertEqual(200, r.status_code)
# 		r = requests.get(url + '/employee/{}'.format(1))
# 		self.assertEqual(200, r.status_code)
#
# 	def test_put(self):
# 		'''Put method test for employees'''
# 		res, _, _ = generate_department()
# 		post = {'name': 'unittest', 'dob': '1000-10-10', 'salary': 1, 'dep_id': res['id']}
# 		response = requests.post(url + '/employee', data=post).json()
# 		put = {'name': 'unittest', 'dob': '2000-10-20', 'salary': 1.33, 'dep_id': res['id'], 'id': response['id']}
# 		r = requests.put(url + '/employee', data=put).json()
# 		self.assertEqual(r['dob'], put['dob'])
# 		requests.delete(url + '/department/by_id/{}'.format(res['id']))
#
# 	def test_delete(self):
# 		'''Delete method test for employees'''
# 		res, _, _ = generate_department()
# 		post = {'name': 'unittest', 'dob': '1000-10-10', 'salary': 1, 'dep_id': res['id']}
# 		response = requests.post(url + '/employee', data=post).json()
# 		r = requests.delete(url + '/employee/{}'.format(response['id']))
# 		self.assertEqual(r.status_code, 200)
# 		requests.delete(url + '/department/by_id/{}'.format(res['id']))


if __name__ == '__main__':
	unittest.main()
