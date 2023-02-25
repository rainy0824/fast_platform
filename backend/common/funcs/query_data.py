# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # author： sunxuan
# # datetime： 2022/6/16 20:01
# # ide： PyCharm
#
# from sqlalchemy.sql import or_, func
# from  models.model_base import Base
# ##获取查询参数
# def filter_data(db,model_obj:Base,filterdata=None,,**kwargs):
#     if filterdata:
#         totals = db.query(func.count(Server.server_id)).filter(
#             or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
#             or_(Server.server_ip == filterdata.server_ip, filterdata.server_ip == None)
#         ).scalar()
#         servers = db.query(Server).filter(
#             or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
#             # or_(Server.server_name == filterdata.server_name, filterdata.server_name == None),
#             ).slice(pages.pagesize * (pages.pageno - 1), pages.pagesize * pages.pageno)
#     else:
#         totals = db.query(func.count(Server.server_id)).scalar()
#         servers = db.query(Server).slice(pages.pagesize *(pages.pageno-1),pages.pagesize*pages.pageno)
