import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import StringVar
from pytube import YouTube
import os
def browse_folder():
    """Открыть диалог выбора папки для сохранения"""
    global folder_path
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)
def download_video():
    """Скачать видео"""
    try:
        video_url = url_entry.get()
        output_path = output_entry.get()
        if not video_url or not output_path:
            messagebox.showerror("Ошибка", "Необходимо указать ссылку на видео и путь сохранения")
            return
        yt = YouTube(video_url)
        if not yt:
            messagebox.showerror("Ошибка", "Видео по данной ссылке не найдено")
            return
        title = yt.title
        filename = "Скачано через TubeLoader TG:t.me/TubeLoaderOfficial" + ".mp4"
        video_exists = False
        for file in os.listdir(output_path):
            if file == filename:
                video_exists = True
                break
        if video_exists:
            messagebox.showwarning("Внимание", f"Видео '{title}' уже существует в указанной папке. Выберите другую папку для сохранения.")
            return
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        status_label.config(text="Загрузка началась...")
        # загрузить видео
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path)
        status_label.config(text="Видео скачано в: " + output_path)
    except Exception as e:
        status_label.config(text="Произошла ошибка: " + str(e))
def update_video_info():
    """Обновить информацию о видео"""
    try:
        video_url = url_entry.get()
        if not video_url:
            messagebox.showerror("Ошибка", "Необходимо указать ссылку на видео")
            return
        yt = YouTube(video_url)
        if not yt:
            messagebox.showerror("Ошибка", "Видео по данной ссылке не найдено")
            return
        title = yt.title
        rating = yt.rating
        title_label.config(text=title)
        rating_label.config(text="Рейтинг: " + str(rating))
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось получить информацию о видео.")
        print(str(e))
root = tk.Tk()
root.title("TubeLoader V1.0")
style = ttk.Style()
style.theme_use('clam')
style.configure('DownloadButton.TButton', font=('Arial', 11, 'bold'), foreground='white', background='#007bff')
style.configure('BrowseButton.TButton', font=('Arial', 11, 'bold'), foreground='white', background='#007bff')
style.configure('UpdateButton.TButton', font=('Arial', 11, 'bold'), foreground='white', background='#007bff')
style.configure('format_combobox', font=('Arial', 11, 'bold'), foreground='white', background='#007bff')# Синий цвет
style.configure('Label.TLabel', font=('Arial', 11, 'bold'), foreground='#007bff')
style.configure('ErrorLabel.TLabel', font=('Arial', 11, 'bold'), foreground='red')
url_label = ttk.Label(root, text="Ссылка на видео:", style='Label.TLabel')
url_label.grid(row=0, sticky="w", pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=1, padx=5, pady=5)
output_label = ttk.Label(root, text="Путь сохранения:", style='Label.TLabel')
output_label.grid(row=2, sticky="w", pady=5)
output_entry = ttk.Entry(root, width=50)
output_entry.grid(row=3, padx=5, pady=5)
browse_button = ttk.Button(root, text="Обзор", style='BrowseButton.TButton', command = browse_folder)
browse_button.grid(row=3, column=1)
download_button = ttk.Button(root, text="Скачать", style='DownloadButton.TButton', command = download_video)
download_button.grid(row=4, columnspan=2, pady=10)
info_frame = tk.Frame(root)
info_frame.grid(row=6, columnspan=2, pady=5)
title_label = ttk.Label(info_frame, text="", font=('Arial', 12, 'bold'), foreground='#007bff')
title_label.pack(side='top')
rating_label = ttk.Label(info_frame, text="", font=('Arial', 11, 'bold'), foreground='#6c757d')
rating_label.pack(side='top')
status_label = ttk.Label(root, text="", font=('Arial', 12, 'bold'), foreground='#007bff')
status_label.grid(row=8, columnspan=2, pady=10)
update_button = ttk.Button(root, text="Обновить информацию", style='UpdateButton.TButton', command = update_video_info)
update_button.grid(row=7, columnspan=2, pady=10)
root.mainloop()
