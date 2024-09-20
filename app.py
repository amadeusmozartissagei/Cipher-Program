from flask import Flask, render_template, request
from ciphers import vigenere_cipher, playfair_cipher, hill_cipher
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    error_message = ''
    text = ''
    language = 'en'  # Bahasa default adalah Inggris

    if request.method == 'POST':
        key = request.form['key']
        cipher_type = request.form['cipher_type']
        mode = request.form['mode']
        language = request.form.get('language', 'en')  # Ambil pilihan bahasa dari form

        # Pesan kesalahan dan teks antarmuka dalam bahasa Inggris dan Indonesia
        messages = {
            'en': {
                'key_length_error': "Key must be at least 12 characters long.",
                'file_format_error': "File must be in .txt format.",
                'empty_text_error': "Text cannot be empty.",
                'hill_key_error': "Key for Hill Cipher must be valid numbers.",
                'hill_key_size_error': "Key for Hill Cipher must have 4 (2x2) or 9 (3x3) numbers.",
                'processing_error': "An error occurred: {}",
                'cipher_program': "Cipher Program",
                'enter_text': "Enter text here...",
                'enter_key': "Enter key...",
                'process': "Process",
                'result': "Result:"
            },
            'id': {
                'key_length_error': "Kunci harus minimal 12 karakter.",
                'file_format_error': "File harus berformat .txt.",
                'empty_text_error': "Teks tidak boleh kosong.",
                'hill_key_error': "Kunci untuk Hill Cipher harus berupa angka yang valid.",
                'hill_key_size_error': "Kunci untuk Hill Cipher harus memiliki 4 (2x2) atau 9 (3x3) angka.",
                'processing_error': "Terjadi kesalahan: {}",
                'cipher_program': "Program Cipher",
                'enter_text': "Masukkan teks di sini...",
                'enter_key': "Masukkan kunci...",
                'process': "Proses",
                'result': "Hasil:"
            }
        }

        if len(key) < 12:
            error_message = messages[language]['key_length_error']
        elif 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if file and file.filename.endswith('.txt'):
                text = file.read().decode('utf-8')
            else:
                error_message = messages[language]['file_format_error']
        else:
            text = request.form['text']

        if not text:
            error_message = messages[language]['empty_text_error']

        if cipher_type == 'Hill':
            if not re.match(r'^[\d\s]+$', key):
                error_message = messages[language]['hill_key_error']
            else:
                key_elements = list(map(int, key.split()))
                if len(key_elements) not in [4, 9]:  # 2x2 atau 3x3
                    error_message = messages[language]['hill_key_size_error']

        if not error_message:  # Jika tidak ada kesalahan, lanjutkan
            try:
                if cipher_type == 'Vigenere':
                    result = vigenere_cipher(text, key, mode)
                elif cipher_type == 'Playfair':
                    result = playfair_cipher(text, key, mode)
                elif cipher_type == 'Hill':
                    text_hill = text.replace(" ", "").upper()
                    result = hill_cipher(text_hill, key, mode)
            except Exception as e:
                error_message = messages[language]['processing_error'].format(str(e))

        return render_template('index.html', result=result, error_message=error_message, language=language, messages=messages[language])

    return render_template('index.html', result=result, error_message=error_message, language=language, messages=messages[language])

if __name__ == '__main__':
    app.run(debug=True)
