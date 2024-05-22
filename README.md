# BankSystem

包含两个目录

- BankSystem: 系统的相关设置
- creditcard: 信用卡子模块内容
- frontend: 前端内容

## BankSystem


- `setting` 系统设置 ( 将DATABASES[  ] 中改成内容自己数据库的信息，所有目前的问题是不知道怎么多人同时访问同一个数据库。)
- `urls` 配置路由 ( 目前所有 creditcard 中的内容都放到了 /api)


## creditcard

- `models` 定义数据库表 
- `views` 定义函数方法
- `urls` 配置路由

## 运行方式

### 启动后端 

`python manage.py runserver` 或者是 `python3 manage.py runserver` 

访问写好的内容只需要在浏览器中访问配置好的路由，问号后面是需要的参数，例如:

`http://127.0.0.1:8000/api/pay_to?account_in_id=1&account_out_id=2&amount=1000&date=2024-05-22`
`http://127.0.0.1:8000/api/show_month_bill?year=2024&month=5&account_in_id=1`

### 启动前端

```
cd frontend
npm install
npm run dev
```

*但是现在还没有把前后端链接到一起*
