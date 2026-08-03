def generate_matrix(key):
    key = key.upper().replace("J", "I")

    matrix = []
    used = set()

    # Add key letters
    for ch in key:
        if ch.isalpha() and ch not in used:
            used.add(ch)
            matrix.append(ch)

    # Add remaining alphabet
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":   # J omitted
        if ch not in used:
            used.add(ch)
            matrix.append(ch)

    # Convert to 5x5 matrix
    playfair = []
    index = 0
    for i in range(5):
        row = []
        for j in range(5):
            row.append(matrix[index])
            index += 1
        playfair.append(row)

    return playfair


def print_matrix(matrix):
    print("\nPlayfair Matrix:")
    for row in matrix:
        print(" ".join(row))


def prepare_text(text):
    text = text.upper().replace(" ", "").replace("J", "I")

    prepared = ""
    i = 0

    while i < len(text):
        first = text[i]

        if i + 1 < len(text):
            second = text[i + 1]

            if first == second:
                prepared += first + "X"
                i += 1
            else:
                prepared += first + second
                i += 2
        else:
            prepared += first + "X"
            i += 1

    return prepared


def find_position(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j


def playfair_encrypt(text, matrix):
    ciphertext = ""

    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]

        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        # Same row
        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5]
            ciphertext += matrix[r2][(c2 + 1) % 5]

        # Same column
        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1]
            ciphertext += matrix[(r2 + 1) % 5][c2]

        # Rectangle
        else:
            ciphertext += matrix[r1][c2]
            ciphertext += matrix[r2][c1]

    return ciphertext


# Main
key = input("Enter the key: ")
plaintext = input("Enter the message: ")

matrix = generate_matrix(key)
print_matrix(matrix)

prepared = prepare_text(plaintext)
print("\nPrepared Plaintext:", prepared)

cipher = playfair_encrypt(prepared, matrix)

print("Ciphertext:", cipher)