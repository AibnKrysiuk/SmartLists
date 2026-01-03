# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.views import generic

# Clase de Vista Genérica para Registro
class RegisterView(generic.CreateView):
    """
    Maneja el registro de nuevos usuarios.
    """
    form_class = UserCreationForm
    # Redirige a la página de login después de un registro exitoso.
    success_url = reverse_lazy('login') 
    # Usa el template compartido.
    template_name = 'accounts/login.html' 
    
    # Sobrescribir el método GET para pasar un contexto que indique qué pestaña está activa
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Esto es crucial para que el template sepa mostrar el formulario de registro.
        context['is_register_tab'] = True 
        return context