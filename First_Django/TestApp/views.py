from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Room
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
    room_element=Room.objects.get(id=pk)

    # for i in rooms_dict:
    #     if i['id']==int(pk):
    #         room_element=i

    context={'room' : room_element}

    return render(request,'TestApp/RoomPage.html',context=context)

def home(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'TestApp/HomePage.html',context=context)

def createRoom(request):
    form=RoomForm()
    
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save() #Saving the record in the database
            return redirect('home')

    context={'form' : form}
    return render(request,'TestApp/RoomForm.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save() #Saving the record in the database
            return redirect('home')

    context={'form' : form}
    return render(request,'TestApp/RoomForm.html',context)


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    