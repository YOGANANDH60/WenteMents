from django.contrib import admin
from .models import category
from .models import product
from .models import productImages
from .models import articals




# from .models import * (for all)

class productImageAdmin(admin.TabularInline):
    model = productImages

class productAdmin(admin.ModelAdmin):
    inlines = [productImageAdmin]
    list_display = ['pname','nprice']


class categoryAdmin(admin.ModelAdmin):
    list_display = ['name','created_at']

class articalsAdmin(admin.ModelAdmin):
    list_display = ['blog_name','created_at']


    

admin.site.register(category,categoryAdmin)
admin.site.register(product,productAdmin)
admin.site.register(articals,articalsAdmin)



