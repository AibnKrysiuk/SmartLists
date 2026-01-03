# lists/forms.py

from django import forms
from .models import List, Item

# RENOMBRADO para coincidir con la importación ListForm usada en views.py
class ListForm(forms.ModelForm):
    """
    Formulario para crear o actualizar una lista.
    """
    class Meta:
        model = List
        # Solo necesitamos que el usuario ingrese el título y el tipo.
        fields = ('title', 'list_type')
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Warehouse A Stock, Groceries, To-Do Today'}),
            'list_type': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'title': 'List Name',
            'list_type': 'List Type',
        }

# 🆕 NUEVO FORMULARIO PARA CREAR SUBTÍTULOS 🆕
class SubtitleForm(forms.ModelForm):
    class Meta:
        model = Item
        # Solo necesitamos el nombre del subtítulo
        fields = ('name',) 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Carnes, Bebidas, Tareas de Casa'}),
        }
        labels = {
            'name': 'Subtitle Name / Category',
        }
        
    def save(self, commit=True):
        # Sobreescribimos save para forzar is_subtitle=True y limpiar otros campos
        subtitle = super().save(commit=False)
        subtitle.is_subtitle = True
        subtitle.quantity = 0
        subtitle.unit = ''
        subtitle.is_completed = False
        
        if commit:
            subtitle.save()
        return subtitle

class ItemForm(forms.ModelForm):
    """
    Formulario base para crear un nuevo ítem. 
    """
    class Meta:
        model = Item
        # Solo pedimos el nombre y la cantidad/estado (la vista manejará el ajuste)
        fields = ('name', 'quantity', 'unit') 
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Laptop Pro X, Buy Milk, Check server logs'}),
            'quantity': forms.NumberInput(attrs={'min': 0, 'placeholder': '0'}),
            'unit': forms.TextInput(attrs={'placeholder': 'e.g., kg, units, liters'}),
        }
        
        labels = {
            'name': 'Item Name / Task',
            'quantity': 'Quantity in Stock',
            'unit': 'Unit',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que quantity y unit sean opcionales a nivel de formulario.
        self.fields['quantity'].required = False 
        self.fields['unit'].required = False
    def clean_quantity(self):
        # Asegura que si no se envía, sea 0 (para Checklist)
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            return 0
        return quantity
        
    def clean_unit(self):
        # Asegura que si no se envía, sea cadena vacía (para Checklist)
        unit = self.cleaned_data.get('unit')
        if unit is None:
            return ''
        return unit