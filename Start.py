# 1.验证登录
# 2.根据不同登录用户获取对应缓存信息
#   a.检查用户数据是否存在,不存在则初始化
#   b.解析用户数据
# 3.渲染主页面
import __init__
import auth
import main


authenticator, name, status, username = auth.auth()
if status:
    main.engine()
