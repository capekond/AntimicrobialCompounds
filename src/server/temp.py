from nicegui import ui
from src.server.config import *
import web_part as web

# h0 = [{'name': 'id', 'label': 'Id', 'field': 'id', 'required': True, 'sortable': True, 'align': 'right'},
#       {'name': 'value', 'label': 'Value', 'field': 'value', 'required': True, 'sortable': True, 'align': 'right'},
#       {'name': 'status', 'label': 'Status', 'field': 'status', 'required': True, 'sortable': True, 'align': 'left'}]
# r0 = [{'id': 516, 'value': 15.0, 'status': 'ACTIVE'}, {'id': 517, 'value': 15.0, 'status': 'ACTIVE'},
#       {'id': 518, 'value': 15.0, 'status': 'ACTIVE'}, {'id': 519, 'value': 15.0, 'status': 'ACTIVE'},
#       {'id': 520, 'value': 212.0, 'status': 'ACTIVE'}, {'id': 521, 'value': 212.0, 'status': 'ACTIVE'}]
# h1 = [{'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'sortable': True, 'align': 'left'},
#       {'name': 'role', 'label': 'Role', 'field': 'role', 'required': True, 'sortable': True, 'align': 'left'}]
# r1 = [{'name': 'admin', 'role': 'admin'}, {'name': 'franta', 'role': 'user'}, {'name': 'josef', 'role': 'user'}]
#
# h2 = [{'name': 'id', 'label': 'Name', 'field': 'name', 'required': True, 'sortable': True, 'align': 'left'},
#       {'name': 'role', 'label': 'Role', 'field': 'role', 'required': True, 'sortable': True, 'align': 'left'}]
# r2 = [{'id': 'admin', 'role': 'admin'}, {'id': 'franta', 'role': 'user'}, {'id': 'josef', 'role': 'user'}]
#
# # columns = h0
# # rows = r0
#
# columns = h2
# rows = r2
#
# tbl = ui.table(columns=columns, rows=rows, selection='multiple' if True else None,
#                pagination=TBL_ROW_COUNT,
#                on_select=lambda e: web.add_status(e.selection, []))
# ui.input(placeholder="Add filter value").bind_value_to(tbl, 'filter')
#
# ui.run()
#
# s = ['a', 'b', 'c']
# s0 = ['a','g']
#
# print(     bool((set(s0)).intersection(set(s)))    )
#
# ss = [{'id': 'boban', 'role': 'user'}, {'id': 'chose', 'role': 'user'}]
# print(  set([list(s.values())[0]  for s in ss])    )
#
# s = ['aa', "bb", "cc"]
# print("','".join(s))
#
# selection = [{'id': 'ondrej', 'role': 'admin'}, {'id': 'josef', 'role': 'user'}]
# web.selected_ids = selection
# print(web.get_ids())

s={"a"}
print(list(s)[0])