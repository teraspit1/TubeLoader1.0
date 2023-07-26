from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from pytube import YouTube
import os


class TubeLoaderApp(App):
    def select_folder(self, instance):
        """Выбрать папку для сохранения"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup = Popup(title='Выберите папку', content=content, size_hint=(None, None), size=(300, 200))
        folder_path = TextInput(multiline=False, size_hint=(None, None), width=200)
        content.add_widget(folder_path)

        def browse_folder(instance):
            self.output_entry.text = folder_path.text
            popup.dismiss()

        browse_button = Button(text='Обзор', size_hint=(None, None), width=100)
        browse_button.bind(on_press=browse_folder)
        content.add_widget(browse_button)

        popup.open()

    def download_video(self, instance):
        """Загрузить видео"""
        url = self.url_entry.text
        output_folder = self.output_entry.text

        if url and output_folder:
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()  # Выбираем наилучшее доступное разрешение
                video.download(output_folder)
                popup = Popup(title='Успех', content=Label(text='Видео успешно загружено'), size_hint=(None, None),
                              size=(150, 100))
                popup.open()
            except Exception as e:
                popup = Popup(title='Ошибка', content=Label(text=str(e)), size_hint=(None, None), size=(300, 150))
                popup.open()
        else:
            popup = Popup(title='Ошибка', content=Label(text='Введите ссылку и выберите папку для сохранения'),
                          size_hint=(None, None), size=(300, 150))
            popup.open()

    def show_video_stats(self, instance):
        """Показать статистику видео"""
        url = self.url_entry.text

        if url:
            try:
                yt = YouTube(url)
                stats = f"Название: {yt.title}\n" \
                        f"Автор: {yt.author}\n" \
                        f"Просмотры: {yt.views}\n" \
                        f"Рейтинг: {yt.rating}\n" \
                        f"Длительность: {yt.length} секунд\n" \
                        f"Описание: {yt.description}"
                popup = Popup(title='Статистика видео', content=Label(text=stats), size_hint=(None, None),
                              size=(400, 300))
                popup.open()
            except Exception as e:
                popup = Popup(title='Ошибка', content=Label(text=str(e)), size_hint=(None, None), size=(300, 150))
                popup.open()
        else:
            popup = Popup(title='Ошибка', content=Label(text='Введите ссылку на видео'), size_hint=(None, None),
                          size=(300, 150))
            popup.open()

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(None, None), size=(300, 400),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

        url_label = Label(text="Ссылка на видео:", size_hint=(None, None), height=30)
        layout.add_widget(url_label)

        self.url_entry = TextInput(hint_text="Введите ссылку на видео", size_hint=(1, None), height=30)
        layout.add_widget(self.url_entry)

        output_label = Label(text="Путь сохранения:", size_hint=(None, None), height=30)
        layout.add_widget(output_label)

        self.output_entry = TextInput(hint_text="Выберите папку для сохранения", size_hint=(1, None), height=30)
        layout.add_widget(self.output_entry)

        browse_button = Button(text="Обзор", size_hint=(1, None), height=30)
        browse_button.bind(on_press=self.select_folder)
        layout.add_widget(browse_button)

        download_button = Button(text="Загрузить", size_hint=(1, None), height=30)
        download_button.bind(on_press=self.download_video)
        layout.add_widget(download_button)

        stats_button = Button(text="Статистика", size_hint=(1, None), height=30)
        stats_button.bind(on_press=self.show_video_stats)
        layout.add_widget(stats_button)

        layout.bind(minimum_height=layout.setter('height'))  # Автоматически подстраиваем высоту окна под содержимое

        return layout


if __name__ == '__main__':
    TubeLoaderApp().run()
