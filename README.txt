# Blackcoffer Data Extraction & Text Analysis Assignment

## ✅ How the Solution Was Approached

This assignment was tackled in two main stages:

### 1. **Article Extraction**
- We read URLs and their IDs from `Input.xlsx`.
- Each article page was scraped using the `requests` library and parsed with `BeautifulSoup`.
- The title and main article body were extracted, excluding headers, footers, and irrelevant content.
- Each article was saved as a `.txt` file using its `URL_ID`.

### 2. **Text Analysis**
- For every article, the text was cleaned by removing punctuation and stop words (from the `StopWords/` folder).
- Tokenization was done using NLTK's `word_tokenize` and `sent_tokenize`.
- Sentiment scores were calculated based on `MasterDictionary/positive-words.txt` and `negative-words.txt`.
- Readability metrics were computed using standard formulas like Gunning Fog Index.
- The results were saved to an Excel file `output.xlsx` in the format of `Output Data Structure.xlsx`.

---

## ▶️ How to Run the Scripts

### 1. Install Required Dependencies
Make sure Python is installed (version >= 3.7). Then run:

```
pip install pandas requests beautifulsoup4 nltk openpyxl
```

### 2. Place Required Files
Ensure the following are in the same directory:
- `Input.xlsx` — The list of URL_IDs and URLs
- `StopWords/` — Folder with all stop word `.txt` files
- `MasterDictionary/` — Folder with positive and negative word lists
- `Output Data Structure.xlsx` — Used to structure the output

### 3. Run the Scripts

#### a. Extract Articles

```
python main.py
```

This will save the article text to the `articles/` folder as `URL_ID.txt` files.

#### b. Perform Text Analysis

```
python text_analysis.py
```

This will process all `.txt` files and output the results to:

```
output.xlsx
```

---

## 📦 Dependencies Required

- `pandas` – For reading/writing Excel files
- `requests` – For making HTTP requests
- `beautifulsoup4` – For parsing HTML content
- `nltk` – For text tokenization
- `openpyxl` – For writing Excel files

Install them using:
```
pip install pandas requests beautifulsoup4 nltk openpyxl
```

---

## 📁 Output

The final output file will be:

```
output.xlsx
```

containing all the computed metrics in the specified format.

