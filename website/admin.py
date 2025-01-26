from django.contrib import admin
from .models import MenuCategory, MenuItem, GalleryItem, WebsiteContent


# Inline class to display MenuItem directly under MenuCategory in the admin panel
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # Number of empty rows to show by default


class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display category name
    search_fields = ('name',)  # Enable searching by category name
    inlines = [MenuItemInline]  # Show related MenuItem in a tabular inline


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)  # Display item name, category, and price
    search_fields = ('name', 'category__name')  # Enable searching by item name and category name


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)


from .models import AboutUs, Chef


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'story_title', 'video_title']


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']


class WebsiteContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'address', 'phone_number', 'email')
    search_fields = ('name', 'tagline', 'address')


admin.site.register(WebsiteContent, WebsiteContentAdmin)

# Register the models with their respective admins
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
