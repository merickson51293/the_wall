from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, 'index.html')

def wall(request):
    context = {
        'wall_messages': Message.objects.all()
    }
    return render(request, 'wall.html', context)

def register(request):
    if request.method=="POST":
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw=request.POST['password']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect("/wall")
    return redirect('/')

def login(request):
    if request.method=="POST":
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/wall')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def message(request):
    Message.objects.create(message=request.POST['message'], person=User.objects.get(id=request.session['user_id']))
    return redirect('/wall')

def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect ('/wall')

def comment(request, message_id):
    person = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=message_id)
    Comment.objects.create(comment=request.POST['comment'], person=person, wall_message=message)
    return redirect('/wall')

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/wall')
    

