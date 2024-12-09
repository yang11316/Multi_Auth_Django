from django.test import TestCase
from django.test.client import Client
 
# csrf_client = Client(enforce_csrf_checks=True)
csrf_client = Client()
c = Client(HTTP_USER_AGENT='Mozilla/5.0')

# class simpleCase(TestCase):
#     def setUp(self):
    
#     def test_get_aux_data(self):

#     def tearDown(self):
