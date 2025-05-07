import heapq
from collections import defaultdict
import os
import tkinter as tk
from tkinter import filedialog

# ==================== Huffman Coding Utilities ====================

def build_frequency_table(text):
    return defaultdict(int, {char: text.count(char) for char in set(text)})

def build_huffman_tree(frequency):
    heap = [[freq, [char, ""]] for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        low1 = heapq.heappop(heap)
        low2 = heapq.heappop(heap)

        for pair in low1[1:]:
            pair[1] = '0' + pair[1]
        for pair in low2[1:]:
            pair[1] = '1' + pair[1]

        heapq.heappush(heap, [low1[0] + low2[0]] + low1[1:] + low2[1:])
    return heapq.heappop(heap)[1:] if heap else []

def generate_huffman_codes(tree_data):
    huff_codes = {char: code for char, code in tree_data}
    reverse_codes = {code: char for char, code in tree_data}
    return huff_codes, reverse_codes

def encode_text(text, huff_codes):
    return ''.join(huff_codes[char] for char in text)

def decode_text(encoded_text, reverse_codes):
    current_code = ""
    decoded = []
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded.append(reverse_codes[current_code])
            current_code = ""
    return ''.join(decoded)

def binary_string_to_bytes(binary_string):
    padding = (8 - len(binary_string) % 8) % 8
    binary_string = '0' * padding + binary_string
    byte_array = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    return byte_array, padding

def bytes_to_binary_string(byte_array, padding=0):
    binary_string = ''.join(f'{byte:08b}' for byte in byte_array)
    return binary_string[padding:] if padding else binary_string

def save_compressed_data(encoded_bytes, filename="compressed.bin"):
    save_path = os.path.join(os.getcwd(), filename)
    with open(save_path, "wb") as file:
        file.write(encoded_bytes)
    print(f"Compressed data saved to: {save_path}")

def load_text_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def load_binary_file(path):
    with open(path, "rb") as file:
        return file.read()

# ==================== GUI-Compatible Utility ====================

def load_file_into_box(target_box):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            target_box.delete("1.0", tk.END)
            target_box.insert(tk.INSERT, text)