import qrcode
from PIL import Image


def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
       # error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='green', back_color='yellow')
    img.save(filename)
    print(f"QR-код успешно сохранён как {filename}")


if __name__ == "__main__":
    data = input("Введите данные для QR-кода: ")
    filename = input("Введите имя файла для сохранения QR-кода (например, qrcode.png): ")
    generate_qr_code(data, filename)

    # Показываем изображение
    img = Image.open(filename)
    img.show()