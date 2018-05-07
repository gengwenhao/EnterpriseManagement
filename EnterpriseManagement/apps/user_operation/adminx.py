import xadmin
from user_operation.models import Board
from xadmin import views


class BoardAdmin:
    list_display = ['user', 'content', 'type', 'target_id', 'add_time']


xadmin.site.register(Board, BoardAdmin)
