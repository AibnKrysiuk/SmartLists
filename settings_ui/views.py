# settings_ui/views.py

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView # Para la edición de perfil
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .forms import ProfileEditForm, PreferencesForm
from .models import UserPreferences

User = get_user_model()

class SettingsView(LoginRequiredMixin, View):
    """
    Vista base y de bienvenida del centro de configuraciones.
    """
    def get(self, request):
        return render(request, 'settings_ui/settings_base.html', {'active_tab': 'welcome'})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Vista para que el usuario edite su propio perfil.
    Utiliza el generic UpdateView.
    """
    model = User
    form_class = ProfileEditForm
    template_name = 'settings_ui/profile_edit.html'
    
    # URL a la que redirigir después de guardar el formulario exitosamente
    success_url = reverse_lazy('settings_ui:profile') 

    def get_object(self, queryset=None):
        """Asegura que solo se edite el perfil del usuario logueado."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Añade la pestaña activa al contexto del template."""
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'profile'
        return context
    
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """
    Vista que maneja el cambio de contraseña del usuario.
    Utiliza el generic PasswordChangeView de Django.
    """
    # El formulario de cambio de contraseña se gestiona automáticamente por Django
    template_name = 'settings_ui/password_change_form.html'
    
    # Redirige a la misma página después de un cambio exitoso
    success_url = reverse_lazy('settings_ui:password_change') 

    def form_valid(self, form):
        # Añade un mensaje de éxito después de cambiar la contraseña
        messages.success(self.request, 'Tu contraseña ha sido actualizada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Añade la pestaña activa al contexto del template."""
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'password' # Marca la pestaña 'password' como activa
        return context

class PreferencesEditView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar las preferencias del usuario.
    Usamos get_object para crear la entrada si no existe (el perfil es nuevo).
    """
    model = UserPreferences
    form_class = PreferencesForm
    template_name = 'settings_ui/preferences_form.html'
    success_url = reverse_lazy('settings_ui:preferences') 

    def get_object(self, queryset=None):
        """
        Intenta obtener las preferencias del usuario. Si no existen, las crea.
        """
        obj, created = self.model.objects.get_or_create(user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        """Añade la pestaña activa al contexto del template."""
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'preferences'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tus preferencias han sido guardadas.')
        return super().form_valid(form)