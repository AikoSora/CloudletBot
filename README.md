# Cloudlet Bot VK

Cloudlet Bot - [группа вк](https://vk.com/cloudletbot)<br />
Личный проект созданный на полном энтузиазме, использует CloudletEngine
<br />
`Python 3.7+` и выше
<br />
настройка - vkbot/settings.py
<br />
запуск - python3 manage.py startbot
<br />

[Warning]
Из-за отключения от PSQL и перехода на SQLite для демонстрации работоспособности
может потребоватся миграция

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```