from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
from business.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import status
from functools import wraps
from rest_framework.permissions import IsAuthenticated


class CustomerView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        customers = Customer.published.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def resource_checker(model):
    def check_entity(func):
        @wraps(func)
        def inner_fun(*args, **kwargs):
            try:
                x = func(*args, **kwargs)
                return x
            except model.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return inner_fun
    return check_entity


class CustomerDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @resource_checker(Customer)
    def get(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @resource_checker(Customer)
    def put(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @resource_checker(Customer)
    def delete(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
