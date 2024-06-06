# 在线银行信用卡子系统-CreditcardSystem

官方操作手册：https://docs.djangoproject.com/zh-hans/5.0/intro/tutorial01

- `CreditcardSystem/settings.py` 系统设置 中 将`DATABASES[  ]` 中改成内容自己数据库的信息

## creditcard 目录

1. 编辑 models.py 文件，改变模型。
2. 运行 `python manage.py makemigrations` 为模型的改变生成迁移文件。
3. 运行 `python manage.py migrate` 数据库根据迁移文件更改表

- `creditcard/urls.py` 配置路由 

    目前所有 creditcard 中的内容都放到了 /api, 详见`CreditcardSystem/urls.py`

- `models` 定义数据库表，存放了我们所需要的表的定义（部分不全因为一些参数没有用到
- `admin`没有用到（可忽略）
- `views` 定义后端函数方法
- `urls` 配置路由，给后端不同函数配置不同地址以便检查

## 运行方式

### 启动后端 

`python manage.py runserver` 或者是 `python3 manage.py runserver` 

访问写好的内容只需要在浏览器中访问配置好的路由，问号后面是需要的参数，例如:
`http://127.0.0.1:8000/api/show_month_bill?account_in_id=1&year=2024&month=5`
界面上出现数据库内容即连接成功

### 启动前端

先进到目录，安装依赖
```
cd frontend
npm install
```
启动前端

运行`npm run dev`

**有关前端部署详见/frontend/README.md**
