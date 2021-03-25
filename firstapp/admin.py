from django.contrib import admin

from .models import Document, Application, News

admin.site.register(Document)
admin.site.register(Application)
admin.site.register(News)