import xadmin
from orgs.models import OrgProfile


class OrgProfileAdmin(object):
    pass


xadmin.site.register(OrgProfile, OrgProfileAdmin)
