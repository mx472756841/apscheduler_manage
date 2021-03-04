# 说明

```
这里是Flask-Admin==1.5.7版本自带的翻译文件，为方便复用，直接复用中文翻译

Flask-Admin本地化处理方式是在babel.py中自定义了CustomDomain，创建了一个domain为admin,初始目录为flask_admin的domain，后续在.html以及.py都是使用domain.gettext方式获取翻译内容

所以我们的扩展方式时，对于flask-admin中的翻译保留，同时将需要的拿过来，然后对于我们需要翻译的内容再进行处理，最后通过pybabel命令编译到domain为admin的mo文件中
```

# 扩展步骤

## 在初始化flask-admin时，指定domain的目录为此目录

    Admin()

## 对于我们新增的代码中进行编译内容处理
### 扩展前置条件

    安装Flasl-Babelex

### 扩展步骤
- 代码中引用gettext，解压出pot文件

    pybabel extract -F babel.cfg -k _gettext -o temp/message.pot app/

    **-k 指定关键字，对于用这个关键字的东西需要翻译，可能使用的方式不同，会有区别**

- 填写翻译文件

    我这里只有中文翻译，所以我只需要一个文件，并且填写中文翻译就可以了

- 生成/更新po文件

    pybabel init -l zh_Hans_CN -D login -d app/translations -i temp/message.pot

    pybabel update -- 如果是更新文件的话，走这个

- 编译到mo文件

    pybabel compile -D admin -l zh_Hans_CN -d app/translations -i app/translations/zh_Hans_CN/LC_MESSAGES/login.po

    **用-D admin，是因为flask-admin中用到的翻译customedomain都是admin,就是找的是admin.mo，所以我们要编译到这个里面**

## 资料
[flask-babelex参考资料](https://pythonhosted.org/Flask-Babel/#translating-applications)
```
1、新建babel.cfg:
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
2、生成编译模板
pybabel extract -F babel.cfg -o messages.pot .
3、翻译
pybabel init -i messages.pot -d app/translations -l zh_Hans_CN -D admin
4、手动输入中文
messages.mo
5、编译翻译结果
pybabel compile -d app/translations -l zh_Hans_CN -D admin
6、更新翻译
pybabel update -i messages.pot -d translations
```