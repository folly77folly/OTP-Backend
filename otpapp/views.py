from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import BookingSerializer, UserSerializer
from .models import User, Booking
from .helpers import id_generator
from decouple import config
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
import twilio
from  twilio.rest import Client
import json



class RegisterUser(APIView):
    """
    List all users, or create a new user.
    """
    def post(self, request, format = None):
        data = request.data
        phone = data['phone_no']
        user = User.objects.filter(phone_no = phone)
        if user:
            message = {"message":"Already Registered !!!"}
            return Response(message, status =  status.HTTP_400_BAD_REQUEST)        
        response = verify_number(phone)
        print(response.status)
        if response.status == "pending":
            message ={'message':"pending"}
            return Response(message, status =  status.HTTP_200_OK)
        message ={'message':"this resource is for customers"}
        return Response(message, status =  status.HTTP_400_BAD_REQUEST)
        # print(response.sid)
        

class VerifyToken(APIView):
    """
    List all users, or create a new user.
    """
    
    def post(self, request, format = None):
        data = request.data
        phone = data['phone_no']
        otp = data['otp']
        user = User.objects.filter(phone_no = phone)
        if user:
            message = {"message":"Already Registered !!!"}
            return Response(message, status =  status.HTTP_400_BAD_REQUEST)
        
        response = verify_token(phone, otp)
        if response.status == "approved":
            #create the user
            userdata = {'phone_no': phone,'password':'1234', 'otp':'1234'}
            serializer = UserSerializer(data=userdata)
            if serializer.is_valid():
                serializer.save()
                message = {"message":"Account created successfully"}
                return Response(message, status =  status.HTTP_201_CREATED)
        # print(response.sid)
        message = {"message":"error"}
        return Response(message, status =  status.HTTP_400_BAD_REQUEST)
        # return Response(response.status, status =  status.HTTP_400_BAD_REQUEST)

class VerifyUser(APIView):
    """
    List all users, or create a new user.
    """
    def post(self, request, format = None):
        data = request.data
        phone = data['phone_no']
        # otp = data['password']
        OTP=654321
        message=f"Please use this OTP to complete your login process:{OTP}"
        user = User.objects.filter(phone_no=phone)
        if user is None :
            response = {"message" : "Incorrect Phone Number"}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        # sms = send_twilio_message(phone, message)
        # print(sms)
        #update the userprofile with OTP
        update_otp(phone, OTP)
        response = {
            "message" : "Please Enter the OTP sent to your Phone",
            }

        return Response(response, status =  status.HTTP_200_OK)

class LoginUser(APIView):
    """
    List all users, or create a new user.
    """
    def post(self, request, format = None):
        data = request.data
        phone = data['phone_no']
        otp = data['otp']
        user = User.objects.filter(phone_no=phone, otp = otp)
        if user is None :
            response = {"message" : "Incorrect Phone Number"}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        user_token = get_token(request)
        response = {
            "message" : "You are logged in welcome back",
            "token" : user_token
            }
        # update_last_login(email)
        return Response(response, status =  status.HTTP_200_OK)


def get_token(request):
    print(request)
    user_obj = User.objects.get(phone_no = request.data['phone_no'])
    print(user_obj)
    # token = Token.objects.create(user = user_obj)
    # return token.key
    if request.method == 'POST':
        token = Token.objects.filter(user=user_obj)
        if token:
            new_key = token[0].generate_key()
            token.update(key=new_key)
            return new_key
        else:
            token = Token.objects.create(user = user_obj)
            return token.key

def send_twilio_message(to_number, body):
    client = Client(
        config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))

    return client.messages.create(
        body=body,
        to=to_number,
        from_=config('TWILIO_PHONE_NUMBER')
    )

def verify_number(to_number):
    client = Client(
        config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))

    verification=client.verify \
                     .services('VAd7aa008d6f009c117b4533b56f321041') \
                     .verifications \
                     .create(to=to_number, channel='sms')
    
    print(verification)
    return verification

def verify_token(to_number, code):
    client = Client(
        config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))

    verification_check = client.verify \
                            .services('VAd7aa008d6f009c117b4533b56f321041') \
                            .verification_checks \
                            .create(to=to_number, code=code)

    print(verification_check.status)
    return verification_check


def update_otp(phone, otp):
    user_obj = User.objects.get(phone_no = phone)
    update_data ={"otp":otp}
    serializer = UserSerializer(user_obj, data = update_data, partial = True)
    if serializer.is_valid():
        serializer.save()

class Booking(APIView):
    pass