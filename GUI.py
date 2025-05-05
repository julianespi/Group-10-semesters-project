import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import tools.compression as compression

root = tk.Tk()
root.title("CSUF Document Scanner & Pattern Extractor")
root.geometry("1070x670")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("TButton", padding=6, font=('Segoe UI', 10))
style.configure("TLabel", font=('Segoe UI', 10))
style.configure("TCombobox", font=('Segoe UI', 10))
style.configure("TLabelframe.Label", font=('Segoe UI', 11, 'bold'), foreground="#2F2D92")

# Upload
upload_frame = ttk.LabelFrame(root, text="Upload Documents")
upload_frame.pack(fill="x", padx=15, pady=10)

upload_btn1 = ttk.Button(upload_frame, text="Upload Document 1", command=lambda: compression.load_file_into_box(box1))
upload_btn1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

upload_btn2 = ttk.Button(upload_frame, text="Upload Document 2", command=lambda: compression.load_file_into_box(box2))
upload_btn2.grid(row=0, column=2, padx=10, pady=10)

box1 = scrolledtext.ScrolledText(upload_frame, width=60, height=15, font=("Courier", 10))
box1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

box2 = scrolledtext.ScrolledText(upload_frame, width=60, height=15, font=("Courier", 10))
box2.grid(row=1, column=2, padx=10, pady=10)

# Plagiarism Detection
control_frame = ttk.LabelFrame(root, text="Plagiarism Detection")
control_frame.pack(fill="x", padx=15, pady=10)

algorithm_choice = ttk.Combobox(control_frame, values=["Naive", "KMP", "Rabin-Karp"], width=25)
algorithm_choice.set("Choose Matching Algorithm")
algorithm_choice.grid(row=0, column=0, padx=10, pady=10)

run_button = ttk.Button(control_frame, text="Run Plagiarism Check")
run_button.grid(row=0, column=1, padx=10, pady=10)

# Compression
compression_frame = ttk.LabelFrame(root, text="Compression Info")
compression_frame.pack(fill="x", padx=15, pady=10)

def compress_documents():
    for idx, (box, orig_label, comp_label, file_prefix) in enumerate([
        (box1, original_label1, compressed_label1, "doc1"),
        (box2, original_label2, compressed_label2, "doc2")
    ], start=1):
        text = box.get("1.0", tk.END).strip()
        if text:
            frequency = compression.build_frequency_table(text)
            tree = compression.build_huffman_tree(frequency)
            huff_codes, _ = compression.generate_huffman_codes(tree)
            encoded = compression.encode_text(text, huff_codes)
            encoded_bytes, _ = compression.binary_string_to_bytes(encoded)

            compression.save_compressed_data(encoded_bytes, filename=f"{file_prefix}_compressed.bin")

            orig_size = len(text.encode('utf-8'))
            comp_size = len(encoded_bytes)

            orig_label.config(text=f"Document {idx} Original Size: {orig_size} bytes")
            comp_label.config(text=f"Document {idx} Compressed Size: {comp_size} bytes")
        else:
            orig_label.config(text=f"Document {idx} Original Size: -")
            comp_label.config(text=f"Document {idx} Compressed Size: -")

compress_btn = ttk.Button(compression_frame, text="Compress Documents", command=compress_documents)
compress_btn.grid(row=0, column=0, padx=10, pady=10)

# Document 1 Labels
original_label1 = ttk.Label(compression_frame, text="Document 1 Original Size: -")
original_label1.grid(row=0, column=1, padx=10, pady=10)

compressed_label1 = ttk.Label(compression_frame, text="Document 1 Compressed Size: -")
compressed_label1.grid(row=0, column=2, padx=10, pady=10)

# Document 2 Labels
original_label2 = ttk.Label(compression_frame, text="Document 2 Original Size: -")
original_label2.grid(row=1, column=1, padx=10, pady=10)

compressed_label2 = ttk.Label(compression_frame, text="Document 2 Compressed Size: -")
compressed_label2.grid(row=1, column=2, padx=10, pady=10)

# Sorting
sorting_frame = ttk.LabelFrame(root, text="Sort Documents")
sorting_frame.pack(fill="x", padx=15, pady=10)

sort_choice = ttk.Combobox(sorting_frame, values=["Author", "Title", "Date"], width=20)
sort_choice.set("Sort By")
sort_choice.grid(row=0, column=0, padx=10, pady=10)

sort_btn = ttk.Button(sorting_frame, text="Sort")
sort_btn.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
