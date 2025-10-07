from django.contrib import admin
from .models import Contact, PortfolioItem, PortfolioImage

# Register your models here.
# class PortfolioItemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'created_at')
#     list_filter = ('category',)
#     search_fields = ('title', 'description')

admin.site.register(Contact)
# admin.site.register(PortfolioItem, PortfolioItemAdmin)

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1  # Number of empty forms to display
    classes = ('collapse',)
    fields = ('image', 'alt_text')

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    inlines = [PortfolioImageInline]
    list_display = ('title', 'category', 'project_date', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    # Add these fields to control the form display
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Details', {
            'fields': ('client', 'project_date', 'project_url'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(PortfolioImage)