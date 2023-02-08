from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users

router = DefaultRouter()

router.register(r'search', users.UserListSearchView, basename='users-search')

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg'),
    path('users/change-passwd/', users.ChangePasswordView.as_view(), name='change_passwd'),
    path('users/me/', users.MeView.as_view(), name='me'),
]

urlpatterns += path('users/', include(router.urls)),
