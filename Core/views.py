from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import State, City
from .serializers import CitySerializer
from django.http import JsonResponse
from .forms import UserForm, ProfileForm
from django.contrib import messages


def Index(request):
    s = State.objects.all()
    statecontext = {'states': s,'year': 2019}
    return render(request, 'Core/index.html', context=statecontext)

class ListCityView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


@api_view()
def details(request, id):
    city = get_object_or_404(City, id=id)
    return JsonResponse({"FirstName": "Praveer", "LastName": "Dhage"})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return render(request, 'core/profile/profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/profile/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })