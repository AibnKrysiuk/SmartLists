# lists/urls.py

from django.urls import path
from .views import (
    DashboardView, 
    ListCreateView, 
    ListaDetailView, 
    ItemUpdateView,      
    ItemDeleteView,
    ListUpdateView,  # Vista para Editar Lista
    ListDeleteView,
    ListExportView,
    ListImportView,
    ListExportTextView  # Vista para Eliminar Lista
)
from .views import ItemReorderView

app_name = 'lists'

urlpatterns = [
    # 1. Rutas del Dashboard y Creación de Listas
    path('', DashboardView.as_view(), name='dashboard'),
    path('create/', ListCreateView.as_view(), name='create'),
    
    # 2. Rutas CRUD de Listas (Listas Existentes)
    
    # Detalle de Lista (Leer)
    path('<int:pk>/', ListaDetailView.as_view(), name='detail'), 
    
    # Edición de Lista (Actualizar) - Usada por el menú "Edit List"
    path('<int:pk>/edit/', ListUpdateView.as_view(), name='list_update'),
    
    # Eliminación de Lista (Eliminar) - Usada por el menú "Delete List"
    path('<int:pk>/delete/', ListDeleteView.as_view(), name='list_delete'),
    
    
    # 3. Rutas CRUD de Ítems (Relacionadas a Listas)
    
    # Actualizar Ítem (Usado para cambiar cantidad o estado 'is_completed')
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    
    # Eliminar Ítem (Usado para el botón de basura en la lista de detalle)
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),

    # Reordenamiento Dinámico (Endpoint para AJAX)
    # Nota: No lleva PK de ítem, solo el PK de la lista para seguridad
    path('<int:pk>/reorder/', ItemReorderView.as_view(), name='reorder_items'),

    # 🆕 EXPORTACIÓN DE LISTA EN FORMATO JSON 🆕
    path('<int:pk>/export/json/', ListExportView.as_view(), name='export_json'),

    # 🆕 EXPORTACIÓN DE LISTA EN TEXTO PLANO 🆕
    path('<int:pk>/export/text/', ListExportTextView.as_view(), name='export_plaintext'),

    # 🆕 IMPORTACIÓN DE LISTA DESDE JSON 🆕
    path('import/json/', ListImportView.as_view(), name='import_json'),
]