import os
from io import BytesIO

from PIL import Image 

from django_resized import ResizedImageField as BaseResizedImageField
from django.core.files.base import ContentFile


class ResizedImageField(BaseResizedImageField):
    """
    Fix bug for saving webp images.
    """
    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        if not file:
            return file

        if not file.name.lower().endswith('.webp'):
            return super().pre_save(model_instance, add)

        try:
            if callable(self.upload_to):
                filename = self.upload_to(model_instance, file.name)
            else:
                filename = os.path.join(self.upload_to, os.path.basename(file.name))

            img = Image.open(file)
            img = img.convert('RGB')

            if self.size:
                img.thumbnail((self.size[0], self.size[1]), Image.ANTIALIAS)

            output = BytesIO()
            img.save(output, format='WEBP', quality=self.quality or 75)
            output.seek(0)

            self.storage.save(filename, ContentFile(output.read()))
            setattr(model_instance, self.attname, filename)

            return filename
        except Exception as e:
            print(f"ResizedImageField - saving image error: {e}")
            return super().pre_save(model_instance, add)
