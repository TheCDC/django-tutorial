from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    # number of blank templates for the associated model to include
    # in the inline display
    # when there are not yet any Choices it will display
    # "Choice #1", "Choice #2", "Choice #3",
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    # class var of fields of model to display in list of data
    list_display = ("question_text", "pub_date", "was_published_recently")
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"], "classes": "collapse"})

    ]
    inlines = [ChoiceInline]
    list_filter = ["pub_date"]


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
