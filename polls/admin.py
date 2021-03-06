from django.contrib import admin

from .models import Question, Choice, Comment


# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice

    def votes_count(self, obj):
        return obj.votes.count()

    votes_count.short_description = 'Votes count'

class CommentInline(admin.StackedInline):
    model = Comment

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'description', 'author', 'image', 'choice_type']}),
        ('Date information', {'fields': ['publish_date']}),
    ]
    list_display = ('question_text', 'publish_date', 'was_published_recently', 'author')
    inlines = [ChoiceInline]
    list_filter = ['publish_date']
    search_fields = ['question_text']
    list_per_page = 10


admin.site.register(Question, QuestionAdmin)
