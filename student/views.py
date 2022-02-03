from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, ListView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from student.forms import InsertStudent, InsertStudent1
from student.models import info, track
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from student.serializers import Studentser


def register(req):
    if (req.method == 'GET'):
        return render(req, 'register.html')
    else:
        print(req.POST)
        # cretae myuser
        usernmae = req.POST['username']
        email = req.POST['Email']
        password = req.POST['password']
        # add myuser
        info.objects.create(fullname=usernmae, password=password, Email=email)
        # add user
        User.objects.create_user(username=usernmae, email=email, password=password, is_staff=True)
        # redirect to login view
        # return HttpResponseRedirect('/login')
        # return render(req, 'login.html',context) , {'users': user}
        return redirect('/login')


def login_1(request):
    if (request.method == 'GET'):
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        # check cred in User
        authuser = authenticate(username=username, password=password)
        # check cred in myuser
        user = info.objects.filter(fullname=username, password=password)

        if (authuser is not None and user is not None):
            request.session['username'] = username
            request.session['authuser'] = authuser.username
            login(request, authuser)
            return redirect('/home', user)
        else:
            context = {}
            context['errormsg'] = 'Invalid Email or Password.'
            return render(request, 'login.html', context)


def mylogout(request):
    request.session['username'] = None
    logout(request)
    request.session['authuser'] = None
    return redirect('/login')


def home(request):
    if (request.session.get('username') is not None):
        return render(request, 'home.html')
    else:
        return redirect('/login')


# *************************************************************************
def isertstudentform(request):
    if (request.session['username'] is not None):
        context = {}

        if (request.method == 'GET'):
            form = InsertStudent()
            return render(request, 'insert.html', {'form': form})
        else:

            info.objects.create(fullname=request.POST['fullname'], password=request.POST['password'],
                                Email=request.POST['Email'])

            return redirect('/insert')
    else:
        return redirect('/login')


def isertstudentform1(request):
    if (request.session['username'] is not None):
        context = {}

        if (request.method == 'GET'):
            form = InsertStudent1()
            return render(request, 'insert.html', {'form': form})
        else:
            form = InsertStudent1(request.POST)
            form.save()
            # info.objects.create(fullname=request.POST['fullname'], password=request.POST['password'], Email=request.POST['Email'])
            return redirect('/insert')
    else:
        return redirect('/login')


def insert(req):
    if (req.session['username'] is not None):
        context = {}
        if (req.method == 'GET'):
            return render(req, 'insert.html')
        else:
            print(req.POST)

            info.objects.create(fullname=req.POST['username'], password=req.POST['password'], Email=req.POST['Email'])

            return render(req, 'insert.html')
    else:
        return redirect('/login')


class trackList(ListView):
    model = track


# *************************************************************************
def update(req):
    if (req.session['username'] is not None):
        user = info.objects.all()
        return render(req, 'update.html', {'users': user})
    else:
        return redirect('/login')


def update1(req, id, name, email, passs):
    if (req.session['username'] is not None):
        if (req.method == 'GET'):
            context = {'id': id, 'name': name, 'email': email, 'password': passs}
            return render(req, 'update1.html', context)
        else:

            objects = info.objects.filter(id=id)
            for obj in objects:
                obj.fullname = req.POST['username']
                obj.Email = req.POST['Email']
                obj.password = req.POST['password']
                obj.save()
            return redirect('/update')
    else:
        return redirect('/login')


def delete(req, id):
    if (req.session['username'] is not None):
        objects = info.objects.filter(id=id)
        objects.delete()
        return redirect('/update')
    else:
        return redirect('/login')


def deleteall(req):
    if req.session['username'] is not None:
        objects = info.objects.all()
        objects.delete()
        return redirect('/update')
    else:
        return redirect('/login')


def search(request):
    if request.session['username'] is not None:
        context = {}
        if (request.method == 'GET'):
            return render(request, 'search.html')
        else:
            # check for user and passs
            name = request.POST['username']
            # if correct
            users = info.objects.filter(fullname__in=[name])
            if (users):
                return render(request, 'search.html', {'users': users})
            else:
                context['errormsg'] = 'No Student with this name.'
                return render(request, 'search.html', context)
    else:
        return redirect('/login')


# ***************************************
class Studentview(viewsets.ModelViewSet):
    queryset = info.objects.all()
    serializer_class = Studentser


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def student_detail(request, id):
    student = info.objects.get(id=id)

    if request.method == 'PATCH':
        serializer = Studentser(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
