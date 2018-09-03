from app import create_app
import unittest

class TestMainRoutes(unittest.TestCase):

	def test_home(self):
		tester = current_app.test_client(self)
		response = tester.get("/home", content_type = "html/text")
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()