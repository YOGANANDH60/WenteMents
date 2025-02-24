from django.contrib import admin
from .models import category
from .models import product
from .models import productImages
from .models import articals
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from .models import * (for all)


class productResource(resources.ModelResource):
    class Meta:
        model = product
        fields = ('pname','nprice','quantity','description')


class productImageAdmin(admin.TabularInline):
    model = productImages

class productAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [productImageAdmin]
    list_display = ['pname','nprice']
    search_fields = ['pname']
    list_filter = ['nprice'] #filter by price
    resource_class = productResource


class categoryAdmin(admin.ModelAdmin):
    list_display = ['name','created_at']
    search_fields = ['name']
    list_filter = ['created_at'] #filter by date

class articalsAdmin(admin.ModelAdmin):
    list_display = ['blog_name','created_at']


    

admin.site.register(category,categoryAdmin)
admin.site.register(product,productAdmin)
admin.site.register(articals,articalsAdmin)



