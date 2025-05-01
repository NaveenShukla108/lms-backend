from django.shortcuts import render
from .serializer import RegisterSerializer
from rest_framework import viewsets


class RegisterViewset(viewsets.ModelViewSet):

    http_method_names = ['post', 'delete']
    serializer_class = RegisterSerializer
    lookup_field = "username"