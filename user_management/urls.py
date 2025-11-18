from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    # User endpoints
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('permissions/', views.UserPermissionsView.as_view(), name='user_permissions'),

]
