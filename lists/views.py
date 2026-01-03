# lists/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.db import transaction
import json

# IMPORTANTE: Usar get_user_model() en lugar de importar User directamente
User = get_user_model() 

# Asumo que tus forms se llaman ListForm y ItemForm (como en los ejemplos anteriores)
# Nota: La importación ListCreateForm no parece coincidir con la convención común (la cambio a ListForm para la solución)
from .models import List, Item
#from .forms import ListCreateForm, ItemForm # Reemplazar con
from .forms import ListForm, ItemForm, SubtitleForm

import json
from django.http import JsonResponse
from django.db import transaction # Útil para asegurar la consistencia
from .utils import format_list_to_plaintext


# ==========================================================
# 1. VISTAS PRINCIPALES (Dashboard y Creación)
# ==========================================================

# VISTA CORREGIDA Y ÚNICA (Reemplaza a ListDashboardView y la DashboardView anterior)
class DashboardView(LoginRequiredMixin, View):
    """ Muestra el panel de control con todas las listas creadas por el usuario logueado. """
    template_name = 'lists/dashboard.html'
    
    def get(self, request):
        # Obtener solo las listas que pertenecen al usuario actual, ordenadas por actualización
        user_lists = List.objects.filter(user=request.user).order_by('-updated_at')

        context = {
            'user_lists': user_lists,
            'page_title': 'My Lists',
        }
        return render(request, self.template_name, context)
    
class ListCreateView(LoginRequiredMixin, CreateView):
    """ Permite a los usuarios logueados crear una nueva lista. """
    model = List
    form_class = ListForm # Asegúrate de que tu form se llama ListForm
    template_name = 'lists/list_form.html' # Usamos la misma plantilla que Update

    def form_valid(self, form):
        form.instance.user = self.request.user 
        messages.success(self.request, "New list created successfully!")
        return super().form_valid(form)
        
    def get_success_url(self):
        # Redirige al detalle de la lista recién creada
        return reverse('lists:detail', kwargs={'pk': self.object.pk})

# ==========================================================
# 2. VISTAS CRUD DE LISTAS (Actualización y Eliminación)
# ==========================================================

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    fields = ['title', 'list_type']
    template_name = 'lists/list_form.html' 

    # IMPORTANTE: Limita para que solo el dueño pueda editar su lista
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
        
    def get_success_url(self):
        messages.success(self.request, f"List '{self.object.title}' updated successfully.")
        return reverse('lists:dashboard')

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = 'lists/list_confirm_delete.html' 
    success_url = reverse_lazy('lists:dashboard')
    
    # IMPORTANTE: Limita para que solo el dueño pueda eliminar su lista
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Mensaje de confirmación antes de borrar
        messages.warning(self.request, f"List '{self.object.title}' was successfully deleted.")
        return super().form_valid(form)

# ==========================================================
# 3. VISTA DE DETALLE DE LISTA Y LÓGICA DE ÍTEMS
# ==========================================================

class ListaDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = 'lists/list_detail.html'
    context_object_name = 'list_data' 
    
    # Asegura que solo vea sus propias listas
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_obj = context['list_data']

        all_items = list_obj.items.all().order_by('order', 'pk') 
        context['items'] = all_items
        
        context['page_title'] = list_obj.title
        context['item_form'] = context.get('item_form', ItemForm())
        
        # 🆕 INCLUIMOS EL FORMULARIO DE SUBTÍTULO 🆕
        context['subtitle_form'] = context.get('subtitle_form', SubtitleForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        
        # 🆕 DETERMINAMOS QUÉ FORMULARIO SE ESTÁ ENVIANDO 🆕
        # Usamos el campo oculto 'is_subtitle_submit' del formulario HTML
        if 'is_subtitle_submit' in request.POST:
            form = SubtitleForm(request.POST)
        else:
            form = ItemForm(request.POST) 
        
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.list = self.object
            
            # Si es un Ítem normal y es Checklist, ajustamos defaults
            if not new_item.is_subtitle and self.object.list_type == 'checklist':
                new_item.quantity = 0 
                new_item.unit = '' # Aseguramos unidad vacía
                new_item.is_completed = False
            
            # Si es Subtítulo, la lógica de defaults ya fue manejada por SubtitleForm.save()
            
            new_item.save()
            messages.success(request, f"'{new_item.name}' added successfully!")
            return redirect(self.object.get_absolute_url()) 
        
        # Si el formulario falla, re-renderiza con el formulario fallido
        context = self.get_context_data(object=self.object)
        
        if 'is_subtitle_submit' in request.POST:
             context['subtitle_form'] = form 
             messages.error(request, "Error creating section/subtitle. Please check the name.")
        else:
            context['item_form'] = form 
            messages.error(request, "Error creating item. Please check the fields.")

        return self.render_to_response(context)


# ==========================================================
# 4. VISTAS CRUD DE ÍTEMS (Deben ser incluidas)
# ==========================================================

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['quantity', 'is_completed'] 

    def get_queryset(self):
        return self.model.objects.filter(list__user=self.request.user)

    def get_success_url(self):
        item = self.object 
        messages.success(self.request, f"Item '{item.name}' updated successfully.")
        return reverse('lists:detail', kwargs={'pk': item.list.pk})
    
    # Manejar POST simple para el formulario inline (checkbox/cantidad)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    
    def get_queryset(self):
        return self.model.objects.filter(list__user=self.request.user)

    def get_success_url(self):
        list_pk = self.object.list.pk 
        messages.warning(self.request, f"Item '{self.object.name}' deleted.")
        return reverse('lists:detail', kwargs={'pk': list_pk})
    
    # Permitir eliminación por GET (es menos seguro, pero común en botones de lista)

class ItemReorderView(LoginRequiredMixin, View):
    """
    Recibe una lista ordenada de IDs de ítems por POST y actualiza
    el campo 'order' de cada ítem en la lista.
    """
    def post(self, request, pk):
        # 1. Asegurar que la lista existe y pertenece al usuario
        list_obj = get_object_or_404(List, pk=pk, user=request.user)
        
        try:
            # 2. Obtener los IDs de la solicitud AJAX (formato JSON)
            data = json.loads(request.body)
            # Esperamos que 'item_ids' sea una lista en el orden deseado
            ordered_item_ids = data.get('item_ids', []) 
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        # 3. Validar y actualizar el orden en una transacción
        with transaction.atomic():
            # Itera sobre los IDs, asignando el índice + 1 como valor de 'order'
            for index, item_id in enumerate(ordered_item_ids):
                try:
                    # Filtramos por el ID del ítem Y aseguramos que pertenezca a la lista
                    Item.objects.filter(list=list_obj, pk=item_id).update(order=index + 1)
                except Exception as e:
                    # Si falla la actualización, logueamos y retornamos un error
                    print(f"Error updating item {item_id}: {e}")
                    # Podrías optar por Transaction.rollback() aquí, pero transaction.atomic() lo hace automático si hay una excepción.
                    return JsonResponse({'error': f'Failed to update item ID {item_id}.'}, status=500)

        # 4. Respuesta exitosa
        return JsonResponse({'success': True, 'message': 'Items reordered successfully.'})
    
class ListExportView(LoginRequiredMixin, View):
    """
    Serializa una lista y sus ítems en formato JSON y fuerza la descarga.
    """
    def get(self, request, pk):
        # 1. Recuperar la lista y asegurar que pertenece al usuario
        list_obj = get_object_or_404(List, pk=pk, user=request.user)

        # 2. Serializar los ítems
        items_data = []
        # El orden ya está asegurado por el campo 'order'
        for item in list_obj.items.all().order_by('order'): 
            items_data.append({
                # Incluimos solo los campos necesarios para la recreación
                'name': item.name,
                'is_subtitle': item.is_subtitle,
                'quantity': item.quantity,
                'unit': item.unit if item.unit else None, # Exportar None si está vacío
                'is_completed': item.is_completed, 
                # NO incluimos: pk, created_at, list_id, user.
            })
            
        # 3. Serializar los datos de la lista
        export_data = {
            'metadata': {
                'title': list_obj.title,
                'list_type': list_obj.list_type,
                'exported_by': request.user.get_username(),
                'export_date': list_obj.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                'version': '1.0' # Para futuras validaciones de importación
            },
            'items': items_data
        }

        # 4. Convertir a JSON
        json_content = json.dumps(export_data, indent=4, ensure_ascii=False)
        
        # 5. Configurar la respuesta HTTP para la descarga
        response = HttpResponse(json_content, content_type='application/json')
        filename = f"{list_obj.title.replace(' ', '_')}_export.json"
        
        # Establecer el encabezado para forzar la descarga del archivo
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
class ListImportView(LoginRequiredMixin, View):
    """
    Maneja la subida de archivos JSON, valida la estructura y crea una nueva lista y sus ítems.
    """
    def post(self, request):
        if 'json_file' not in request.FILES:
            messages.error(request, "Debe subir un archivo JSON.")
            return redirect('lists:dashboard')

        json_file = request.FILES['json_file']
        
        # Validación básica de extensión
        if not json_file.name.endswith('.json'):
            messages.error(request, "El archivo debe ser de formato .json.")
            return redirect('lists:dashboard')

        try:
            # 1. Leer y decodificar el archivo
            file_content = json_file.read().decode('utf-8')
            imported_data = json.loads(file_content)

            # 2. Validar estructura
            metadata = imported_data.get('metadata')
            items_data = imported_data.get('items')
            
            if not metadata or not items_data or 'title' not in metadata or 'list_type' not in metadata:
                messages.error(request, "Estructura del archivo JSON no válida. Faltan metadatos o ítems.")
                return redirect('lists:dashboard')

        except (json.JSONDecodeError, UnicodeDecodeError):
            messages.error(request, "Error al decodificar el archivo JSON.")
            return redirect('lists:dashboard')
        
        # 3. Crear la nueva lista y sus ítems dentro de una transacción
        try:
            with transaction.atomic():
                # Crear la nueva lista (vinculada al usuario actual)
                new_list = List.objects.create(
                    user=request.user,
                    title=f"[Imported] {metadata['title']}", # Prefijo para identificarla
                    list_type=metadata['list_type']
                )
                
                # Contador para el campo 'order'
                item_order = 1 
                
                # Crear los ítems
                for item_data in items_data:
                    # Crear el ítem con los datos importados
                    Item.objects.create(
                        list=new_list,
                        name=item_data.get('name', 'Unnamed Item'),
                        is_subtitle=item_data.get('is_subtitle', False),
                        quantity=item_data.get('quantity', 0),
                        unit=item_data.get('unit') if item_data.get('unit') is not None else '',
                        is_completed=item_data.get('is_completed', False),
                        order=item_order # Asignamos el orden importado
                    )
                    item_order += 1

            messages.success(request, f"Lista '{new_list.title}' importada exitosamente.")
            return redirect('lists:detail', pk=new_list.pk) # Redirigir a la nueva lista

        except Exception as e:
            messages.error(request, f"Error interno al crear la lista: {e}")
            return redirect('lists:dashboard')
        
class ListExportTextView(LoginRequiredMixin, View):
    """
    Genera el texto plano de la lista y lo devuelve para copiar/descargar.
    """
    def get(self, request, pk):
        list_obj = get_object_or_404(List, pk=pk, user=request.user)
        
        # Usamos la función de utilidad para generar el texto
        plaintext_content = format_list_to_plaintext(list_obj)

        # Configuramos la respuesta como texto simple
        response = HttpResponse(plaintext_content, content_type='text/plain')
        
        # Opcional: Si quieres forzar la descarga de un .txt en lugar de solo mostrarlo:
        # filename = f"{list_obj.title.replace(' ', '_')}_list.txt"
        # response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response