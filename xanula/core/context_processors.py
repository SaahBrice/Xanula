from .models import ExplanationRequest

def notification_count(request):
    if request.user.is_authenticated:
        count = ExplanationRequest.objects.filter(user=request.user, status='pending').count()
        return {'notification_count': count}
    return {'notification_count': 0}