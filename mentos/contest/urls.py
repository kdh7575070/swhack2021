from django.urls import path, include
import contest.views

urlpatterns = [
    path('', contest.views.home, name="home"),
    path('hostPage/', contest.views.hostPage, name="hostPage"),
    path('participantPage/', contest.views.participantPage, name="participantPage"),
    path('likedPage/', contest.views.likedPage, name='likedPage'),

    path('contestPost/createPost/', contest.views.createPost, name="createPost"),
    path('contestPost/create/', contest.views.create, name="create"),
    path('contestPost/<int:post_id>', contest.views.contestPost, name="contestPost"),
    path('contestPost/editPost/<int:post_id>', contest.views.edit, name='editPost'),
    path('contestPost/update/<int:post_id>', contest.views.update, name='update'),
    path('contestPost/delete/<int:post_id>', contest.views.delete, name='delete'),
    #path('contestPost/post_like/<int:post_id>', contest.views.post_like, name='post_like'),
    path('contestPost/post/like', contest.views.post_like, name='post_like'),
    
    #Search
    path('search/',contest.views.search, name='search'),
    path('category/<str:c_name>',contest.views.category, name='category'),

    #Comment
    path('contestPost/<int:post_id>/comment_create',contest.views.comment_create, name='comment_create'),
    path('contestPost/<int:post_id>/comment_delete/<int:comment_id>',contest.views.comment_delete, name='comment_delete'),

    #Idea
    path('contestPost/<int:post_id>/createIdea', contest.views.createIdea, name='createIdea'),
    path('contestPost/<int:post_id>/createI', contest.views.createI, name='createI'),
    path('contestPost/<int:post_id>/allIdea', contest.views.allIdea, name='allIdea'),
    path('contestPost/<int:post_id>/contestIdea/<int:idea_id>', contest.views.contestIdea, name='contestIdea'),
    path('contestPost/<int:post_id>/deleteI/<int:idea_id>', contest.views.deleteI, name='deleteI'),
    path('contestPost/<int:post_id>/selectI/<int:idea_id>', contest.views.selectI, name='selectI'),
    
]