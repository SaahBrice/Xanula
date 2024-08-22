from .models import ExplanationRequest

def notification_count(request):
    if request.user.is_authenticated:
        count = ExplanationRequest.objects.filter(user=request.user, status='pending').count()
        return {'notification_count': count}
    return {'notification_count': 0}


from .models import Notification

def general_notification_count(request):
    if request.user.is_authenticated and not request.user.is_staff:
        count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count() + Notification.objects.filter(
            is_global=True, 
            is_read=False
        ).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}