# settings_ui/urls.py

from django.urls import path
from .views import SettingsView, ProfileEditView, PasswordChange,PreferencesEditView

app_name = 'settings_ui'

urlpatterns = [
    # Ruta principal de Settings (referenciada en el Dashboard)
    path('', SettingsView.as_view(), name='settings'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
    path('password/', PasswordChange.as_view(), name='password_change'),
    path('preferences/', PreferencesEditView.as_view(), name='preferences'),
    
    # Próximamente: Rutas para Account, Preferences, etc.
    # path('account/', SettingsAccountView.as_view(), name='account'),
]