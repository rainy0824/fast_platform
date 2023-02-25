# 项目说明
> 采用python3+fastapi+vue2.x搭建的后台管理系统，集成swagger,后台模板采用vue-admin-template

***
### 功能
- [x] 系统管理（用户、角色、菜单、权限）
- [x] http在线测试 代码调试
- [x] 项目管理、模块管理、环境管理、接口用例管理
- [ ] 测试套件管理、定时任务
- [ ] mock服务、 测试报告、集成Httprunner
****
#### 后台服务注意事项
    修改 config中db.py中的数据库连接地址
    使用alemic 来配置sqlalchemy,修改alembic.ini中的地址
####运行
    cd backend
    pip install -r requirements.txt
    python main.py

