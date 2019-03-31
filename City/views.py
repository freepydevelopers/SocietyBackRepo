from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from Core.models import City
from Core.serializers import CitySerializer
from django.http import JsonResponse
from json import JSONEncoder
from django.core import serializers

class ListCityView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

@api_view()
def details(request, id):
    city = get_object_or_404(City, id=id)
    array_result = serializers.serialize('json', [city], ensure_ascii=False)
    just_object_result = array_result[1:-1]
    return JsonResponse(just_object_result, safe=False)

class Hello(APIView):
    def get(self, request, format=None):
        return Response("Pune")



