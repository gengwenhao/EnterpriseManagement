# 企业管理系统后台代码设计

> 北软2015届, 软件专业毕业设计, 耿文浩

## Run Project

``` shell
# install pipenv
pip install pipenv

# install dependencies
cd EnterpriseManagement
pipenv install

# migrate database
python3 manage.py migrate

# run project
python3 manage.py runserver [port or address: port]
```

