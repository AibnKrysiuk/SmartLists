# settings_ui/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import UserPreferences

# Obtener el modelo de usuario activo (por defecto es django.contrib.auth.models.User)
User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    """
    Formulario para la edición del perfil del usuario (nombre, apellido, etc.).
    """
    class Meta:
        model = User
        # Solo permitimos editar el nombre, apellido y correo electrónico.
        # No incluimos la contraseña ni el nombre de usuario.
        fields = ('first_name', 'last_name', 'email')
        
        # Opcional: Personalizar etiquetas
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

class PreferencesForm(forms.ModelForm):
    """
    Formulario para la edición de las preferencias del usuario.
    """
    class Meta:
        model = UserPreferences
        fields = ('is_dark_mode', 'default_stock_threshold', 'language')
        
        labels = {
            'is_dark_mode': 'Enable Dark Mode',
            'default_stock_threshold': 'Default Low Stock Threshold',
            'language': 'Language',
        }