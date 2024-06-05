import random
import string
import numpy as np
import os


def generate_sequences(surname, group_number, sequence_length=20, student_number=8):
    sequences = []

    # Послідовність 1: Випадкова бінарна послідовність з певною кількістю '1'
    seq1 = ['1'] * student_number + ['0'] * (sequence_length - student_number)
    random.shuffle(seq1)
    sequences.append(seq1)

    # Послідовність 2: Прізвище, доповнене '0'
    seq2 = list(surname) + ['0'] * (sequence_length - len(surname))
    seq2 = seq2[:sequence_length]
    sequences.append(seq2)

    # Послідовність 3: Випадкова послідовність з букв прізвища та '0'
    alphabet = list(surname) + ['0']
    seq3 = [random.choice(alphabet) for _ in range(sequence_length)]
    sequences.append(seq3)

    # Послідовність 4: Чергування прізвища та номеру групи
    alphabet_4 = list(surname) + list(str(group_number))
    seq4 = []
    for i in range(sequence_length):
        seq4.append(alphabet_4[i % len(alphabet_4)])
    sequences.append(seq4)

    # Послідовність 5: Випадкова послідовність з перших двох букв прізвища та номеру групи, P=0.2
    alphabet_5 = list(surname[:2]) + list(str(group_number))
    seq5 = np.random.choice(alphabet_5, sequence_length, p=[0.2] * len(alphabet_5))
    sequences.append(seq5.tolist())

    # Послідовність 6: Випадкова послідовність з перших двох букв прізвища та номеру групи, P(letters)=0.7, P(numbers)=0.3
    letters = list(surname[:2])
    numbers = list(str(group_number))
    alphabet_6 = letters + numbers
    seq6 = np.random.choice(alphabet_6, sequence_length, p=[0.35, 0.35, 0.1, 0.1, 0.1])
    sequences.append(seq6.tolist())

    # Послідовність 7: Випадкова послідовність з англійських букв та цифр
    alphabet_7 = list(string.ascii_letters + string.digits)
    seq7 = [random.choice(alphabet_7) for _ in range(sequence_length)]
    sequences.append(seq7)

    # Послідовність 8: Послідовність з одиниць
    seq8 = ['1'] * sequence_length
    sequences.append(seq8)

    return sequences


def calculate_characteristics(sequence):
    length = len(sequence)
    alphabet = set(sequence)
    alphabet_size = len(alphabet)
    probabilities = {char: sequence.count(char) / length for char in alphabet}
    avg_probability = sum(probabilities.values()) / alphabet_size
    entropy = -sum(p * np.log2(p) for p in probabilities.values())
    redundancy = 1 - entropy / np.log2(alphabet_size) if alphabet_size > 1 else 0

    return {
        "length": length,
        "alphabet_size": alphabet_size,
        "probabilities": probabilities,
        "avg_probability": avg_probability,
        "entropy": entropy,
        "redundancy": redundancy
    }


def convert_to_bits(sequence, bits_per_symbol=16):
    bit_sequence = ''.join(format(ord(char), '016b') for char in sequence)
    return bit_sequence


def parity_check_encoding(bit_sequence, block_size=3):
    blocks = [bit_sequence[i:i + block_size * 16] for i in range(0, len(bit_sequence), block_size * 16)]
    encoded_blocks = []
    for block in blocks:
        parity_bits = '0' if block.count('1') % 2 == 0 else '1'
        encoded_blocks.append(block + parity_bits)
    return ''.join(encoded_blocks)


def iterative_encoding(bit_sequence, block_size=9):
    blocks = [bit_sequence[i:i + block_size * 16] for i in range(0, len(bit_sequence), block_size * 16)]
    return ''.join(block for block in blocks)


def add_errors(bit_sequence, error_rate=12):
    bit_list = list(bit_sequence)
    for i in range(0, len(bit_sequence), error_rate):
        if i < len(bit_list):
            bit_list[i] = '0' if bit_list[i] == '1' else '1'
    return ''.join(bit_list)


def main():
    surname = "Назаров"
    group_number = 529
    sequences = generate_sequences(surname, group_number)

    with open('result.txt', 'w', encoding='utf-8') as f:
        for idx, seq in enumerate(sequences, 1):
            f.write(f"------------------------------------Послідовність {idx}----------------------------------\n")
            f.write(f"Оригінальна послідовність: {''.join(seq)}\n")

            characteristics = calculate_characteristics(seq)
            f.write(f"Розмір послідовності: {characteristics['length']}\n")
            f.write(f"Розмір алфавіту: {characteristics['alphabet_size']}\n")
            f.write(f"Ймовірність появи символів: {characteristics['probabilities']}\n")
            f.write(f"Середнє арифметичне ймовірності: {characteristics['avg_probability']}\n")
            f.write(f"Ентропія: {characteristics['entropy']}\n")
            f.write(f"Надмірність джерела: {characteristics['redundancy']}\n")

            bit_sequence = convert_to_bits(seq)
            f.write(f"Оригінальна послідовність у бінарному вигляді: {bit_sequence}\n")
            f.write(f"Розмір послідовності у бінарному вигляді: {len(bit_sequence)}\n")

            # Кодування з перевіркою на парність
            parity_encoded = parity_check_encoding(bit_sequence)
            f.write(f"--------------------Кодування з перевіркою на парність-----------------------\n")
            f.write(f"Закодовані дані: {parity_encoded}\n")

            # Додавання помилок
            parity_encoded_with_errors = add_errors(parity_encoded)
            f.write(f"Бінарна послідовність з внесеними помилками: {parity_encoded_with_errors}\n")

            # Ітеративне кодування
            iterative_encoded = iterative_encoding(bit_sequence)
            f.write(f"--------------------Кодування ітеративним кодом-----------------------\n")
            f.write(f"Закодовані дані: {iterative_encoded}\n")

            # Додавання помилок
            iterative_encoded_with_errors = add_errors(iterative_encoded)
            f.write(f"Бінарна послідовність з внесеними помилками: {iterative_encoded_with_errors}\n")



if __name__ == "__main__":
    main()
