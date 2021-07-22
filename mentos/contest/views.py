from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *

import random
from django.http import HttpResponse
import json

#C
def create(request):
    post=Post()
    post.title=request.POST['title']
    post.content=request.POST['content']

    post.manager=request.user
    post.save()

    checked_categories=request.POST.getlist('category[]')
    for checked_category in checked_categories:
        category = Category()
        category.category_name = checked_category
        category.post = post
        category.save()
        
    post.save()

    return redirect('/contestPost/'+str(post.id))

#R
#홈페이지
def home(request):
    posts = Post.objects
    post_list=list(Post.objects.all())

    random_post = None
    random_items = None
    items_range = None
    random.shuffle(post_list)
    if posts.exists():
        if len(post_list) == 1:
            random_post= post_list[0]
        elif len(post_list) < 5:
            random_post= post_list[0]
            random_items= post_list[1:]
        else:
            random_post = post_list[0]
            random_items = post_list[1:5]
    
    if random_items is not None:
        items_range = range(1, len(random_items)+1)
    return render(request,'home.html',{'posts':posts, 'random_post':random_post, 'random_items':random_items, 'items_range':items_range})  

#멘티글
def contestPost(request, post_id):
    user=request.user
    post = get_object_or_404(Post,pk=post_id)
    categories = Category.objects.all().filter(post = post)

    if post.likes.filter(id=user.id):
        message="좋아요취소"
    else:
        message="좋아요"
    #좋아요버튼
    num = post.likes.count()
    
    comments = Comment.objects.all().filter(post = post)
    comment_num = comments.count()

    participate_idea = Idea.objects.filter(post = post, i_writer = user).first()
    if participate_idea is not None:
        return render(request,'contestPost.html' ,{'post':post, 'message':message, 'comments':comments, 'categories':categories, 'participate_idea': participate_idea, 'num':num})

    return render(request,'contestPost.html' ,{'post':post, 'message':message, 'comments':comments, 'categories':categories, 'num':num})

#멘티 확인 페이지
def hostPage(request):
    user = request.user
    if user.is_active:
        posts = Post.objects.filter(manager=user) 
        return render(request, 'hostPage.html', {'posts':posts})
    return render(request,'hostPage.html')

#신청한 멘티 페이지
def participantPage(request):
    user = request.user
    if user.is_active:
        ideas = Idea.objects.filter(i_writer=user)
        post_list=[]
        for idea in ideas:
            if idea.post not in post_list:
                post_list.append(idea.post)
        return render(request, 'participantPage.html', {'post_list':post_list})
    return render(request,'participantPage.html')

#좋아요 모음 페이지
def likedPage(request):
    user = request.user
    if user.is_active:
        likes=Like.objects.select_related()
        return render(request, 'likedPage.html', {'likes':likes})
    return render(request,'likedPage.html')

