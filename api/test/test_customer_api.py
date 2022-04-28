from msilib.schema import Class
from urllib import response
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from api.views import CustomerView, CustomerDetailView
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User


class ApiUrlsTests(SimpleTestCase):

    def test_get_customer_is_resolved(self):
        url = reverse('customer')
        self.assertEqual(resolve(url).func.view_class, CustomerView)


class CustomerApiViewTests(APITestCase):

    customer_urls = reverse('customer')

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass
    

    def test_get_customers_authenticated(self):
        response = self.client.get(self.customer_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_urls)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_customer_authenticated(self):
        data = {
            "title" : "Test",
            "name" : "Test",
            "last_name" : "Test",
            "gender":"M",
            "status" :"published"
        }
        response = self.client.post(self.customer_urls, data, formart="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CustomerDetailViewTests(APITestCase):
    customer_urls = reverse('customer')
    customer_url = reverse('customer-detail', args=[1])


    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a customer
        data = {
            "title" : "Test",
            "name" : "Test",
            "last_name" : "Test",
            "gender":"M",
            "status" :"published"
        }
        response = self.client.post(self.customer_url, data, format='json')

    def tearDown(self):
        pass 

    def test_get_customer_autheticated(self):
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)








       
        
 