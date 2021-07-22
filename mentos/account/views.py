# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from .models import *
from contest.models import *
from django.core.paginator import Paginator
import json
from .mbti import intro, question, option1, option2

# Create your views here.
def signup(request):
    if request.method == "POST":
        userID=request.POST.get('userID', None)
        name=request.POST.get('name', None)
        birthday=request.POST.get('birthday', None)
        mbti=request.POST.get('mbti', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        number=request.POST.get('number', None)
        email=request.POST.get('email', None)
        # 회원가입 검증
        if not (userID and password1 and password2 and name and birthday and number and email and mbti):
            return render(request, 'signup.html', {'error': '필수 정보를 입력해주세요!'})
        if User.objects.filter(username=userID).exists():
            return render(request, 'signup.html', {'error': '중복된 아이디입니다.'})
        if Profile.objects.filter(name=name).exists():
            return render(request, 'signup.html', {'error': '중복된 닉네임입니다.'})
        # 비밀번호 일치 여부 확인
        if password1 == password2:
            user = User()
            user.username = userID
            user.set_password(password1)
            profile = Profile()
            profile.name = name
            profile.birthday = birthday
            profile.number = number
            profile.email = email
            # mbti 검사 페이지로 이동
            if mbti == '모름':
                return render(request, 'mbti.html', {'user': user, 'profile': profile, 'intro': json.dumps(intro), 'question': json.dumps(question), 'option1': json.dumps(option1), 'option2': json.dumps(option2)})
            # home으로 이동
            else:
                profile.mbti = mbti
                user.save()
                profile.user = user
                profile.save() 
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'signup.html', {'error': '비밀번호가 일치하지 않습니다.'})
    return render(request,'signup.html')

def mbti(request):
    return render(request, 'mbti.html')

def result(request):
    if request.method == 'POST':
        result = request.POST.get('result', None)
        username = request.POST.get('userID', None)
        password = request.POST.get('password', None)
        name = request.POST.get('name', None)
        birthday = request.POST.get('birthday', None)
        number = request.POST.get('number', None)
        email = request.POST.get('email', None)

        user = User()
        user.username = username
        user.password = password
        user.save()
        profile = Profile()
        profile.name = name
        profile.birthday = birthday
        profile.number = number
        profile.email = email
        profile.mbti = result
        profile.user = user
        profile.save() 

        auth.login(request,user)
        
        return render(request, 'result.html', {'profile': profile})

def only_mbti(request):
    return render(request, 'only_mbti.html', {'intro': json.dumps(intro), 'question': json.dumps(question), 'option1': json.dumps(option1), 'option2': json.dumps(option2)})

def only_result(request):
    mbti = request.POST['result']
    return render(request, 'only_result.html', {'mbti': mbti})

def login(request):
    if request.method =="POST":
        userID=request.POST['userID']
        password=request.POST.get('password','')
        user = auth.authenticate(request,username=userID, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.'})
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
    user = request.user
    return render(request,'edituser.html')

def updateuser(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.name=request.POST['name']
    profile.birthday=request.POST['birthday']
    profile.mbti=request.POST['mbti']
    profile.number=request.POST['number']
    profile.email=request.POST['email']
    profile.save()
    return render(request, 'mypage.html')