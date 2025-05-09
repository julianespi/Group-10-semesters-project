import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import tools.compression as compression
import tools.searchTools as search

# Frame
class CSUFScanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSUF Document Scanner & Pattern Extractor")
        self.geometry("760x720")
        self.configure(bg="#f4f4f4")

        self.frames = {}
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Initialize all frames
        for F in (HomePage, PlagiarismPage, SearchPage, CompressionPage, GraphAnalysisPage, SortingPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="CSUF Document Scanner & Pattern Extractor", font=("Segoe UI", 16, "bold"), foreground="#2F2D92").pack(pady=30)

        for text, frame in [
            ("Plagiarism Checker", PlagiarismPage),
            ("Real-Time Search", SearchPage),
            ("Compression", CompressionPage),
            ("Graph Analysis", GraphAnalysisPage),
            ("Sorting", SortingPage)
        ]:
            ttk.Button(self, text=text, width=30, command=lambda f=frame: controller.show_frame(f), style="Home.TButton").pack(pady=10)
            style = ttk.Style()
            style.configure("Home.TButton", font=("Segoe UI", 12, "bold"), padding=20)


def split_into_phrases(text, window_size=5):
    words = text.split()
    return [' '.join(words[i:i+window_size]) for i in range(len(words) - window_size + 1)]

def show_scrollable_message(title, message):
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry("500x300")
    popup.resizable(False, False)

    ttk.Label(popup, text=title, font=("Segoe UI", 12, "bold")).pack(pady=10)

    text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=60, height=10)
    text_area.pack(padx=10, pady=10)
    text_area.insert(tk.END, message)
    text_area.config(state='disabled')  # make read-only

    ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

class PlagiarismPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Plagiarism Checker", font=("Segoe UI", 14, "bold"), foreground="#2F2D92").pack(pady=10)
        ttk.Button(self, text="← Back to Home", command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10)

        # Upload Section
        upload_frame = ttk.LabelFrame(self, text="Upload Documents")
        upload_frame.pack(fill="x", padx=15, pady=10)

        self.box1 = scrolledtext.ScrolledText(upload_frame, width=40, height=10, font=("Courier", 10))
        self.box1.grid(row=1, column=0, padx=10, pady=10)

        self.box2 = scrolledtext.ScrolledText(upload_frame, width=40, height=10, font=("Courier", 10))
        self.box2.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(upload_frame, text="Upload Main Text", command=lambda: self.load_file_into_box(self.box1)).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(upload_frame, text="Upload Comparison Text", command=lambda: self.load_file_into_box(self.box2)).grid(row=0, column=1, padx=10, pady=10)

        # Algorithm Choice Section
        control_frame = ttk.LabelFrame(self, text="Plagiarism Detection")
        control_frame.pack(fill="x", padx=15, pady=10)

        self.algorithm_choice = ttk.Combobox(control_frame, values=["KMP", "Rabin-Karp"], width=25)
        self.algorithm_choice.set("Choose Matching Algorithm")
        self.algorithm_choice.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(control_frame, text="Run Plagiarism Check", command=self.plagiarism_check).grid(row=0, column=1, padx=10, pady=10)

        # Similarity Percentage Bar Section
        self.similarity_label = ttk.Label(self, text="Similarity: 0%")
        self.similarity_label.pack(pady=10)

        # Canvas to show the similarity bar
        self.similarity_canvas = tk.Canvas(self, width=400, height=40, bg="white")
        self.similarity_canvas.pack(pady=10)

    def plagiarism_check(self):
        text1 = self.box1.get("1.0", tk.END).strip()
        text2 = self.box2.get("1.0", tk.END).strip()

        if not text1 or not text2:
            messagebox.showwarning("Input Missing", "Both documents must be loaded.")
            return

        algo = self.algorithm_choice.get()
        if algo not in ["KMP", "Rabin-Karp"]:
            messagebox.showwarning("Algorithm Missing", "Please select a matching algorithm.")
            return

        # Phrase segmentation (e.g., 5-word phrases)
        phrases = []
        words = text1.split()
        phrase_len = 4

        for i in range(len(words) - phrase_len + 1):
            phrase = " ".join(words[i:i + phrase_len])
            phrases.append(phrase)

        matches = []
        for phrase in phrases:
            if algo == "KMP":
                found = search.kmp_search(text2, phrase)
            else:
                found = search.rabin_karp(text2, phrase)

            if found:
                matches.append((phrase, found))

        total_checked = len(phrases)
        matched_count = len(matches)
        similarity_percent = (matched_count / total_checked) * 100 if total_checked else 0

        # Update the similarity bar and label
        self.update_similarity_bar(similarity_percent)

        # Display plagiarism results
        if matches:
            result_text = "\n\n".join([f"'{p}' found at positions {pos}" for p, pos in matches])
            result_text = f"Similarity: {similarity_percent:.2f}%\n\n" + result_text
            messagebox.showinfo("Plagiarism Detected", f"Matching phrases found:\n\n{result_text}")
        else:
            messagebox.showinfo("No Plagiarism Detected", "No matching phrases found.")

    def load_file_into_box(self, box):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
                box.delete("1.0", tk.END)
                box.insert(tk.END, contents)

    def update_similarity_bar(self, similarity_percent):
        # Update the similarity percentage label
        self.similarity_label.config(text=f"Similarity: {similarity_percent:.2f}%")

        # Scale the similarity percentage to fit the canvas width
        bar_width = similarity_percent * 4  # 100% corresponds to 400px in width

        # Set color based on similarity
        if similarity_percent > 70:
            bar_color = "red"
        elif similarity_percent > 40:
            bar_color = "yellow"
        else:
            bar_color = "green"

        # Clear any previous bars and draw a new one
        self.similarity_canvas.delete("all")
        self.similarity_canvas.create_rectangle(0, 0, bar_width, 40, fill=bar_color)


class CompressionPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        import tools.compression as compression  # Local import to keep it modular
        self.compression = compression

        ttk.Label(self, text="Compression", font=("Segoe UI", 14, "bold"), foreground="#2F2D92").pack(pady=10)
        ttk.Button(self, text="← Back to Home", command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10)

        upload_frame = ttk.LabelFrame(self, text="Upload and Compress")
        upload_frame.pack(fill="x", padx=15, pady=10)

        self.box1 = scrolledtext.ScrolledText(upload_frame, width=40, height=10, font=("Courier", 10))
        self.box1.grid(row=1, column=0, padx=10, pady=10)

        self.box2 = scrolledtext.ScrolledText(upload_frame, width=40, height=10, font=("Courier", 10))
        self.box2.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(upload_frame, text="Upload Main Text", command=lambda: self.load_file_into_box(self.box1)).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(upload_frame, text="Upload Comparison Text", command=lambda: self.load_file_into_box(self.box2)).grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self, text="Compress Documents", command=self.compress_documents).pack(pady=10)

        # Main Text Compression Section
        self.original_label1 = ttk.Label(upload_frame, text="Original Size: -")
        self.original_label1.grid(row=2, column=0, padx=10, pady=(0, 2), sticky="w")

        self.compressed_label1 = ttk.Label(upload_frame, text="Compressed Size: -")
        self.compressed_label1.grid(row=3, column=0, padx=10, pady=(0, 2), sticky="w")

        self.ratio_label1 = ttk.Label(upload_frame, text="Compression Ratio: -")
        self.ratio_label1.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="w")

        # Comparison Text Compression Section
        self.original_label2 = ttk.Label(upload_frame, text="Original Size: -")
        self.original_label2.grid(row=2, column=1, padx=10, pady=(0, 2), sticky="w")

        self.compressed_label2 = ttk.Label(upload_frame, text="Compressed Size: -")
        self.compressed_label2.grid(row=3, column=1, padx=10, pady=(0, 2), sticky="w")

        self.ratio_label2 = ttk.Label(upload_frame, text="Compression Ratio: -")
        self.ratio_label2.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="w")

        # Encoded Huffman boxes section
        encoded_frame = ttk.LabelFrame(self, text="Huffman Codes")
        encoded_frame.pack(fill="x", padx=15, pady=10)

        self.encoded_box1 = scrolledtext.ScrolledText(encoded_frame, width=40, height=10, font=("Courier", 10), state='disabled')
        self.encoded_box1.grid(row=0, column=0, padx=10, pady=10)

        self.encoded_box2 = scrolledtext.ScrolledText(encoded_frame, width=40, height=10, font=("Courier", 10), state='disabled')
        self.encoded_box2.grid(row=0, column=1, padx=10, pady=10)


    def load_file_into_box(self, box):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
                box.delete("1.0", tk.END)
                box.insert(tk.END, contents)

    def compress_documents(self):
        for idx, (box, orig_label, comp_label, file_prefix, encoded_box) in enumerate([
            (self.box1, self.original_label1, self.compressed_label1, "doc1", self.encoded_box1),
            (self.box2, self.original_label2, self.compressed_label2, "doc2", self.encoded_box2)
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

                orig_label.config(text=f"Original Size: {orig_size} bytes")
                comp_label.config(text=f"Compressed Size: {comp_size} bytes")

                # Calculate compression ratio
                compression_ratio = (100 - (comp_size / orig_size) * 100) if orig_size else 0
                ratio_text = f"Compression Ratio: {compression_ratio:.2f}%"

                if idx == 1:
                    self.ratio_label1.config(text=ratio_text)
                else:
                    self.ratio_label2.config(text=ratio_text)

                # Format and display Huffman codes
                formatted_codes = "Huffman Codes:\n\n"
                for symbol, code in sorted(huff_codes.items(), key=lambda item: (len(item[1]), item[0])):
                    if symbol == " ":
                        symbol_display = "␣"  # use ␣ for space for clarity
                    elif symbol == "\n":
                        symbol_display = "\\n"
                    elif symbol == "\t":
                        symbol_display = "\\t"
                    else:
                        symbol_display = symbol
                    formatted_codes += f"{symbol_display}: {code}\n"

                encoded_box.config(state='normal')
                encoded_box.delete("1.0", tk.END)
                encoded_box.insert(tk.END, formatted_codes.strip())
                encoded_box.config(state='disabled')
            else:
                orig_label.config(text=f"Original Size: -")
                comp_label.config(text=f"Compressed Size: -")
                if idx == 1:
                    self.ratio_label1.config(text="Compression Ratio: -")
                else:
                    self.ratio_label2.config(text="Compression Ratio: -")
                encoded_box.config(state='normal')
                encoded_box.delete("1.0", tk.END)
                encoded_box.insert(tk.END, "")
                encoded_box.config(state='disabled')


class SearchPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Real-Time Search", font=("Segoe UI", 14, "bold"), foreground="#2F2D92").pack(pady=10)
        ttk.Button(self, text="← Back to Home", command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10)

        # Upload & Search Section
        upload_frame = ttk.LabelFrame(self, text="Upload and Search")
        upload_frame.pack(fill="x", padx=15, pady=10)

        ttk.Button(upload_frame, text="Upload Document", command=self.load_document).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(upload_frame, text="Search Word/Phrase:").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.search_entry = ttk.Entry(upload_frame, width=30)
        self.search_entry.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.perform_search)

        self.result_label = ttk.Label(upload_frame, text="Occurrences Found: 0")
        self.result_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Text Box Section
        self.text_box = scrolledtext.ScrolledText(self, wrap="word", width=80, height=20, font=("Courier", 10))
        self.text_box.pack(padx=15, pady=10)
        self.text_box.tag_config("highlight", background="yellow")

    def load_document(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, content)
                self.perform_search()  # Trigger search after load

    def perform_search(self, event=None):
        phrase = self.search_entry.get().strip()
        text = self.text_box.get("1.0", tk.END)
        self.text_box.tag_remove("highlight", "1.0", tk.END)

        if not phrase:
            self.result_label.config(text="Occurrences Found: 0")
            return

        count = 0
        idx = "1.0"

        # Naive search
        while True:
            idx = self.text_box.search(phrase, idx, nocase=True, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(phrase)}c"
            self.text_box.tag_add("highlight", idx, end_idx)
            idx = end_idx
            count += 1

        self.result_label.config(text=f"Occurrences Found: {count}")


# TODO: Add BFS/DFS inputs and visualization later
class GraphAnalysisPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Graph Analysis", font=("Segoe UI", 14, "bold"), foreground="#2F2D92").pack(pady=10)
        ttk.Button(self, text="← Back to Home", command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10)


# TODO: Add Merge or Counting Sort Backend
class SortingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Sorting", font=("Segoe UI", 14, "bold"), foreground="#2F2D92").pack(pady=10)
        ttk.Button(self, text="← Back to Home", command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10)

        # Upload Folder Section 
        folder_frame = ttk.LabelFrame(self, text="Upload Document Folder")
        folder_frame.pack(fill="x", padx=15, pady=10)

        ttk.Button(folder_frame, text="Upload Folder", command=self.upload_folder).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.folder_label = ttk.Label(folder_frame, text="No folder selected", font=("Segoe UI", 10))
        self.folder_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Sorting Options
        sorting_frame = ttk.LabelFrame(self, text="Sorting Options")
        sorting_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(sorting_frame, text="Sort By:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")


        self.sort_choice = ttk.Combobox(sorting_frame, values=["Author", "Title", "Date"], width=20)
        self.sort_choice.set("Sort By")
        self.sort_choice.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Button(sorting_frame, text="Sort", command=self.sort_documents).grid(row=0, column=2, padx=10, pady=10, sticky="w")

        
    def upload_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_label.config(text=folder_path)
        else:
            self.folder_label.config(text="No folder selected")

    def sort_documents(self):
        print("Sorting... ")


if __name__ == "__main__":
    app = CSUFScanner()
    app.mainloop()
