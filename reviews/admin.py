from django.contrib import admin

from reviews.models import Review, User

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    list_filter = ['time_created']
    search_fields = ['user', 'title', 'content']

admin.site.register(Review, ReviewAdmin)