def test_get_menus_tree(datas):
    '''
     items =[
      {"id":1,"name":'部门1',"pid":0},
      {"id":2,"name":'部门2',"pid":1},
      {"id":3,"name":'部门3',"pid":1},
      {"id":4,"name":'部门4',"pid":3},
      {"id":5,"name":'部门5',"pid":4}
     ]
    '''
    lists = []
    tree = {}
    for data in datas:
        tree[data['menu_id']] = data  # 每一列列表转换为字典
    print(f'=----{tree}')
    for data in datas:
        if not data['parent_id']:  # pid 为0则为该条data为根菜单
            root = tree[data['menu_id']]
            lists.append(root)
        else:
            parent_id = data['parent_id']
            if 'children' not in tree[parent_id]:
                tree[parent_id]['children'] = []
            tree[parent_id]['children'].append(tree[data['menu_id']])
    print(lists)
    return lists


def list_to_tree(datas):
    '''

    Args:
        datas (): 格式必须为[{key1:数字,key2:字符,k3:数字},{key1:数字,key2:字符,k3:数字}]
        [
    {"menu_id": 1, "name": '部门1', "parent_id": 0},
    {"menu_id": 2, "name": '部门2', "parent_id": 1},
    {"menu_id": 3, "name": '部门3', "parent_id": 1},
    {"menu_id": 4, "name": '部门4', "parent_id": 3},
    {"menu_id": 5, "name": '部门5', "parent_id": 4}
    ]

    Returns:
    '''
    key1, key2, key3 = datas[0].keys()
    lists = []
    tree = {}
    for data in datas:
        tree[data[key1]] = data  # 每一列列表转换为字典
    print(f'=----{tree}')
    for data in datas:
        if not data[key3]:  # pid 为0则为该条data为根菜单
            root = tree[data[key1]]
            lists.append(root)
        else:
            new_key = data[key3]
            if 'children' not in tree[new_key]:
                tree[new_key]['children'] = []
            tree[new_key]['children'].append(tree[data[key1]])
    print(lists)
    return lists


items = [
    {"menu_id": 1, "name": '部门1', "parent_id": 0},
    {"menu_id": 2, "name": '部门2', "parent_id": 1},
    {"menu_id": 3, "name": '部门3', "parent_id": 1},
    {"menu_id": 4, "name": '部门4', "parent_id": 3},
    {"menu_id": 5, "name": '部门5', "parent_id": 4}
]

if __name__ == '__main__':
    list_to_tree(items)
