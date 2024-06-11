import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import cv2
import os
from inputimeout import inputimeout, TimeoutOccurred
import pyttsx3
import csv
import webbrowser
from datetime import datetime

# Hàm để nghe lệnh từ người dùng
def listen():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            print("Bạn có thể nói điều gì đó...")
            speak("Tôi đang lắng nghe bạn.")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language='vi-VN')
                print(f"Bạn nói: {text}")
                engine.say(text)
                engine.runAndWait()
                return text.lower()
            except sr.UnknownValueError:
                print("Xin lỗi, tôi không hiểu bạn nói gì.")
                speak("Xin lỗi, tôi không hiểu bạn nói gì.")
            except sr.RequestError:
                print("Xin lỗi, không thể kết nối đến dịch vụ nhận diện giọng nói.")
                speak("Xin lỗi, không thể kết nối đến dịch vụ nhận diện giọng nói.")
                return ""

# Hàm để trợ lý ảo nói
def speak(text):
    tts = gTTS(text=text, lang='vi')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Hàm để chụp ảnh từ webcam với tên tệp duy nhất
def capture_image(name):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        filename = f"user_images/{name}.jpg"
        cv2.imwrite(filename, frame)
    cam.release()
    cv2.destroyAllWindows()
    return filename

# Hàm để đọc lại thông tin đã nhập
def read_info(name, email, phone, gender, address):
    print(f"Thông tin của bạn: Tên: {name}, Email: {email}, Số điện thoại: {phone}, Giới tính: {gender}, Địa chỉ: {address}")
    speak(f"Thông tin của bạn: Tên: {name}, Email: {email}, Số điện thoại: {phone}, Giới tính: {gender}, Địa chỉ: {address}")

# Hàm để đăng ký người dùng
def register_user():
    try:
        name = input("Nhập tên: ")
        email = input("Nhập email: ")
        phone = input("Nhập số điện thoại: ")
        gender = input("Nhập giới tính (1: Nam, 2: Nữ, 3: Khác): ")  # Thay vì chọn, nhập giới tính từ danh sách
        gender = map_gender(gender)
        address = input("Nhập địa chỉ: ")
        read_info(name, email, phone, gender, address)
        print("Vui lòng nhìn vào camera để chụp ảnh.")
        speak("Vui lòng nhìn vào camera để chụp ảnh.")
        image_path = capture_image(name)
        print("Đã chụp ảnh thành công.")
        speak("Đã chụp ảnh thành công.")
        if save_user_info(name, email, phone, gender, address, image_path):  # Lưu thông tin người dùng vào file
            print("Đã đăng ký người dùng thành công.")
            speak("Đã đăng ký người dùng thành công.")
        else:
            print("Người dùng đã tồn tại.")
            speak("Người dùng đã tồn tại.")
    except TimeoutOccurred:
        print("Hết thời gian, vui lòng thử lại sau.")
        speak("Hết thời gian, vui lòng thử lại sau.")

# Hàm để chuyển đổi giới tính từ số sang chuỗi tương ứng
def map_gender(gender_input):
    gender_map = {
        '1': 'Nam',
        '2': 'Nữ',
        '3': 'Khác'
    }
    return gender_map.get(gender_input, 'Khác')

# Hàm để lưu thông tin người dùng vào file CSV
def save_user_info(name, email, phone, gender, address, image_path):
    # Kiểm tra xem người dùng đã tồn tại hay chưa
    if not os.path.isfile("user_info.csv"):
        with open("user_info.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Email", "Phone", "Gender", "Address", "Image"])

    with open("user_info.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name:
                return False  # Người dùng đã tồn tại

    with open("user_info.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, phone, gender, address, image_path])
    return True

# Hàm để hiển thị thông tin người dùng từ file CSV
def display_user_info():
    if os.path.isfile("user_info.csv"):
        with open("user_info.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua tiêu đề
            for row in reader:
                print(f"Tên: {row[0]}, Email: {row[1]}, Số điện thoại: {row[2]}, Giới tính: {row[3]}, Địa chỉ: {row[4]}")
                speak(f"Tên: {row[0]}, Email: {row[1]}, Số điện thoại: {row[2]}, Giới tính: {row[3]}, Địa chỉ: {row[4]}")
    else:
        print("Không có thông tin người dùng.")
        speak("Không có thông tin người dùng.")

# Hàm để mở Spotify
def open_spotify():
    print("Đang mở Spotify...")
    speak("Đang mở Spotify...")
    webbrowser.open("https://www.spotify.com")

# Hàm để hiển thị thời gian hiện tại
def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bây giờ là {current_time}")
    speak(f"Bây giờ là {current_time}")

# Hàm để xóa màn hình console
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Hàm chính để xử lý các lệnh
def assistant():
    clear_screen()  # Xóa màn hình console khi bắt đầu
    print("Xin chào bạn, tôi có thể giúp gì cho bạn?")
    speak("Xin chào bạn, tôi có thể giúp gì cho bạn?")
    while True:
        print("\n------ MENU ------")
        print("1. Đăng ký người dùng")
        print("2. Hiển thị thông tin người dùng")
        print("3. Mở Spotify")
        print("4. Mấy giờ rồi")
        print("5. Thoát")
        print("------------------")
        speak("Bạn muốn làm gì?")
        command = listen()
        clear_screen()  # Xóa màn hình console trước khi thoát
        if "một" in command or "đăng ký" in command:
            print("Vui lòng nhập thông tin người dùng")
            speak("Vui lòng nhập thông tin người dùng")
            register_user()
        elif "hai" in command or "hiển thị" in command:
            print("Thông tin người dùng")
            speak("Thông tin người dùng")
            display_user_info()
        elif "ba" in command or "spotify" in command:
            open_spotify()
        elif "bốn" in command or "giờ" in command:
            tell_time()
        elif "năm" in command or "thoát" in command:
            clear_screen()  # Xóa màn hình console trước khi thoát
            print("Tạm biệt! Hẹn gặp lại.")
            speak("Tạm biệt! Hẹn gặp lại.")
            return
        else:
            print("Lệnh không hợp lệ. Vui lòng thử lại.")
            speak("Lệnh không hợp lệ. Vui lòng thử lại.")

# Chạy trợ lý ảo
if __name__ == "__main__":
    if not os.path.exists('user_images'):
        os.makedirs('user_images')
    assistant()
