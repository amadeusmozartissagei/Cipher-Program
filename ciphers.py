import numpy as np  # Pastikan numpy diimpor

def vigenere_cipher(text, key, mode):
    result = ""
    key_length = len(key)
    key_as_int = [ord(i) - ord('A') for i in key.upper() if i.isalpha()]  # Hanya ambil huruf
    text_as_int = [ord(i) - ord('A') for i in text.upper() if i.isalpha()]  # Hanya ambil huruf

    key_index = 0  # Indeks untuk kunci
    for i in range(len(text_as_int)):
        if mode == 'encrypt':
            value = (text_as_int[i] + key_as_int[key_index % key_length]) % 26
            result += chr(value + ord('A'))  # Kembalikan ke huruf
            key_index += 1  # Hanya increment jika karakter valid
        elif mode == 'decrypt':
            value = (text_as_int[i] - key_as_int[key_index % key_length]) % 26
            result += chr(value + ord('A'))  # Kembalikan ke huruf
            key_index += 1  # Hanya increment jika karakter valid

    return result

def playfair_cipher(text, key, mode):
    def create_matrix(key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key = ''.join(sorted(set(key), key=key.index))
        key += ''.join(filter(lambda x: x not in key, alphabet))
        return [key[i:i + 5] for i in range(0, 25, 5)]

    def find_position(char, matrix):
        for i, row in enumerate(matrix):
            if char in row:
                return (i, row.index(char))
        return None

    def encrypt_pair(a, b, matrix):
        pos_a = find_position(a, matrix)
        pos_b = find_position(b, matrix)

        if pos_a is None or pos_b is None:
            raise ValueError(f"Karakter '{a if pos_a is None else b}' tidak ditemukan dalam matriks.")

        row_a, col_a = pos_a
        row_b, col_b = pos_b

        if row_a == row_b:
            return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            return matrix[row_a][col_b] + matrix[row_b][col_a]

    def decrypt_pair(a, b, matrix):
        pos_a = find_position(a, matrix)
        pos_b = find_position(b, matrix)

        if pos_a is None or pos_b is None:
            raise ValueError(f"Karakter '{a if pos_a is None else b}' tidak ditemukan dalam matriks.")

        row_a, col_a = pos_a
        row_b, col_b = pos_b

        if row_a == row_b:
            return matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            return matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            return matrix[row_a][col_b] + matrix[row_b][col_a]

    text = text.replace("J", "I").upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"

    matrix = create_matrix(key)
    result = ""

    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if mode == 'encrypt':
            result += encrypt_pair(a, b, matrix)
        else:
            result += decrypt_pair(a, b, matrix)

    return result

def hill_cipher(text, key, mode):
    def matrix_mod_inv(matrix, mod):
        det = int(np.round(np.linalg.det(matrix))) % mod
        if det == 0 or np.gcd(det, mod) != 1:
            raise ValueError("Matriks kunci tidak dapat di-inversi untuk modulus yang diberikan.")
        det_inv = pow(det, -1, mod)
        matrix_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % mod
        return matrix_inv

    def encrypt(text, key_matrix):
        text_vector = [ord(char) - 65 for char in text]
        text_vector = np.array(text_vector).reshape(-1, len(key_matrix))
        encrypted_vector = np.dot(text_vector, key_matrix) % 26
        return ''.join(chr(num + 65) for num in encrypted_vector.flatten())

    def decrypt(text, key_matrix):
        key_matrix_inv = matrix_mod_inv(key_matrix, 26)
        text_vector = [ord(char) - 65 for char in text]
        text_vector = np.array(text_vector).reshape(-1, len(key_matrix))
        decrypted_vector = np.dot(text_vector, key_matrix_inv) % 26
        return ''.join(chr(num + 65) for num in decrypted_vector.flatten())

    try:
        # Memecah input kunci menjadi matriks
        key_matrix = np.array([[int(num) for num in row.split()] for row in key.strip().splitlines()])
    except ValueError:
        return "Kunci harus berupa angka yang valid."

    # Memastikan matriks kunci berbentuk persegi
    if key_matrix.shape[0] != key_matrix.shape[1]:
        return "Matriks kunci harus berbentuk persegi."

    # Memastikan determinan tidak nol dan dapat di-inversi
    if np.linalg.det(key_matrix) == 0 or np.gcd(int(np.round(np.linalg.det(key_matrix))), 26) != 1:
        return "Matriks kunci tidak dapat di-inversi untuk modulus yang diberikan."

    # Memastikan panjang teks kelipatan dari ukuran matriks kunci
    if len(text) % len(key_matrix) != 0:
        return "Panjang teks harus kelipatan dari ukuran matriks kunci."

    if mode == 'encrypt':
        return encrypt(text, key_matrix)
    elif mode == 'decrypt':
        return decrypt(text, key_matrix)
