import tkinter as tk
from tkinter import filedialog, scrolledtext
import heapq
from collections import defaultdict
import os

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

# ==================== GUI Integration ====================

def load_file_into_box(target_box):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            target_box.delete("1.0", tk.END)
            target_box.insert(tk.INSERT, text)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            process_text(content)

def process_text(content):
    frequency = build_frequency_table(content)
    tree = build_huffman_tree(frequency)
    huff_codes, reverse_codes = generate_huffman_codes(tree)

    encoded = encode_text(content, huff_codes)
    encoded_bytes, padding = binary_string_to_bytes(encoded)

    save_compressed_data(encoded_bytes)

    text_area.delete("1.0", tk.END)
    code_list = "\n".join([f"{char}: {code}" for char, code in huff_codes.items()])
    text_area.insert(tk.INSERT, f"Huffman Codes:\n\n{code_list}\n")

    compression_detail.config(
        text=f"Original: {len(content)} bytes | Compressed: {len(encoded_bytes)} bytes | Ratio: {(len(encoded_bytes)/len(content))*100:.2f}%"
    )

def decode_bin_file(reverse_codes=None, padding=0):
    file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
    if file_path:
        with open(file_path, "rb") as file:
            encoded_bytes = file.read()
            binary_string = bytes_to_binary_string(encoded_bytes, padding)

            decoded_text_area.delete("1.0", tk.END)

            if reverse_codes:
                decoded = decode_text(binary_string, reverse_codes)
                decoded_text_area.insert(tk.INSERT, decoded)
            else:
                decoded_text_area.insert(tk.INSERT, "Cannot decode without Huffman map.")

# ==================== UI Setup ====================

root = tk.Tk()
root.title("Huffman Coding Compression")

# Input / output area
text_area = scrolledtext.ScrolledText(root, width=60, height=15)
text_area.pack()

compression_detail = tk.Label(root, text="Compression details will appear here.")
compression_detail.pack()

decoded_text_area = scrolledtext.ScrolledText(root, width=60, height=10)
decoded_text_area.pack()

# Buttons
tk.Button(root, text="Open Text File", command=open_file).pack()
tk.Button(root, text="Decode Binary File", command=decode_bin_file).pack()

root.mainloop()
