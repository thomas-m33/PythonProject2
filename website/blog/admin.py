from django.contrib import admin
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_posted")
    list_filter = ("categories", "tags")
    search_fields = ("title", "content", "tags__name", "categories__name")
    filter_horizontal = ("categories",)

admin.site.register(Category)
# Categories are a separate model that admins can add or remove things from. This can also be done in the terminal.
