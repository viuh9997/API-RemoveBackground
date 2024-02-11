from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Bem-vindo à API de processamento de imagens!</h1>
    <p>Para usar esta API, siga as instruções abaixo:</p>
    <ol>
        <li>Faça um POST para /upload com uma imagem anexada.</li>
        <li>A imagem será processada para remover o fundo.</li>
        <li>Você receberá uma resposta JSON contendo a imagem processada.</li>
    </ol>
    """

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'error': 'Arquivo enviado não é uma imagem válida'}), 400

    input_image = Image.open(file)
    output_image = remove(input_image)
    
    buffered = io.BytesIO()
    output_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run()
