## 这是Akari的爱特工作室程序部第二周作业（9th Nov.）

## 菜菜，捞捞，打高分

## 运行

```bash
git clone https://github.com/AkariShorz/ITStudioWork_Week2.git
cd ITStudioWork_Week2

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata activities/fixtures/demo_activities.json
python manage.py runserver
```

## 测试

在项目根目录运行：

```bash
python manage.py test activities
```
