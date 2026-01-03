# lists/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class List(models.Model):
    """
    Representa una lista de inventario o una lista de verificación.
    """
    LIST_TYPE_CHOICES = [
        ('stock', 'Stock / Inventory'),
        ('checklist', 'Checklist / To-Do'),
    ]

    title = models.CharField(max_length=100)
    list_type = models.CharField(max_length=10, choices=LIST_TYPE_CHOICES)
    
    # La lista pertenece a un usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # Utiliza la URL 'lists:detail' y le pasa la Primary Key (pk)
        return reverse('lists:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"[{self.list_type.upper()}] {self.title}"

    class Meta:
        ordering = ['title']

class Item(models.Model):
    """
    Representa un ítem dentro de una lista (puede ser un producto de stock o una tarea).
    """
    # Foreign Key a la lista a la que pertenece
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    
    name = models.CharField(max_length=200)

    # 🆕 CAMPO CLAVE PARA SUBTÍTULOS/AGRUPACIÓN
    is_subtitle = models.BooleanField(default=False)
    
    # Campo específico para Stock
    quantity = models.IntegerField(default=0)

    # 🆕 CAMPO CLAVE PARA UNIDADES DE MEDIDA (Opcional)
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unit of Measure")

    # 🆕 CAMPO CLAVE PARA EL REORDENAMIENTO
    order = models.IntegerField(default=0)
    
    # Campo específico para Checklist (tarea completada)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # ... (código __str__ sin cambios) ...
        if self.is_subtitle:
            return f"--- SUBTITLE: {self.name} ---"
            
        if self.unit:
            return f"{self.name} ({self.quantity} {self.unit})"
        return f"{self.name} ({self.quantity})"

    class Meta:
        # 🆕 CAMBIO CLAVE: Ordenar por el nuevo campo 'order'
        # Luego, como desempate, usamos el PK
        ordering = ['order', 'pk']