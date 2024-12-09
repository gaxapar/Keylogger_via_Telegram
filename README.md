# Скриншоты

### Приложения
<img src="https://github.com/gaxapar/Keylogger_via_Telegram/blob/main/images/Screenshot%20(46).png" width="300" />

### Скриншоты с телефона
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/gaxapar/Keylogger_via_Telegram/blob/main/images/phone_scr1" width="200" />
  <img src="https://github.com/gaxapar/Keylogger_via_Telegram/blob/main/images/phone_scr2" width="200" />
</div>

# Инструкция по установке и использованию

Для того, чтобы собрать и запустить программу, выполните следующие шаги:

## Шаг 1: Установите .NET Framework 4.8.1

Программа требует установленного .NET Framework 4.8.1. Вы можете скачать и установить его с официального сайта:

[Скачать .NET Framework 4.8.1](https://dotnet.microsoft.com/download/dotnet-framework)

## Шаг 2: Установите Python

Если Python ещё не установлен, скачайте и установите его с официального сайта:

[Скачать Python](https://www.python.org/downloads/)

Во время установки убедитесь, что выбрали опцию **Add Python to PATH**.

## Шаг 3: Установите PIP

PIP — это инструмент для установки Python-библиотек. Он обычно устанавливается вместе с Python, но если по какой-то причине его нет, скачайте его отсюда:

[Установить PIP](https://pip.pypa.io/en/stable/installation/)

## Шаг 4: Установите библиотеки

Для работы программы нужно установить несколько Python-библиотек. Создайте виртуальное окружение или используйте вашу систему Python для установки необходимых библиотек.

Скачайте все библиотеки из файла `requirements.txt` с помощью команды:

```bash
pip install -r requirements.txt
```

## Шаг 5: Установите PyInstaller

PyInstaller — это инструмент для упаковки Python-программ в исполнимые файлы (.exe). Для установки PyInstaller выполните команду:

```bash
pip install pyinstaller
```

## Шаг 6: Компиляция EXE файла

После того, как вы установили все необходимые компоненты, вы можете запустить программу. В программе будет поле для ввода **Bot Token** и **User ID**. Введите свой **Bot Token**, который вы получили при создании бота через [BotFather](https://core.telegram.org/bots#botfather), а также **User ID** — это идентификатор пользователя, которому будет предоставлен доступ к боту. Другие пользователи не будут иметь доступ к боту.

После того как вы введете эти данные, нажмите на кнопку **Run**. Программа скомпилирует ваш Python скрипт в EXE файл.

## Шаг 7: Настройте Telegram-бота

Ваш Telegram-бот позволит вам удалённо управлять компьютером. Для этого вам нужно создать собственного бота в Telegram через BotFather.

### Что может делать Telegram-бот:
1. **Управлять мышью**: Двигайте курсор, выполняйте клики.
2. **Использовать телефон как клавиатуру**: Вводите текст прямо с телефона.
3. **Управлять громкостью**: Регулируйте громкость компьютера.
4. **Получать изображения с камеры**: Сделайте фото с подключённой камеры компьютера.
5. **Делать скриншоты**: Снимайте экран и отправляйте изображения в чат.
6. **Записывать нажатия клавиш (keylogger)**: Отслеживайте ввод на клавиатуре.

Для настройки бота, следуйте этим шагам:
1. Откройте [BotFather](https://core.telegram.org/bots#botfather) в Telegram.
2. Создайте нового бота с помощью команды `/newbot`.
3. Скопируйте полученный токен.

Теперь вы готовы к использованию бота.

## Шаг 8: Запустите программу

После выполнения всех вышеописанных шагов, вы сможете запустить вашу программу и скомпилировать Python скрипт в EXE файл. После этого вы сможете загрузить этот EXE файл на целевой компьютер и контролировать его через ваш Telegram-бот.

# Возникли проблемы? Нужна помощь?  
Напишите автору: [https://t.me/psmib](https://t.me/psmib)


