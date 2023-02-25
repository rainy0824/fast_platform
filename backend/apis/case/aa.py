# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 23:32
# @Author  : sunxuan
# @Site    : 
# @File    : aa.py

def qq(func_str, func_name,**kwargs):
    try:
        namespace = {}
        exec(func_str,namespace)
        # print(f'namespace:{namespace}')
        ret = namespace.get(func_name)(**kwargs)
        print("ret", ret)
        return {'code':200,'data':ret}
    except Exception as e:
         return f'调试出错:{e}'
func_str = """
def vv():
    all_data = [
            {'seed-url': 'https://rf.eefocus.com/', 'list-url': 'https://rf.eefocus.com/article/list-all/sort-new?p={}', 'pages': int(3)},
    ]
    url_list = []
    for data in all_data:
        url = data['list-url']
        pages = data['pages']
        for page in range(1, int(pages)):
            url_list.append(url.format(page))
    return url_list
"""
aa= """
def aa():
    return 5
def vv(x,y):
    s=aa()
    z=s+x+y
    return z
"""

# qq(func_str, 'vv')

qq(func_str=aa,func_name='vv',x=5,y=2)