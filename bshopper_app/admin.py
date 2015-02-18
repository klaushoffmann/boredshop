from django.contrib import admin
from models import UserPreferences, Categories
from django_facebook.models import FacebookCustomUser
from models import ScrapedItems

class ScrapedItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'title', 'description', 'manufacturer', 'scraped_category', 'color' )
    search_fields = ('manufacturer', 'title', 'description')
    filter_fields = ('manufacturer',)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('CatId', 'Category_name', 'Category_name_hier', 'Gender')
    search_fields = ('Category_name',)
    filter_fields = ('Category_name',)

admin.site.register(UserPreferences)
admin.site.register(FacebookCustomUser)
admin.site.register(ScrapedItems, ScrapedItemsAdmin)
admin.site.register(Categories, CategoriesAdmin)
#admin.site.register(ScrapedItems)
