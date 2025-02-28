from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

import yt_dlp
from yt_dlp import YoutubeDL
import os
import threading

Window.size = (600, 400)  
Window.resizable = False 




KV = """
Screen:
    FloatLayout:
        # Imagen de fondo
        Image:
            source: 'Image/Link.png'
            allow_stretch: True
            keep_ratio: False

        MDBoxLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.27}
            spacing: "20dp"
            
            FloatLayout:
                MDBoxLayout:
                    orientation: 'horizontal'
                    pos:120,170

                    MDBoxLayout:
                        orientation: "horizontal"
                        pos_hint: {"center_x": 1, "center_y": 0.8}
                        
                        MDCheckbox:
                            group: "format"
                            active: True
                            size_hint: None, None
                            size: "30dp", "53dp"
                            color_active: '#EB8E9B'
                            id: mp4
                            
                            

                        MDLabel:
                            text: "MP4"
                            theme_text_color: "Primary"
                            size_hint: None, None  # Fija el tamaño del texto
                            id: mp4_checkbox
                            size: "100dp", "48dp"
                            font_name: "Font/Lovelo.otf"
                            color:'gray'
                            font_size: 12

                    MDBoxLayout:
                        orientation: "horizontal"
                        pos_hint: {"center_x": 1, "center_y": 0.8}
                            
                        MDCheckbox:
                            group: "format"
                            active: True
                            size_hint: None, None
                            size: "30dp", "53dp"
                            color_active: '#EB8E9B'
                            id: mp3
                            
                            

                        MDLabel:
                            text: "MP3"
                            theme_text_color: "Primary"
                            size_hint: None, None 
                            size: "100dp", "48dp"
                            font_name: "Font/Lovelo.otf"
                            color:'gray'
                            font_size: 12

            FloatLayout:
                MDTextField:
                    hint_text: "Link"
                    pos: 60,150
                    size_hint: 0.8, None
                    mode: "round"
                    text_color_focus:'gray'
                    line_color_normal: 'gray'
                    icon_right:"download"
                    line_color_focus:"#3f637e"
                    color_focus:"black"
                    icon_right_color_focus: "#3f637e"
                    id: link
                    
                    
                    
            FloatLayout:
                MDRoundFlatButton:
                    text: 'DOWNLOAD'
                    font_size: 16
                    size_hint: 0.25, None
                    md_bg_color: "#EB8E9B"
                    font_name: "Font/Friday_Sunytime.otf"
                    pos_hint: {"center_x": 0.5, "center_y": 1.1}
                    on_press: app.descargar()  
                    text_color: "white"
                    line_color: 0, 0, 0, 0
                
                    
                    

            FloatLayout:
                MDProgressBar:
                    pos: 60,33
                    size_hint: 0.8, None
                    size:0, 12
                    id: progress_bar
                    value: 0
                    animation: True
                    color:"#6ED1DE"
                    

            
        FloatLayout:
            MDIconButton:
                pos:540,350
                icon: "folder-download"
                icon_size: "25sp"
                theme_icon_color: "Custom"
                icon_color:"#3f637e"
                on_press: app.galeria()
        
        FloatLayout:
            MDIconButton:
                pos:540,310
                icon: "cog-refresh-outline"
                icon_size: "25sp"
                theme_icon_color: "Custom"
                icon_color:"#3f637e"
                on_press: app.galeria()


"""

class MyApp(MDApp):
    def build(self):
        self.icon = "Image/icono.png"
        self.title = "Youtuby"
        Clock.schedule_interval(self.enforce_window_size, 0.1)
        return Builder.load_string(KV)

    def descargar(self):
        self.root.ids.progress_bar.value = 0

        if self.root.ids.mp4.active:
            url = self.root.ids.link.text
            threading.Thread(target=self.descargar_video, args=(url, self.root.ids.progress_bar), daemon=True).start()
            print("mp4")
        elif self.root.ids.mp3.active:
            url = self.root.ids.link.text
            threading.Thread(target=self.youtube_to_mp3, args=(url, self.root.ids.progress_bar), daemon=True).start()
            print("mp3")
        else:
            self.show_error_dialog("Seleccione una de las opciones: MP4/MP3.")

    def enforce_window_size(self, dt):
        """Forzar el tamaño de la ventana en cada frame."""
        if Window.size != (600, 400):
            Window.size = (600, 400)
    
    def show_error_dialog(self, message):
    # Programamos la apertura del diálogo en el hilo principal
        Clock.schedule_once(lambda dt: self._show_dialog(message))

    def _show_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", md_bg_color="#ff616b", font_name="Font/Lovelo.otf", on_release=lambda x: self.close_dialog())],
        )
        self.dialog = dialog
        dialog.open()

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss()
    
    def youtube_to_mp3(self, video_url, progress_bar):
        if not video_url:
            self.show_error_dialog("Por favor, ingresa una URL válida.")
            return
        
        output_folder = "Descargas/Mp3"
        try:
            progress_bar.value = 0  
            os.makedirs(output_folder, exist_ok=True)
            print("Descargando audio del video...")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
                'progress_hooks': [lambda d: self.mostrar_progreso(d, progress_bar)],  # Conectar la barra de progreso
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print("Descarga completada y convertida a MP3.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            self.show_error_dialog("Por favor, ingresa una URL válida.")

    def descargar_video(self, url, progress_bar):
        if not url:
            # Si la URL no es válida, mostramos el diálogo de error en el hilo principal
            self.show_error_dialog("Por favor, ingresa una URL válida.")
            return

        output_folder = "Descargas/Mp4"
        try:
            progress_bar.value = 0  
            os.makedirs(output_folder, exist_ok=True)

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  
                'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  
                'noplaylist': True,  
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4', 
                }],
                'quiet': False,  
                'merge_output_format': 'mp4',  
                'progress_hooks': [lambda d: self.mostrar_progreso(d, progress_bar)],  
            }

            # Descargar el video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Descargando video...")
                ydl.download([url])

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            self.show_error_dialog("Por favor, ingresa una URL válida.")

    def mostrar_progreso(self, d, progress_bar):
        if d['status'] == 'downloading':
            # Calcular el porcentaje y actualizar el valor de la barra
            porcentaje = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            # Usar Clock para actualizar la barra en el hilo principal
            Clock.schedule_once(lambda dt: setattr(progress_bar, 'value', porcentaje))
        elif d['status'] == 'finished':
            print("¡Descarga completa!")
            # Asegurarse de que la barra llegue al 100%
            Clock.schedule_once(lambda dt: setattr(progress_bar, 'value', 100))

    def galeria(self):
        os.startfile(r"Descargas")

MyApp().run()
