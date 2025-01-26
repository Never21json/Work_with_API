from flask import Flask, render_template, request
import requests
from datetime import datetime


app = Flask(__name__)

API_KEY = 'DEMO_KEY'
BASE_URL = "https://api.nasa.gov/planetary/apod"

@app.route("/", methods=["GET", "POST"])
def index():
    # Змінні для зберігання URL зображення і дати
    image_url = None
    date = None

    # Перевіряємо, чи це POST запит (тобто користувач надіслав форму)
    if request.method == "POST":
        # Отримуємо введену користувачем дату з форми
        date = request.form["date"]
        
        # Спробуємо перевірити, чи дата в правильному форматі
        try:
            # Перетворюємо рядок дати в об'єкт datetime, щоб перевірити її правильність
            datetime.strptime(date, "%Y-%m-%d") 
            
            # Якщо дата правильна, робимо запит до NASA API
            response = requests.get(BASE_URL, params={"api_key": API_KEY, "date": date})

            # Якщо запит успішний (статус код 200), отримуємо дані з API
            if response.status_code == 200:
                data = response.json()  # Перетворюємо відповідь в формат JSON
                image_url = data.get("url")  # Отримуємо URL зображення з відповіді
            else:
                # Якщо статус код не 200, картинка не буде відображена
                image_url = None
        except ValueError:
            # Якщо формат дати неправильний, присвоюємо None
            image_url = None

    return render_template("index.html", image_url=image_url, date=date)

if __name__ == "__main__":
    app.run(debug=True)

