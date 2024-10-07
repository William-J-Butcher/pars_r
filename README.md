# Установка (Linux)
___

### 1. Пошаговое руководство по установке Docker на Ubuntu.

<details>
<summary>Чтобы получить более подробную информацию об установке, нажмите здесь.</summary>

### Шаг 1: Обновление
Сначала обновите существующий список пакетов, чтобы убедиться, что вы загружаете последние версии.

```
$ sudo apt-get update
```
### Шаг 2: Установка зависимостей
Установите необходимые пакеты, чтобы разрешить apt использовать репозитории по HTTPS:
```commandline
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```
### Шаг 3: Добавьте GPG-ключ Docker
Добавьте официальный ключ GPG Docker, чтобы ваша система доверяла репозиторию Docker:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
### Шаг 4: Добавьте репозиторий Docker
Добавьте репозиторий Docker APT в список источников Ubuntu:
```commandline
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
### Шаг 5: Повторное обновление базы данных пакетов.
Обновите базу данных пакетов, добавив в нее пакеты Docker из недавно добавленного репозитория:
```commandline
sudo apt update
```
### Шаг 6: Установка Docker
Теперь установите Docker:
```commandline
sudo apt install docker-ce docker-ce-cli containerd.io
```
### Шаг 7: Проверка установки Docker
После установки проверьте правильность работы Docker, проверив версию:
```commandline
sudo docker --version
```
</details>

### 2. Клонирование репозитория на сервер

```
https://github.com/William-J-Butcher/pars_r.git
```
### 3. Собрать docker image из Dockerfile

```
$ docker build -t parser .
```
### 4. Запуск контейнера   
```
$ docker run -it --rm -v /home:/data parser
```

### 6. Настройка планировщика задач Cron
<details>
<summary>Чтобы получить более подробную информацию о настройке, нажмите здесь.</summary>
Шаг 1: Откройте Crontab
Чтобы отредактировать задания cron для текущего пользователя, откройте файл конфигурации crontab:
```
$ crontab -e
```
Шаг 2: Добавьте задания cron
В файле crontab добавьте следующую строку, чтобы запланировать запуск команды Docker каждые два дня в определенное время (например, в 00:00 ночи):
```
0 0 */2 * * docker run -it --rm -v /home:/data parser
```
Объяснение:
0 0– Задание будет выполнено в полночь (00:00).
*/2– Задание будет выполняться каждые 2 дня .
* *– Это позволяет поддерживать работу каждый месяц и каждый день недели.
Остальное — ваша команда Docker.
Шаг 3: Сохраните и выйдите
После добавления задания cron сохраните файл и выйдите из редактора. Например, в nano вы нажмете CTRL + O, чтобы сохранить, и , CTRL + Xчтобы выйти.

Шаг 4: Проверьте задание Cron
Чтобы подтвердить добавление задания cron, выполните следующую команду:
```commandline
crontab -l
```
Это должно отобразить задания cron для текущего пользователя, включая то, которое вы только что добавили.

Теперь команда Docker будет автоматически запускаться каждые 2 дня.

</details>