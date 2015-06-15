### 

> 使用 [virtualenv](https://virtualenv.pypa.io/en/latest/) 可以更好的管理各个项目的第三方库

`virtualenv env` ==> `. env/bin/activate`

`pip install -r pip_requirements.txt`

run rqworker: `python myrqworker.py`



用`python manager.py`来执行命令, 输入这个命令后会出现帮助.

REST API是用 flask-peewee 生成, 具体可以看*web/controllers/api*文件. 具体文档可以看[这里](http://flask-peewee.readthedocs.org/en/latest/rest-api.html)

搜索*inspiration*是用 [whoosh](https://pythonhosted.org/Whoosh/index.html) 来做的, whoosh schema 的定义在*web/model/whoose_schema*里面.

原先 whoosh 的 index 是存在文件系统的, 我修改了别人的 Redis-Storage 的实现, 具体实现再*web/util/whoose_redis_storage*

同时再*web/util/__init__*有个 whoosh index_writer 的小函数.

中文分词是使用 jieba 的.

用了很简单的消息队列模块: [python-rq](http://python-rq.org/)


## 文件组织结构
```
.
├── deploy_config  ------ not used in this project
├── fall           ------ not used in this project
├── tools          ------ not used in this project
├── unittests      ------ not used in this project, 
│                  ------ but you could write some unittest here by 'nosetest'
└── web            ------ contain main code 
    ├── admin
    ├── blueprints
    ├── config
    ├── controllers  -- search_api define /search /and-search
    ├── libs
    ├── model -- define models
    ├── static
    └── util  -- lru, whoose redis storage
```








