from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.core import urlresolvers
from django.template.loader import render_to_string
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import urls
from .models import Reminder


class ReminderWarningPanel(object):
    name = 'pages_for_moderation'
    order = 200

    def __init__(self, request):
        self.request = request
        try:
            self.reminders = Reminder.objects.filter(sent=True, page_reviewed=False, user=request.user)

        except Reminder.DoesNotExist:
            pass

    def render(self):
        if self.reminders:
            return render_to_string('wagtailrelevancy/panel_warnings.html', {
                'reminders': self.reminders,
                'request': self.request,
            })
        else:
            return None


@hooks.register('construct_homepage_panels')
def reminder_warnings(request, panels):
    reminder_panels = ReminderWarningPanel(request)
    if reminder_panels.reminders:
        panels.append(reminder_panels)


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^relevancy/', include(urls)),
    ]


@hooks.register('register_settings_menu_item')
def register_menu_settings():
    return MenuItem(
        'Relevancy',
        urlresolvers.reverse('wagtailrelevancy'),
        classnames='icon icon-doc-full',
        order=250
    )
