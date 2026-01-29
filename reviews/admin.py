from django.contrib import admin
from .models import Application, AppReview, Feedback


# -------------------------------------------------
# Inline Reviews (Shown inside Application Admin)
# -------------------------------------------------
class AppReviewInline(admin.TabularInline):
    model = AppReview
    extra = 0
    can_delete = False
    readonly_fields = (
        'user',
        'comment',
        'sentiment',
        'sentiment_score',
        'review_status',
        'ip_address',
        'created_at',
    )
    fields = (
        'user',
        'comment',
        'sentiment',
        'sentiment_score',
        'review_status',
        'ip_address',
        'created_at',
    )


# -------------------------------------------------
# Application Admin
# -------------------------------------------------
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'is_fraud',
        'created_at',
    )

    list_filter = (
        'category',
        'is_fraud',
        'created_at',
    )

    search_fields = (
        'name',
        'category',
        'description',
    )

    readonly_fields = (
        'created_at',
    )

    inlines = [AppReviewInline]

    ordering = ('-created_at',)


# -------------------------------------------------
# AppReview Admin (Moderation Panel)
# -------------------------------------------------
@admin.register(AppReview)
class AppReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'app',
        'user',
        'review_status',
        'sentiment',
        'sentiment_score',
        'ip_address',
        'created_at',
    )

    list_filter = (
        'review_status',
        'sentiment',
        'created_at',
    )

    search_fields = (
        'app__name',
        'user__username',
        'comment',
        'ip_address',
    )

    readonly_fields = (
        'created_at',
        'sentiment',
        'sentiment_score',
        'ip_address',
    )

    list_editable = (
        'review_status',
    )

    ordering = ('-created_at',)


# -------------------------------------------------
# Feedback Admin
# -------------------------------------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
    )

    search_fields = (
        'user__username',
        'message',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = ('-created_at',)
