# settings_ui/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreferences(models.Model):
    """
    Modelo para guardar las preferencias específicas de la aplicación por usuario.
    Se conecta al modelo User con una relación OneToOne.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Preferencia de tema (Modo Claro vs Modo Oscuro)
    is_dark_mode = models.BooleanField(default=False)
    
    # Umbral de Stock por defecto para notificaciones (ej: avisar si hay menos de 5 unidades)
    default_stock_threshold = models.IntegerField(default=5)
    
    # Opcional: Idioma de la interfaz (podría ser útil más adelante)
    language = models.CharField(max_length=5, default='es')

    def __str__(self):
        return f"Preferences for {self.user.username}"