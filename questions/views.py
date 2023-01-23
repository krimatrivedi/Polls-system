from cmath import log
from django.shortcuts import redirect, render
import datetime
from django.utils import timezone
from questions.models import Answers, Phonenumbers, Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from .tasks import *
from django.http import HttpResponse
#import requests
from django.contrib.auth import logout as auth_logout

from django.contrib import messages

#login of user
def login_view(request):
   # return HttpResponse("<h1> Django Deployed</h1>")
   # messages.info(request, 'Account not found')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj= User.objects.filter(username = email)
        if not user_obj.exists  ():
            messages.info(request, 'Account not found')
            return redirect('/register/')

        user_obj = authenticate(username =email ,password = password)
        
        if user_obj:
            login(request , user_obj)
            return redirect('/dashboard/')

        messages.info(request, 'Invalid password')
        return redirect('/')
        
    return render(request , 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('/')

#user register

def register_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        phone_no=request.POST.get('phone_no')

        user_obj= User.objects.filter(username = email)

        if user_obj.exists():
            messages.info(request, 'Username is already taken')
            return redirect('/register/')

        user_obj = User.objects.create(username = email,first_name=first_name)
        #phone number of user with user's foreign key
        pro_obj=Phonenumbers.objects.create(phone_no=phone_no , user = user_obj)
        user_obj.set_password(password)
        user_obj.save()
        messages.info(request, 'Account created')
        return redirect('/')

    return render(request , 'register.html')



#dashboard where all polls of every user's
def dashboard(request):
   
    if request.method == 'GET':
    
        questions = Question.objects.all()
        
        return render(request ,'dashboard.html' ,{'questions' : questions})


def create_poll(request):
    #user can ask only five question
    if request.method == 'GET':
        que_five=Question.objects.filter(user=request.user)
      
        if len(que_five)>4:
                messages.info(request, 'Only five questions can be created')
                return render(request , 'dashboard.html',{'questions' : que_five})
    #user create poll here
    if request.method == 'POST':
        question = request.POST.get('question')
        answers = request.POST.getlist('answers')

        question_obj = Question.objects.create(
            user = request.user,
            question_text = question
        )
        

        for answer in answers:
            Answers.objects.create(answer_text = answer , question = question_obj)


        messages.info(request, 'Your Poll Has been created')

        return redirect('/create_poll/')

    return render(request , 'create_poll.html')


#user can see only own polls
def see_answers(request):
    #below is celery's call for delete each poll after 24 hr
    delete_file()

    user= User.objects.filter(username = request.user)

    questions = Question.objects.filter(user = request.user)
    context = {'questions' : questions,
    'user' : user,

    }

    return render(request ,'see_ansswers.html' ,context)



#api for saving result
@api_view(['POST'])
@csrf_exempt
def save_question_result(request):
    data = request.data
    question_uid = data.get('question_uid')
    answer_uid = data.get('answer_uid')

    if question_uid is None and answer_uid is None:
        payload = {'data' : 'both question uid and answer uid are required' , 'status' : False}

        return Response(payload)

    question_obj = Question.objects.get(uid = question_uid)
    answer_obj  = Answers.objects.get(uid = answer_uid)
    answer_obj.counter += 1
    answer_obj.save()

    payload = {'data' : question_obj.calculate_percentage() , 'status' : True}

    return Response(payload)





def question_detail(request , question_uid):
    try:
        question_obj = Question.objects.get(uid = question_uid)
        context = {'question' : question_obj}
        return render(request , 'question.html' , context)

    except Exception as e :
        print(e)
        # return redirect('/')