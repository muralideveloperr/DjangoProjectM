from django.contrib import admin
from .models import About, AddBook, ExpenseCategory, ExpensesTracker, JobBoard, JobType, ManageLibraryCard, Services, Resume, ChatbotRules

# Register your models here.

class projectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(About, projectAdmin)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'icon_color')

admin.site.register(Services, ServicesAdmin)

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'email', 'phone')

admin.site.register(Resume, ResumeAdmin)

class ChatbotRulesAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'response')

admin.site.register(ChatbotRules, ChatbotRulesAdmin)

class ManageLibraryCardAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'name', 'email', 'phone', 'issued_date')

admin.site.register(ManageLibraryCard, ManageLibraryCardAdmin)

class AddBookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'published_date', 'category', 'borrowed', 'borrowed_by', 'borrowed_date', 'return_date')

admin.site.register(AddBook, AddBookAdmin)

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)

class ExpensesTrackerAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'category')

admin.site.register(ExpensesTracker, ExpensesTrackerAdmin)

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('job_type',)

admin.site.register(JobType, JobTypeAdmin)