def allIdea(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    ideas = Idea.objects.filter(post=post)
    return render(request,'allIdea.html', {'post':post,'ideas':ideas})

#게시글 등록 페이지
def createPost(request):
    return render(request, 'createPost.html')

#U
def edit(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    post_categories = Category.objects.all().filter(post=post)
    post_category_list = []
    for post_category in post_categories :
        post_category_list.append(post_category.category_name)

    categories = ['운동 및 취미', '대학생활','학업']

    return render(request, 'editPost.html', {'post':post,
                                            'post_category_list':post_category_list,
                                            'categories':json.dumps(categories)
                                            })

def update(request, post_id):

    post=get_object_or_404(Post, pk=post_id)
    post.title=request.POST['title']
    post.content=request.POST['content']

    post.manager=request.user
    categories = Category.objects.filter(post = post)
    for category in categories:
        category.delete()
    #post.save()

    checked_categories=request.POST.getlist('category[]')
    for checked_category in checked_categories:
        category = Category()
        category.category_name = checked_category
        category.post = post
        category.save()
        
    post.save()

    return redirect('/contestPost/'+str(post.id))

#D
def delete(request, post_id):
    post=get_object_or_404(Post, pk=post_id) 
    post.delete()

    return redirect('home')


#서치관련
def search(request):
    post_list=Post.objects.all().order_by('-id')
    m=request.GET.get('post_name','init')

    posts=None
    if m:
        posts=post_list.filter(title__icontains=m)
    
    return render(request, 'search.html', {
        'posts':post_list,
        'post_search': posts,
        'm':m,
    })

def category(request, c_name):
    #TODO HTML에서 받을 때 {% url '' category_name = 넣을 변수명 %} 테스트 해보기
    category_posts=[]
    category_list =Category.objects.all().filter(category_name=c_name)
    for category in category_list:
        if category.post not in category_posts: 
            category_posts.append(category.post)
            
    return render(request,'search.html' , {'c_name': c_name, 'category_posts': category_posts})


# def post_like(request, post_id):
#     user = request.user # 로그인된 유저의 객체를 가져온다.
#     post = get_object_or_404(Post, pk=post_id) # 좋아요 버튼을 누를 글을 가져온다.

#     # 이미 좋아요를 눌렀다면 좋아요를 취소, 아직 안눌렀으면 좋아요를 누른다.
#     if post.likes.filter(id=user.id): # 로그인한 user가 현재 post 객체에 좋아요를 눌렀다면
#         post.likes.remove(user) # 해당 좋아요를 없앤다.
#         message="Favorites_Registered"
#     else: # 아직 좋아요를 누르지 않았다면
#         post.likes.add(user) # 좋아요를 추가한다.
#         message="Favorites_Unregistered"
        
#     ret = {
#         'message' : message,
#         'num' : post.like_count(),
#     }

#     return HttpResponse(json.dumps(ret), content_type="application/json")
    
#     # redirect('/contestPost/'+str(post.id))

def post_like(request):

    if request.is_ajax():
        blog_id = request.GET['post_id'] #좋아요를 누른 게시물id가지고 오기
        post = Post.objects.get(id=blog_id) 

        user = request.user # 로그인된 유저의 객체를 가져온다.     
        
        if not request.user.is_authenticated: #버튼을 누른 유저가 비로그인 유저일 때
                message = "로그인을 해주세요" #화면에 띄울 메세지 
                ret = {'like_count' : post.likes.count(),"message":message}
                return HttpResponse(json.dumps(ret), content_type='application/json')

        # 이미 좋아요를 눌렀다면 좋아요를 취소, 아직 안눌렀으면 좋아요를 누른다.
        if post.likes.filter(id=user.id).exists(): # 로그인한 user가 현재 post 객체에 좋아요를 눌렀다면
            post.likes.remove(user) # 해당 좋아요를 없앤다.
            message="좋아요"
        else: # 아직 좋아요를 누르지 않았다면
            post.likes.add(user) # 좋아요를 추가한다.
            message="좋아요취소"
            
        ret = {
            'message' : message,
            'num' : post.likes.count(),
        }

        return HttpResponse(json.dumps(ret), content_type="application/json")
     
#댓글 관련
def comment_create(request, post_id):
    if request.method == "POST":
        comment=Comment()
        comment.c_writer = request.user
        comment.body = request.POST['body']
        comment.pub_date = timezone.datetime.now()
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
        return redirect('/contestPost/'+str(post_id))
    else:
        return redirect('/contestPost/'+str(post_id))

def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    comment.delete()

    return redirect('/contestPost/'+str(post_id))


# 참여관련
def createI(request, post_id):
    if request.method == "POST":
        user = request.user
        post=get_object_or_404(Post, pk=post_id)
        ideas = Idea.objects.filter(i_writer=user , post=post)

        if ideas.exists():
            participate_idea = ideas.first()

            message='본인의 게시물이거나 이미 참여하신 게시물입니다.'
            categories = Category.objects.all().filter(post = post)

            if post.likes.filter(id=user.id):
                state="Favorites_Registered"
            else:
                state="Favorites_Unregistered"

            comments = Comment.objects.all().filter(post = post)
            return render(request,'contestPost.html' ,{'post':post, 'state':state, 'comments':comments, 'categories':categories, 'message':message, 'participate_idea':participate_idea})
        #한번만참여하게처리

        idea=Idea()
        idea.i_writer = user
        idea.title=request.POST['title']
        idea.body=request.POST['content']

        idea.pub_date = timezone.datetime.now()
        idea.post = post
        idea.save()
        return redirect('/contestPost/'+str(post_id)+'/contestIdea/'+str(idea.id))
    else:
        return redirect('/contestPost/'+str(post_id)+'/contestIdea/'+str(idea.id))

#멘티 신청 페이지
def createIdea(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    return render(request, 'createIdea.html', {'post':post})

#멘티 신청 게시글
def contestIdea(request, post_id, idea_id):
    idea=get_object_or_404(Idea, pk=idea_id)
    post=get_object_or_404(Post, pk=post_id)
    # post=get_object_or_404(Post, pk=idea.post.id)
    return render(request,'contestIdea.html',{'post':post , 'idea':idea} )

#멘티 신청 삭제
def deleteI(request, post_id, idea_id):
    idea=get_object_or_404(Idea, pk=idea_id)
    #post_id=idea.post.id
    idea.delete()
    return redirect('/contestPost/'+str(post_id))


def selectI(request, post_id, idea_id):
    idea=get_object_or_404(Idea, pk=idea_id)
    post=get_object_or_404(Post, pk=post_id)
    pre_selected_idea = None
    pre_selected_idea = Idea.objects.filter(post=post, selected=True).first()
    if pre_selected_idea is not None:
        pre_selected_idea.selected = False
        pre_selected_idea.save()
    
    idea.selected = True
    idea.save()
    return render(request,'contestIdea.html',{'post':post , 'idea':idea} )