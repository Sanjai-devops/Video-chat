from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from videoChat.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout

# Create your views here  

def getToken(request):
    appId="cfd02a5b4bf04bb0b738a58ecee6748d"
    appCertificate="dcd9b94c092c486583a24ec9eeff8a90"
    channelName= request.GET.get('channel')
    uid= random.randint(1,230)
    expirationTimeInSeconds= 3600*24
    currentTimeStamp= time.time()
    privilegeExpiredTs= currentTimeStamp + expirationTimeInSeconds
    role= 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration Success You can Login Now..!")
            return redirect('/signin')
    return render(request,'register.html',{'form':form})  

def signin(request):
      if request.user.is_authenticated:
        return redirect("/")
      else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("/signin")
        return render(request, 'login.html')

def signout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')

def createuser(request):
    data = json.loads(request.body)
    member,created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']},safe=False)
    