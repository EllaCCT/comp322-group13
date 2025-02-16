from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from Backend.models.users.account.models import Member

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json

@api_view(['POST','GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getInfo(request):
  user = request.user
  member = Member.objects.get(user=user)
  print(member)
  if not member:
    return Response({
      'message': "Haven't login"
    })
  return Response({
    'message':'Logined',
    'username': user.username,
    'email': member.email,
    'address': member.address,
  })
  

@api_view(['POST','GET'])
def login(request):  
  user = get_object_or_404(User, username=request.data.get("username"))
  if not user.check_password(request.data['password']):
    return Response({
      'message' : "Wrong username or password."
    })
  token, _ = Token.objects.get_or_create(user=user)
  
  return Response({
    "message":"Login successful.",
    "jwt_token": str(token),
  })
  
def register(request):   
  if request.method == "POST":   
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    address = data.get("address")
    confirm_password = data.get("confirm_password")
      
    if not username or not password:
      return JsonResponse({
        "message":"Username and Password cannot be empty"
      })
      
    if password != confirm_password:
      return JsonResponse({
        "message":"Two passwords do not match"
      })
    
    if User.objects.filter(username=username).exists():
      return JsonResponse({
        "message":"This username already exist."
      })
    
    user = User(username=username)
    user.set_password(password)
    user.save()
    
    Member.objects.create(user=user)
    login(request, user)
    
    return JsonResponse({
      "message":"Registered successful."
    })
        
      
      
  
  