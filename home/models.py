from django.db import models

# Create your models here.

from simditor.fields import RichTextField
# from ckeditor.fields import RichTextField


class Home(models.Model):
    about = RichTextField(blank=True)
