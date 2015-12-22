from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('headline',)}


admin.site.register(Article, ArticleAdmin)
