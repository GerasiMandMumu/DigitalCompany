from django.contrib import admin

from .models import Document, Application, News, UserQuestion

admin.site.register(Document)
admin.site.register(Application)
admin.site.register(News)
admin.site.register(UserQuestion)