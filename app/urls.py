from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

# Creating Router onject
router = DefaultRouter()

# Register BlogModelViewSet with Router
router.register('blog_api', BlogModelViewSet, basename='blogs')

urlpatterns = [
    path('', home, name="home"),

    path('dashboard/', dashboard, name="dashboard"),

    path('login/', login, name="login"),

    path('logout/', logout, name="logout"),

    path('register/', register, name="register"),

    path('update_profile/', update_profile, name="update_profile"),

    path('blogdetail/<slug>/', blogdetail, name="blogdetail"),

    path('create_blog/', create_blog, name="create_blog"),

    path('delete_blog/<slug>/', delete_blog, name="delete_blog"),

    path('password_reset/', PasswordResetView.as_view(
        template_name='forgotpassword.html'), name="password_reset"),

    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='resetdone.html'), name="password_reset_done"),

    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='resetconfirm.html'), name="password_reset_confirm"),

    path('password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='resetcomplete.html'), name="password_reset_complete"),

    path('', include(router.urls)),
]
