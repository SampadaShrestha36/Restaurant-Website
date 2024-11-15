from django.contrib import admin
from .models import Management
# Register your models here.
@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display=['id','title','price','category','image']