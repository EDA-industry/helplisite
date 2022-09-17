from django.contrib import admin
from .models import Category, Product, Tag, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title', 'adress', 'product_id')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)

admin.site.register(Product, ProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    prepopulated_fields = {'slug': ('user',)}
    autocomplete_fields = ('products',)

admin.site.register(Cart, CartAdmin)

class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
