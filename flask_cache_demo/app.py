from flask import Flask
from flask import render_template
from flask_cache import Cache  # 引入缓存的拓展
# 同时需要修改源码的一个导入配置，
# 具体查看：flask中缓存cache导入时引发的错误 - https://www.cnblogs.com/gavinclc/p/9622095.html
# import redis

app = Flask(__name__)
# Check Configuring Flask-Cache section for more details

# 本地存储
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# 存储到redis
cache = Cache(app, config={'CACHE_TYPE': 'redis',          # Use Redis
                           'CACHE_REDIS_HOST': '127.0.0.1',  # Host, default 'localhost'
                           'CACHE_REDIS_PORT': 6379,       # Port, default 6379
                           # 'CACHE_REDIS_PASSWORD': 'test123',  # Password
                           # [Redis]ResponseError: Client sent AUTH, but no password is set
                           # 如果报上面这行错，可以先把密码配置注释
                           'CACHE_REDIS_DB': 0})          # DB, default 0


@app.route('/')
@cache.cached(timeout=50)
def index():
    """
    逻辑
    0. 完成如该视图函数所示的配置
    1. 测试对print(12341234)的缓存
        效果：在首次访问的50秒内，只有第一次会打印12341234，后面50秒内在访问该路径的视图函数都不会打印
    2. 测试对模板页面index.html的缓存
        效果：对模板页面的缓存配置也是50秒(模板页面的具体配置查看header.html,footer.html,及index.html页面)
        测试结果：页面大小为300kb，首次访问耗时180ms左右，再通过ctrl+r强制刷新页面，访问页面耗时20-50ms之间，
        结论：明显对模板页面的缓存产生效果
        总结：1. 应该将{% cache 50, 'temp_index' %}{% endcache %}放在{% block blockContent %}{% endblock %}内部
              2. 模板缓存的名字不要重名,或者 干脆不命名（当然，这不利于清除缓存）
    :return:
    """
    print('12341234')
    return render_template('index.html', data="这是一个缓存测试12", temp_name='temp_index')


@app.route('/test')
def test():
    return render_template('test.html', data="这是一个test的一个缓存测试12", temp_name='temp_test')


# 测试对普通函数的缓存
@cache.memoize(timeout=50)
def create_list(num):
    print('method create_list called')
    l = []
    for i in range(num):
        l.append(str(i))
    return l


@app.route('/list/<int:num>')
def list(num):
    return ', '.join(create_list(num))


if __name__ == '__main__':
    app.run(debug=True)

