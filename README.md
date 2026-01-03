# 📝 SmartLists: Tu Gestor de Listas Inteligente

SmartLists es una aplicación web full-stack desarrollada con Django. Permite a los usuarios crear, gestionar y compartir listas de inventario (Stock) y listas de tareas (Checklists) de manera eficiente. Su principal característica es la flexibilidad, el reordenamiento dinámico y la capacidad de exportación e importación de datos.

## ✨ Características Principales

* **Tipos de Lista:** Soporte para listas de Stock (con cantidad/unidad) y Checklists (con estado de completado).
* **Reordenamiento Dinámico (Drag & Drop):** Permite arrastrar y soltar ítems y subtítulos para organizar la lista de forma intuitiva.
* **Secciones/Subtítulos:** Organiza listas largas dividiéndolas en secciones lógicas.
* **Exportación de Datos Avanzada:**
    * **JSON:** Exporta/Importa la lista completa (incluyendo estructura y metadatos) para transferencias entre usuarios o copias de seguridad.
    * **Texto Plano:** Copia la lista en un formato legible, ideal para compartir rápidamente por WhatsApp o cualquier mensajería.
    * **PDF:** (Funcionalidad pendiente de despliegue) Generación de un documento PDF estructurado para impresión o archivo.
* **Autenticación Segura:** Inicio de sesión y registro de usuarios con control de acceso por lista.

## 🚀 Despliegue y Uso

### Despliegue en Producción

La aplicación está desplegada actualmente en [Render](https://render.com).

* **URL de Producción:** `[AQUÍ VA EL ENLACE DE TU APLICACIÓN EN RENDER]`

### Requisitos del Sistema

Para el desarrollo local o si deseas correr la aplicación desde cero:

* Python 3.8+
* pip (Administrador de paquetes de Python)
* PostgreSQL (Recomendado para producción)

### Instalación Local (Entorno de Desarrollo)

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://www.youtube.com/watch?v=9d7lq4oMyPk](https://www.youtube.com/watch?v=9d7lq4oMyPk)
    cd SmartLists
    ```

2.  **Crear y Activar el Entorno Virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # Linux/macOS
    ```

3.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
    *Nota: Si estás en un entorno Linux, la instalación de `WeasyPrint` puede requerir la instalación previa de librerías como `libcairo2` y `libpango1.0-0`.*

4.  **Configurar la Base de Datos y Variables de Entorno:**
    * Crea un archivo `.env` o usa tu método preferido para gestionar `SECRET_KEY`, `DEBUG`, y la configuración de la base de datos (PostgreSQL/SQLite).

5.  **Ejecutar Migraciones:**
    ```bash
    python manage.py migrate
    ```

6.  **Crear Superusuario (Opcional):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el Servidor:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## 🛠️ Tecnologías Utilizadas

* **Backend:** [Django](https://www.djangoproject.com/) (Python)
* **Base de Datos:** SQLite (Desarrollo), PostgreSQL (Producción)
* **Frontend:** HTML, CSS, JavaScript Vanilla
* **Librerías Clave:**
    * **SortableJS:** Para la funcionalidad Drag and Drop.
    * **WeasyPrint:** Para la generación de documentos PDF (requiere dependencias de sistema).

## 🤝 Contribuciones

Si deseas contribuir, por favor:

1.  Haz un *fork* del repositorio.
2.  Crea una rama de característica (`git checkout -b feature/nueva-funcionalidad`).
3.  Confirma tus cambios (`git commit -m 'feat: Añade nueva funcionalidad X'`).
4.  Empuja la rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un *Pull Request*.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---
*Hecho con 💙 por AibnKrysiuk
