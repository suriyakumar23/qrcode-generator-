import qrcode
from io import BytesIO
from base64 import b64encode
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    base64_img = None
    if request.method == 'POST':
        # Get the URL entered by the user
        data = request.form.get('link')  # Get the URL entered by the user
        
        if not data:
            return render_template('index.html', error="Please enter a valid URL.")

        # Generate the QR code for the entered URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code to an in-memory buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert the image to a Base64 string to display on the frontend
        base64_img = "data:image/png;base64," + b64encode(buffer.getvalue()).decode('ascii')

    # Render the template and pass the Base64-encoded image
    return render_template('index.html', data=base64_img)

if __name__ == '__main__':
    app.run(debug=True)
