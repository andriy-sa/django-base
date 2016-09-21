from django.contrib import admin

from . import models
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget

class EntryAdmin(MarkdownModelAdmin):
    list_display = ('title','slug','created_at')
    prepopulated_fields = {'slug' : ('title',)}
    formfield_overrides = {TextField : {'widget':CKEditorWidget}}

admin.site.register(models.Entry, EntryAdmin)
