from django.urls import path

from apps.posts.views import MyPostListAPIView, PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, \
    bookmark_post_api_view, unbookmark_post_api_view

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("my/", MyPostListAPIView.as_view(), name="post-my"),
    path("<slug:slug>/", PostRetrieveUpdateDestroyAPIView.as_view(), name="post-retrieve-update-destroy"),
    path("<slug:slug>/bookmark/", bookmark_post_api_view, name="post-bookmark"),
    path("<slug:slug>/unbookmark/", unbookmark_post_api_view, name="post-unbookmark"),
]
