import pdfkit
import os
import sys
import platform
import requests
from datetime import datetime

def download_html(url, temp_html_file):
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Некорректный URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка загрузки HTML: {response.status_code}")
    with open(temp_html_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"HTML файл загружен: {temp_html_file}")

def convert_html_to_pdf(html_file, output_pdf):
    try:
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        pdfkit.from_file(html_file, output_pdf, configuration=config)
        print(f"PDF создан: {output_pdf}")
    except OSError as e:
        print(f"Ошибка при создании PDF: {e}")

def delete_temp_html(temp_html_file):
    # Удаляем временный PDF
    os.remove(temp_html_file)
    print(f"Временный HTML файл удален: {temp_html_file}")

def open_pdf(output_pdf):
    # Открытие PDF в стандартной программе
    system = platform.system()
    if system == "Windows":
        os.startfile(output_pdf)
    elif system == "Linux":
        os.system(f"xdg-open {output_pdf}")
    else:
        print("Не поддерживаемая операционная система")

if __name__ == "__main__":
    html_file = sys.argv[1] # URL HTML
    temp_html_file = "temp_report.html" # Временный HTML файл

    name = "ShiftReport" #Имя отчета
    current_date = datetime.now().strftime("%Y-%m-%d") #Дата
    system = platform.system()
    # Путь для сохранения PDF файла
    if system == "Windows":
        save_path = r"C:\dll"
    elif system == "Linux":
        save_path = r"/opt/Docsheet"
    os.makedirs(save_path, exist_ok=True)
    output_pdf = os.path.join(save_path, f"{name}_{current_date}.pdf")

    download_html(html_file, temp_html_file)
    convert_html_to_pdf(temp_html_file, output_pdf)
    open_pdf(output_pdf)
    delete_temp_html(temp_html_file)
