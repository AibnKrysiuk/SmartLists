def format_list_to_plaintext(list_obj):
    """
    Genera una representación de texto plano legible de la lista,
    ideal para copiar al portapapeles o compartir en mensajería.
    Formato: Título, Subtítulo, Ítems (con Cantidad y Unidad).
    """
    output = []
    
    # 1. Título de la Lista
    output.append(f"📦 LIST: {list_obj.title.upper()}")
    output.append("-" * (len(list_obj.title) + 12))
    
    # Variable para rastrear el subtítulo actual
    current_subtitle = None
    
    # 2. Iterar sobre los ítems (ordenados por el campo 'order')
    items = list_obj.items.all().order_by('order')
    
    for item in items:
        if item.is_subtitle:
            # Si es un subtítulo, lo establecemos como el nuevo título de sección
            current_subtitle = item.name.upper()
            output.append("\n=== " + current_subtitle + " ===")
            
        else:
            # Si es un ítem normal, lo formateamos
            line = "  - " # Indentación para items
            
            # 2.1 Agregar Nombre
            line += item.name
            
            # 2.2 Agregar Cantidad y Unidad (solo si no es Checklist o si son > 0)
            if list_obj.list_type == 'stock' or item.quantity > 0:
                quantity_str = str(item.quantity)
                
                if item.unit:
                    line += f" ({quantity_str} {item.unit})"
                else:
                    line += f" ({quantity_str})"
            
            # 2.3 Agregar estado para Checklist (opcional, si el usuario lo requiere)
            if list_obj.list_type != 'stock' and item.is_completed:
                 line += " [DONE]"

            output.append(line)
            
    # Unir todas las líneas con saltos de línea
    return "\n".join(output)