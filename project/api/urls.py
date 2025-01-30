from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

# Register viewsets with the router
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')  # Corrected `basename`
router.register('profile', views.UserProfileViewSet)  # No `basename` needed as `queryset` is defined in the viewset
router.register('feed', views.UserProfileFeedViewSet)  # No `basename` needed

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]
