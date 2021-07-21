# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from .models import *
from contest.models import *
from django.core.paginator import Paginator


# Create your views here.
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user=User.objects.get(username=request.POST['userID'])
                return HttpResponse('이미 사용하고 있는 아이디입니다!')
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST["userID"],password=request.POST["password1"]
                )
                user.profile.name=request.POST['name']
                user.profile.birthday=request.POST['birthday']
                user.profile.mbti=request.POST['mbti']
                user.profile.number=request.POST['number']
                user.profile.email=request.POST['email']
                if user.profile.name and user.profile.birthday and user.profile.number and user.profile.email:
                    user.save()
                else:
                    return HttpResponse('모든필드를채워주세요!')
                auth.login(request,user)
                return redirect('home')
    return render(request,'signup.html')

def login(request):
    if request.method =="POST":
        userID=request.POST['userID']
        password=request.POST.get('password','')
        user = auth.authenticate(request,username=userID, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return HttpResponse('userID or password is incorrect')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def mypage(request):
    user = request.user

    like_post_list=[]
    participant_post_list=[]
    host_post_list=[]

    if user.is_active:
        likes=Like.objects.select_related()
        for like in likes:
            if like.user == user:
                like_post_list.append(like.post)
        like_post_list = sorted(like_post_list, key=lambda like_post_list: like_post_list.created_at, reverse=True)
        like_paginatior = Paginator(like_post_list,4)
        like_page = request.GET.get('like_page')
        like_posts = like_paginatior.get_page(like_page)


        ideas = Idea.objects.filter(i_writer=user)
        for idea in ideas:
            if idea.post not in participant_post_list:
                participant_post_list.append(idea.post)

        participant_post_list = sorted(participant_post_list, key=lambda participant_post_list: participant_post_list.created_at, reverse=True)
        participant_paginatior = Paginator(participant_post_list,4)
        participant_page = request.GET.get('participant_page')
        participant_posts = participant_paginatior.get_page(participant_page)

        posts = Post.objects.filter(manager=user).order_by('-created_at')
        host_post_list= posts
        host_paginatior = Paginator(host_post_list,4)
        host_page = request.GET.get('host_page')
        host_posts = host_paginatior.get_page(host_page)

        return render(request, 'mypage.html', {'like_posts':like_posts,
                                                'participant_posts':participant_posts,
                                                'host_posts':host_posts})

    
    return render(request,'mypage.html')

def edituser(request):
    return render(request,'edituser.html')

def updateuser(request):
    user = request.user
    user.profile.name=request.POST['name']
    user.profile.birthday=request.POST['birthday']
    user.profile.mbti=request.POST['mbti']
    user.profile.number=request.POST['number']
    user.profile.email=request.POST['email']
    user.save()
    return render(request, 'mypage.html')