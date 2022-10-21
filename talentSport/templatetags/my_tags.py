from django import template
from talentSport.models import Notification

register = template.Library()


@register.inclusion_tag('talentSport/notification_mobile.html', takes_context=True)
def notif(context):
	request_user = context['request'].user
	notification = Notification.objects.filter(destinataire=request_user).exclude(est_vu=True).order_by('-date_envoi')
	return {'notification':notification}