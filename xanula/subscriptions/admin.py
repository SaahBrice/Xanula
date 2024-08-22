from django.utils import timezone
from django.contrib import admin
from .models import SubscriptionPlan, Subscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'price')
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'is_valid')
    list_filter = ('is_active', 'plan')
    search_fields = ('user__username', 'user__email', 'plan__name')
    date_hierarchy = 'start_date'

    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True
    is_valid.short_description = 'Currently Valid'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'plan')
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('user', 'plan', 'start_date')
        return ()

    def save_model(self, request, obj, form, change):
        if not change:  # creating a new object
            obj.save()  # This will set the end_date based on the plan's duration
        super().save_model(request, obj, form, change)
    actions = ['extend_subscription']

    def extend_subscription(self, request, queryset):
        for subscription in queryset:
            if subscription.is_active:
                subscription.end_date += timezone.timedelta(days=subscription.plan.duration_days)
                subscription.save()
    extend_subscription.short_description = "Extend selected subscriptions"