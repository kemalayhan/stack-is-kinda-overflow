from django.db import models

# Create your models here.

class Tag(models.Model):
    title       = models.CharField(max_length=50)
    content     = models.TextField(null=True, blank=True)
    tag_image   = models.ImageField(upload_to="tag_image")

    def __str__(self):
        return self.title
    