from django.contrib import admin
from .models import Application, AppReview, Feedback


# -----------------------------------------
# Inline Reviews (Shown inside Application)
# -----------------------------------------
class AppReviewInline(admin.TabularInline):
    model = AppReview
    extra = 0
    readonly_fields = ('user', 'comment', 'sentiment', 'sentiment_score', 'created_at')


# -----------------------------------------
# Application Admin
# -----------------------------------------
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_fraud', 'created_at')
    list_filter = ('category', 'is_fraud', 'created_at')
    search_fields = ('name', 'category')
    inlines = [AppReviewInline]


# -----------------------------------------
# AppReview Admin
# -----------------------------------------
@admin.register(AppReview)
class AppReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'user', 'sentiment', 'sentiment_score', 'created_at')
    list_filter = ('sentiment', 'created_at')
    search_fields = ('app__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)


# -----------------------------------------
# Feedback Admin
# -----------------------------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)
