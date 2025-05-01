import heapq
import os
from collections import Counter
from bitarray import bitarray
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Huffman Tree Node Class
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
         return self.freq < other.freq

# Select File
def select_file():
    filename = filedialog.askopenfilename(title="Select a text file",
                                            filetypes=[("Text Files", "*.txt")])
    return filename

# Read the Selected File
def read_input_file():
    global input_filename
    nput_filename = select_file()
    if not input_filename:
        messagebox.showwarning("Warning", "No file selected!")
        return None
    with open(input_filename, "r", encoding="utf-8") as file:
        return file.read().strip()

# Build Huffman Tree
def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(freq, char) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    return heap[0]

# Generate Huffman Codes
def generate_codes(node, current_code="", codes={}):
    if node.char:
        codes[node.char] = current_code
        return
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)
    return codes

# Encode Text
def encode(text, codes):
    return ''.join(codes[char] for char in text)

# Save Encoded Data to File
def save_compressed_file(encoded_text):
    with open("compressed.bin", "wb") as file:
        bitarray(encoded_text).tofile(file)
    messagebox.showinfo("Success", "Compressed file saved as 'compressed.bin'.")

# Load Encoded File
def load_compressed_file():
    with open("compressed.bin", "rb") as file:
        binary_data = bitarray()
        binary_data.fromfile(file)
    return binary_data.to01()

# Decode Encoded Text
def decode(encoded_text, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    current_code, decoded_text = "", ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""
    return decoded_text

# Compare File Sizes
def compare_file_sizes():
    original_size = os.path.getsize(input_filename)
    compressed_size = os.path.getsize("compressed.bin")
    compression_ratio = (1 - (compressed_size / original_size)) * 100
    return original_size, compressed_size, compression_ratio

# Function to Handle Compression
def compress():
    global text, huffman_codes
    text = read_input_file()
    if not text:
        return

    # Build Huffman Tree
    huffman_tree_root = build_huffman_tree(text)

    # Generate Huffman Codes
    huffman_codes = generate_codes(huffman_tree_root)

    # Encode the text
    encoded_text = encode(text, huffman_codes)

    # Save compressed file
    save_compressed_file(encoded_text)

    # Display Huffman Codes
    codes_display.delete("1.0", tk.END)
    codes_display.insert(tk.END, "\n".join(f"'{char}': {code}" for char, code in
    huffman_codes.items()))

    # Display Compression Stats
    original_size, compressed_size, compression_ratio = compare_file_sizes()
    compression_info.set(f"Original: {original_size} bytes | Compressed:{compressed_size} bytes | Ratio: {compression_ratio:.2f}%")

# Function to Handle Decompression
def decompress():
    # Load compressed file
    loaded_encoded_text = load_compressed_file()

    # Decode text
    decoded_text = decode(loaded_encoded_text, huffman_codes)

    # Display decoded text
    decoded_text_display.delete("1.0", tk.END)
    decoded_text_display.insert(tk.END, decoded_text)

    # Verify correctness
    if text == decoded_text:
        messagebox.showinfo("Success", "Decoding successful! Original text matches.")
    else:
        messagebox.showerror("Error", "Decoding failed! Original text does not match.")
        
# ---------------- GUI Implementation ----------------
# Create Main Window
root = tk.Tk()
root.title("Huffman Compression Tool")
root.geometry("700x600")
root.configure(bg="#f0f0f0")
# Title Label
title_label = tk.Label(root, text="📦 Huffman Coding Compression Tool",
font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)
# File Selection Button
file_button = tk.Button(root, text="📦 Select Text File", font=("Arial", 12),
command=compress)
file_button.pack(pady=5)
# Compression Stats Label
compression_info = tk.StringVar()
compression_info.set("Compression details will appear here.")
stats_label = tk.Label(root, textvariable=compression_info, font=("Arial", 12),
bg="#f0f0f0", fg="blue")
stats_label.pack(pady=5)
# Huffman Codes Display
codes_label = tk.Label(root, text="📦 Huffman Codes:", font=("Arial", 12, "bold"),
bg="#f0f0f0")
codes_label.pack()
codes_display = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial",
10))
codes_display.pack()
# Decode Button
decode_button = tk.Button(root, text="📦 Decompress File", font=("Arial", 12),
command=decompress)
decode_button.pack(pady=5)
# Decoded Text Display
decoded_label = tk.Label(root, text="📦 Decoded Text:", font=("Arial", 12, "bold"),
bg="#f0f0f0")
decoded_label.pack()
decoded_text_display = scrolledtext.ScrolledText(root, width=50, height=5,
font=("Arial", 10))
decoded_text_display.pack()
# Run the GUI
root.mainloop()
