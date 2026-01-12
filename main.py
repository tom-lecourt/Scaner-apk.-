from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
import requests

# Importations pour le scan (gérées par Buildozer lors de l'APK)
from pyzbar import pyzbar
from PIL import Image as PILImage

class QRScannerApp(App):
    def build(self):
        # Organisation de l'interface
        self.layout = BoxLayout(orientation='vertical')

        # 1. Widget Caméra
        # Sur Android, l'index 0 est la caméra arrière
        self.cam = Camera(play=True, resolution=(640, 480))
        self.layout.add_widget(self.cam)

        # 2. Zone de texte pour le statut
        self.label = Label(
            text="Visez un QR Code", 
            size_hint_y=0.2,
            color=(0, 1, 0, 1) # Texte en vert
        )
        self.layout.add_widget(self.label)

        self.dernier_code = ""

        # On analyse l'image toutes les 1.5 secondes pour ne pas surcharger le processeur
        Clock.schedule_interval(self.analyser_frame, 1.5)

        return self.layout

    def analyser_frame(self, dt):
        if self.cam.texture:
            # Récupération des données brutes de la caméra
            pixels = self.cam.texture.pixels
            size = self.cam.texture.size

            # Conversion pour PyZbar via PIL (Pillow)
            pil_image = PILImage.frombytes(mode='RGBA', size=size, data=pixels)
            barcodes = pyzbar.decode(pil_image)

            for barcode in barcodes:
                contenu = barcode.data.decode('utf-8')
                if contenu != self.dernier_code:
                    self.dernier_code = contenu
                    self.notifier_serveur(contenu)

    def notifier_serveur(self, code):
        # Ton adresse mise à jour
        url = "https://xelery.pythonanywhere.com/update"
        try:
            # Envoi du texte du QR code au serveur
            requests.post(url, data={'code': code}, timeout=5)
            self.label.text = f"Envoyé : {code}"
        except:
            self.label.text = "Erreur de connexion (Serveur hors ligne ?)"

if __name__ == '__main__':
    QRScannerApp().run()
