from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    else:
        unread_notifications_count = 0
    
    return {
        'unread_notifications_count': unread_notifications_count
    } 