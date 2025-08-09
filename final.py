from kivy.app import App
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture

class ColorPickerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image(source='image.jpg')
        self.label = Label(text='Tap on image to get HEX color')
        self.layout.add_widget(self.img)
        self.layout.add_widget(self.label)
        self.img.bind(on_touch_down=self.on_touch)
        self.texture = CoreImage('image.jpg').texture
        return self.layout

    def on_touch(self, instance, touch):
        if self.img.collide_point(*touch.pos):
            x, y = int(touch.x - self.img.pos[0]), int(touch.y - self.img.pos[1])
            # flip y because Kivy origin is bottom-left for textures
            y = self.img.height - y
            if 0 <= x < self.texture.width and 0 <= y < self.texture.height:
                pixel = self.texture.get_region(x, y, 1, 1).pixels
                r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3]
                hex_color = '#{:02X}{:02X}{:02X}'.format(r, g, b)
                self.label.text = f'HEX: {hex_color}'

if __name__ == '__main__':
    ColorPickerApp().run()
