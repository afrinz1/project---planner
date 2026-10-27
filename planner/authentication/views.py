from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.contrib.auth import authenticate,login

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from . serializer import ProfileSerializer

from planner.utils import generate_password,send_email

import threading

# from django.contrib.auth.hashers import make_password

class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username,password = password)  #this will return the profile object , but if no user is present it will return null

        if user :

            refresh_token = RefreshToken.for_user(user)

            access_token = refresh_token.access_token

            data  = {'refresh_token':str(refresh_token),'access_token':str(access_token)}

            return Response(data,status=200)

        data = {'msg': 'invalid username'}

        return Response(data,status=400)

class UserRegisterView(APIView):

    def post(self,request,*args,**kwargs):

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data.get('username')   #this gives the data in dictionary format

            profile = serializer.save()

            profile.email = username

            profile.role = 'user'

            password = generate_password()

            # profile.password = password
            # profile.make_password(password)
            profile.set_password(password)   #it is basically used to hash the passowrd before it goes out

            profile.save()

            recipient = profile.email
            subject = 'cake site - login credentials'
            context = {'name':profile.first_name,'username':profile.username,'password':password}

            template = 'emails/credentials.html'

            thread = threading.Thread(target=send_email,args=(recipient,subject,context,template)) #now thread will do this send_email operation paralalaey
            thread.start()
            # send_email(recipient,subject,context,template)


            data = {'msg':'account created successfully'}

            return Response(data,status=200)

        return Response(serializer.errors,status=400)