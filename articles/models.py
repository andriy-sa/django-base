from django.db import models
from users.models import MyUser

class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)

class Entry(models.Model):
    title      = models.CharField(max_length=200)
    body       = models.TextField()
    slug       = models.SlugField(max_length=200, unique=True)
    publish    = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(MyUser, related_name='articles', on_delete=models.CASCADE)

    objects = EntryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles List"
        ordering = ["-created_at"]
