# dialogflow_bot

С помощью этого бота можно вести несложные диалоги и отвечать на вопросы пользователей. В качестве движка используется Dialogflow от Google.
Демонастрация работы:

![](telegram_small.gif) ![](vk_small.gif)

Можете попробовать пообщаться с ботом сами:
[Telegram](https://t.me/dialog348_bot), 
[сообщество VK](https://vk.com/club191375658)

Предварительная подготовка

Для работы ботов нужно будет создать проект на платформе Google Cloud Platform и зарегистрировать сервисный ключ. При выпуске ключа нужно выбрать JSON формат. После скачивания файла, к нему нужно указать путь в переменной окружения ```GOOGLE_APPLICATION_CREDENTIALS``` Пошаговая инструкция находится [здесь](https://cloud.google.com/dialogflow/docs/quick/api) в разделе "Set up your GCP project and authentication".

Кроме того, нужно будет создать агента в консоли Dialogflow. Пошаговая инструкция на [этой](https://cloud.google.com/dialogflow/docs/quick/api) странице в разделе "Create an agent". После создания агента, нужно будет зайти в его настройки, найти идентификатор проекта и записать в переменную окружения ```PROJECT_ID```.

Для работы скрипта нужно зарегистрировать в операционной системе переменные окружения:

```TG_TOKEN``` - токен бота в телеграме

 ```VK_TOKEN``` - токен доступа к группе Вконтакте. 

 ```GOOGLE_APPLICATION_CREDENTIALS``` - путь к json файлу с ключами к google.cloud

 ```PROJECT_ID``` - идентификатор проекта в Dialogflow

Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```pip install -r requirements.txt```

Для обучения бота нужно подготовить специально структурированый файл json. Пример такого файла:
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
```
После подготовки файла нужно запустить программу и в качестве аргумента указать имя файла. Например:
```python training.py questions.json```
