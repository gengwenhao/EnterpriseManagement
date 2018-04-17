import xadmin
from xadmin import views
from users.models import VerifyCode, Message


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'EM'
    site_footer = 'EM'
    menu_style = 'accordion'


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile']


class MessageAdmin(object):
    list_display = ['user', 'content']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(Message, MessageAdmin)
