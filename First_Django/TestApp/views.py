from cmath import log
from curses.ascii import US
from email import message
from multiprocessing import context
from os import name
from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Message, Room, Topic
from .forms import RoomForm



def room_simple(request):
    return HttpResponse('Inside Room')

def home_simple(request):
    return HttpResponse('Inside Home')


# rooms_dict=[
#     {'id' : 1, 'name' : 'Python Development'},
#     {'id' : 2, 'name' : 'Fintech'},
#     {'id' : 3, 'name' : 'Accouting and Finance'},
#     {'id' : 4, 'name' : 'Computer Arch'},
#     {'id' : 5, 'name' : 'Operating Systems'},
# ]


def room(request,pk):
    room=Room.objects.get(id=pk)

    # for i in rooms_dict:
    #     if i['id']==int(pk):
    #         room_element=i
    
    # Fetching all the messages corresponding the room.
    room_messages=room.message_set.all()

    # Fetching all the participants
    participants=room.participants.all()

    if request.method=='POST':
        # Create the message instance
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # Adding the pariticipant if he/she makes a comment.
        room.participants.add(request.user)
        # Then refresh the current page.
        return redirect('room',pk=room.id)


    context={'room' : room, 'room_messages':room_messages,'participants':participants}
    return render(request,'TestApp/RoomPage.html',context=context)

def home(request):

    # Getting the get url contents and filtering the rooms.
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    # print(q)
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # Getting all the room messages.
    # room_messages=Message.objects.all()
    # Getting room message filtered based on topic.
    room_messages=Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )


    
    topics=Topic.objects.all()
    total_rooms=Room.objects.all().count()

    context={'rooms':rooms,'topics':topics, 'room_messages':room_messages,'total_rooms':total_rooms}

    return render(request,'TestApp/HomePage.html',context=context)


def loginPage(request):

    # To differentiate between login and register pages.
    page='login'

    # If the user is already authenticated.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        # First checking whether the user exists or not.
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        
        # Then authenticate the user if exists.
        user=authenticate(request,username=username,password=password)

        # If the user is authenticated, login the user.
        if user!=None:
            login(request,user=user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Username or Password')

    context={'page':page}
    return render(request,'TestApp/LoginRegister.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    
    if request.method=='POST':
        form=RoomForm(request.POST)
        room_topic=request.POST.get('topic')
        topic, created_on=Topic.objects.get_or_create(name=room_topic)
        Room.objects.create(
            topic=topic,
            host=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context={'form' : form,'topics':topics}
    return render(request,'TestApp/RoomForm.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user!=room.host:
        return HttpResponse('You are not allowed to update other people\'s rooms')

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        room_topic=request.POST.get('topic')
        topic, created_on=Topic.objects.get_or_create(name=room_topic)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form' : form, 'room' : room,'topics':topics}
    return render(request,'TestApp/RoomForm.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to delete other rooms')

    if request.method=="POST":
        room.delete()
        return redirect('home')

    context={'obj':room}
    return render(request,'TestApp/Delete.html',context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse('You are not allowed to delete other messages')

    if request.method=="POST":
        message.delete()
        return redirect('room',pk=message.room.id)

    context={'obj':message}
    return render(request,'TestApp/Delete.html',context)

def registerPage(request):

    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #Not saving the user. Instead doing some data cleaning.
            user.username=user.username.lower()
            user.save()
            # After registration, the user must be logged in.
            login(request=request,user=user)
            return redirect('home')
        else:
            messages.error(request,'Error during Registration')
            

    context={'form': form}
    return render(request=request,template_name='TestApp/LoginRegister.html',context=context)

def userProfile(request, pk):

    user=User.objects.get(id=pk)
    topics=Topic.objects.all()
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    total_rooms=Room.objects.all().count()

    context={'user':user,'topics' : topics,'rooms':rooms,'room_messages':room_messages,'total_rooms':total_rooms}
    return render(request,'TestApp/UserProfile.html',context)