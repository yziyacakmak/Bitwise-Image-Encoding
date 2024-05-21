import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import ipywidgets as widgets
from IPython.display import display,Javascript


# Resim yükleme ve gösterme fonksiyonu
def on_file_upload(change, image_widget, label_widget):
    # Yüklenen dosya
    uploaded_file = change["new"][0]
    print(["name"])
    # uploaded_file = list(change.values())[0]
    content = uploaded_file['content']
    filename = uploaded_file['name']  # Dosya adını al

    # Dosya adını etikete yaz
    label_widget.value = f"Seçilen dosya: {filename}"

    # OpenCV ile yüklenen dosyayı okuma
    np_img = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

     # OpenCV görüntüyü BGR formatında yükler, bunu RGB formatına çevirelim
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # OpenCV görüntüsünü PIL görüntüsüne dönüştürelim
    image_pil = Image.fromarray(image_rgb)

    # PIL görüntüsünü bir buffer'a kaydedelim
    buffer = BytesIO()
    image_pil.save(buffer, format='PNG')
    buffer.seek(0)

    image_widget.on_msg(lambda _, content: show_popup(f"data:image/png;base64,{content['data']['data']}"))

    # ipywidgets.Image ile görüntüyü gösterelim
    image_widget.value = buffer.getvalue()    


def on_trackbar_change(change, label_widget):
    label_widget.value = f"2 bit start index: {change['new']}"


    

def show_popup(image_data):
    display(Javascript(f'''
        var img = new Image();
        img.src = "{image_data}";
        var w = window.open("");
        w.document.write(img.outerHTML);
        '''))