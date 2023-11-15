from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .permissions import IsAdminUser  

from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to my app!")  


def user_list_view(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user credentials
            password = form.cleaned_data.get('password1')

            user = authenticate(email=user.email, password=password)
            if user is not None:
                login(request, user)
                # Create a token for the new user
                token, created = Token.objects.get_or_create(user=user)
                # Directly log the user in and redirect to the homepage or
                request.session['auth_token'] = token.key
                return Response({'token': token.key})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return render(request, 'client_list.html', {'token': token.key})
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    else:
        return render(request, 'login.html')


