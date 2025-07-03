import os
import re
import pandas as pd
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


from nltk.tokenize import word_tokenize, sent_tokenize

# For syllable and complex word estimation
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    if count == 0:
        count = 1
    return count

def is_complex(word):
    return count_syllables(word) > 2

# Load stopwords from folder
def load_stopwords(folder):
    stop_words = set()
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), 'r', encoding='ISO-8859-1') as f:
            stop_words.update([line.strip().lower() for line in f])
    return stop_words

# Load sentiment dictionary
def load_dictionary(path):
    with open(path, 'r') as f:
        return set(line.strip().lower() for line in f)

stop_words = load_stopwords("StopWords")
positive_words = load_dictionary("MasterDictionary/positive-words.txt")
negative_words = load_dictionary("MasterDictionary/negative-words.txt")

# Analysis function
def analyze_text(text):
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation
    words = word_tokenize(text_clean.lower())
    words = [w for w in words if w not in stop_words and w.isalpha()]
    sentences = sent_tokenize(text)

    word_count = len(words)
    sentence_count = len(sentences) if len(sentences) > 0 else 1

    positive_score = sum(1 for w in words if w in positive_words)
    negative_score = sum(1 for w in words if w in negative_words)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    avg_sentence_length = word_count / sentence_count
    complex_words = [w for w in words if is_complex(w)]
    percentage_complex = len(complex_words) / word_count
    fog_index = 0.4 * (avg_sentence_length + percentage_complex)

    syllable_count = sum(count_syllables(w) for w in words)
    avg_word_length = sum(len(w) for w in words) / word_count

    pronouns = re.findall(r"\b(I|we|my|ours|us)\b", text, re.I)
    
    return {
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_sentence_length,
        "COMPLEX WORD COUNT": len(complex_words),
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_count / word_count,
        "PERSONAL PRONOUNS": len(pronouns),
        "AVG WORD LENGTH": avg_word_length
    }
# Combine everything and save output
input_df = pd.read_excel("Input.xlsx")
results = []

for idx, row in input_df.iterrows():
    url_id = str(row["URL_ID"])
    try:
        with open(f"articles/{url_id}.txt", "r", encoding="utf-8") as file:
            text = file.read()
            metrics = analyze_text(text)
            row_data = row.to_dict()
            row_data.update(metrics)
            results.append(row_data)
    except FileNotFoundError:
        print(f"File for URL_ID {url_id} not found.")

# Convert and save to CSV
output_df = pd.DataFrame(results)
output_df.to_excel("output.xlsx", index=False)
print("✅ Text analysis complete and saved to output.xlsx")
