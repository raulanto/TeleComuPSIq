from django.core.files.storage import Storage
from django.conf import settings
import os

class CustomStorage(Storage):
    def _save(self, name, content):
        # Guardar el archivo en el sistema de archivos local
        file_path = os.path.join(settings.MEDIA_ROOT, name)
        with open(file_path, 'wb') as f:
            f.write(content.read())
        return name

    def url(self, name):
        # Obtener la URL del archivo en el sistema de archivos local
        return settings.MEDIA_URL + name