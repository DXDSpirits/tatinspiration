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

## supervisord.ini

```
[program:boring]
command=/root/workspace/tatinspiration/env/bin/gunicorn -b 127.0.0.1:9988 web.app:app
directory=/root/workspace/tatinspiration
user=root
autostart=true
autorestart=true
;redirect_stderr=true
;stdout_logfile=/root/workspace/tatinspiration/boring.log
;stdout_logfile_maxbytes=0
;stderr_logfile=/root/workspace/tatinspiration/boring_error.log


[program:boring-worker]
; Point the command to the specific rqworker command you want to run.
; If you use virtualenv, be sure to point it to
; /path/to/virtualenv/bin/rqworker
; Also, you probably want to include a settings module to configure this
; worker.  For more info on that, see http://python-rq.org/docs/workers/
command=/root/workspace/tatinspiration/env/bin/python /root/workspace/tatinspiration/myrqworker.py
process_name=%(program_name)s

; If you want to run more than one worker instance, increase this
numprocs=1

; This is the directory from which RQ is ran. Be sure to point this to the
; directory where your source code is importable from
directory=/root/workspace/tatinspiration

; RQ requires the TERM signal to perform a warm shutdown. If RQ does not die
; within 10 seconds, supervisor will forcefully kill it
stopsignal=TERM

; These are up to you
autostart=true
autorestart=true

;[program:compose]
;command=/root/workspace/tatcompose/bin/www
;directory=/root/workspace/tatcompose
;user=root
;autostart=true
;autorestart=true
```
