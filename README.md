# Kafka-Проект 

## Описание проекта
Настройка кластера Kafka и реализация продюсера с двумя консьюмерами

## Технологии

- Python
- Kafka
- FastApi
- Vue3
- Vite
- Docker
- Nginx

## Запуск проекта

- клонируйте репозиторий на локальную машину и перейдите в созданную папку:

''' git clone git@github.com:son13425/kafka-project.git'''

- установите Docker (Зайдите на официальный сайт https://www.docker.com/products/docker-desktop и скачайте установочный файл Docker Desktop для вашей операционной системы)

- проверьте, что Docker работает:

'''sudo systemctl status docker'''

- создайте файлы /infra/.env.kafka, /backend/.env.backend, /frontend/.env.frontend по шаблонам

- выполните команду в директории /infra:

'''sudo docker-compose up -d --build'''

- приложение разворачивается локально и становится доступным по адресам:

  - http://localhost - фронт приложения для запуска/остановки передачи сообщений в Kafka;

  - http://localhost/api/openapi# - API сервера приложения;

  - http://localhost/kafka-ui/ui/clusters/kraft-cluster/ - UI-кафка;


## Автор
[Оксана Широкова](https://github.com/son13425)

## Лицензия
Сценарии и документация в этом проекте выпущены под лицензией [MIT](https://github.com/son13425/kafka-project/blob/main/LICENSE)
