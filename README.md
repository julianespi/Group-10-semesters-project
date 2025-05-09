##  Authors
- Julian Espinoza
- Helen Ngo
- Isaias Soria

##  Objective  
This tool is designed to scan student documents for plagiarism and extract key information such as duplicate phrases, citation structures, and compression statistics. It combines classical algorithms with user-friendly GUI functionality to support academic integrity and document analysis.

---

##  Features  

###  File Upload (via GUI)  
- Upload two plain text `.txt` documents.  
- Files are read and processed through a simple GUI interface.

###  Plagiarism Detection  
- **Rabin-Karp Algorithm**: Efficient rolling-hash string matching for duplicate phrase detection.  
- **KMP Algorithm**: Pattern searching for consistent phrase matches.  

###  Search
- **Naive Search**: Fast keyword/phrase lookups for real-time search during document review.

###  Compression  
- **Huffman Coding**:  
  - Applied to both documents after analysis.  
  - Shows compressed output and the compression ratio for space efficiency evaluation.

###  Display Results  
- Highlights:  
  - Matching phrases between documents.  
  - Compression ratio and related stats.  
- Intuitive GUI panels display matches and compression outcomes clearly.

###  Citation Graph (Optional Extension)  
- Model references/citations as a graph.  
- Use **BFS** or **DFS** to analyze citation relationships.

###  Sorting Support  
- Organize documents based on metadata (author, title, or date).  
- Uses **Merge Sort** or **Counting Sort** for efficient sorting.

###  Optimization Strategy  
- **Dynamic Programming** is used to prioritize which documents to scan first, based on relevance (e.g., risk score vs. scan time).

---

##  Notes  
- Make sure input files are in plain `.txt` format.  
- All modules are independently testable for easier debugging and scalability.  
- Optional extensions like citation graph visualization can be added using libraries like `networkx` or `matplotlib`.

---

##  Sample Workflow  
1. Launch the GUI.  
2. Upload two text documents.  
3. View matched sections and compression results.  
4. Optionally explore citation graphs or sorting features.

---
