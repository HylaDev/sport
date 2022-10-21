from django import template
from talentSport.models import Notification

register = template.Library()

@register.inclusion_tag('talentSport/notification.html', takes_context=True)
def notification(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(destinataire=request_user).exclude(est_vu=True).order_by('-date_envoi')
	return {'notifications':notifications}
