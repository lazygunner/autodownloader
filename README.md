#Autodownloader#

本应用是一款基于Flask & MongoDB的追剧平台，数据爬自人人影视。

##基本功能##

1.查看热播美剧更新

2.定制个人追剧，配合[homedownloader](https://github.com/lazygunner/homedownloader)项目，更新自动下载到家中硬盘，并邮件通知

3.配合[homedownloader](https://github.com/lazygunner/homedownloader)项目，完成在线添加链接地址，家中下载

##环境搭建##

    git clone https://github.com/lazygunner/autodownloader
    virtualenv .
    source bin/active
    pip install -r requirement
    
##配置信息##

本应用使用了flask-security作为登录验证以及邮箱通知模块，相应配置可以参考[flask-security](https://pythonhosted.org/Flask-Security/)相关配置

1.密钥加密算法 & 加盐

    app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'  
    app.config['SECURITY_PASSWORD_SALT'] = 'passwordsalt'
    
2.通知邮箱配置

    app.config['MAIL_SERVER'] = 'smtp.xxx.com'
    app.config['DEFAULT_MAIL_SENDER'] = 'xxx.xxx.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'xxx'
    app.config['MAIL_PASSWORD'] = 'xxx'
    app.config['MAIL_DEBUG'] = False
