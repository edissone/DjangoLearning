from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['publish_date']}),
    ]
    list_display = ('question_text', 'publish_date', 'was_published_recently')
    inlines = [ChoiceInline]
    list_filter = ['publish_date']
    search_fields = ['question_text']
    list_per_page = 10

admin.site.register(Question, QuestionAdmin)