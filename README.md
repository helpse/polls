POLLS
=====

# INSTALL

```
$ git clone git@gitlab.com:helpse/polls.git
$ cd polls

$ virtualenv venv -p /usr/bin/python3 (linux)
$ . venv/bin/activate (linux)

$ virtualenv venv -p /c/Python35/python3.exe (windows)
$ . venv/Scripts/activate (windows)

$ pip3 install -r requirements.txt
$ mysql -uroot -e"create database polls"
$ chmod 774 manage.py (linux)
$ ./manage.py migrate
```

# ERROR
```
_mysql.c(29): fatal error C1083: Cannot open include file: 'my_config.h': No such file or directory
error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\BIN\\cl.exe' failed with exit status 2
```

https://github.com/PyMySQL/mysqlclient-python/issues/54

FIX:
`$ pip3 install whl/mysqlclient-1.3.9-cp35-cp35m-win32.whl`

# RUN
`$ ./manage.py runserver`
