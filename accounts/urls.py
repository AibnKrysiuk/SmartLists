from django.urls import path
from . import views
# Importamos las vistas de autenticación integradas de Django
from django.contrib.auth import views as auth_views 
from .views import RegisterView

# accounts/urls.py

# ...
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # 2. LOGOUT - SIN ARGUMENTO next_page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    
    # 3. REGISTRO
    path('register/', RegisterView.as_view(), name='register'),
]