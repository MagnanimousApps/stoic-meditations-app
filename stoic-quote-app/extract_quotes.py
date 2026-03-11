import requests
import re

# 1. Download the public domain Meditations text (plain text)
url = "https://www.gutenberg.org/cache/epub/2680/pg2680.txt"
response = requests.get(url)
text = response.text

# 2. Optionally trim header/footer from Gutenberg
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
end_marker   = "*** END OF THIS PROJECT GUTENBERG EBOOK"
if start_marker in text and end_marker in text:
    text = text.split(start_marker)[-1].split(end_marker)[0]

# 3. Normalize whitespace
text = re.sub(r"\s+", " ", text).strip()

# 4. Split into sentences using punctuation
raw_sentences = re.split(r"(?<=[.!?])\s+", text)

# 5. Clean and filter
quotes = []
for s in raw_sentences:
    s = s.strip()
    if len(s) < 30:
        continue  # skip short bits
    if re.search(r"\d", s):
        continue  # skip numbered sections like "1.1", etc.
    quotes.append(s)

# 6. Deduplicate
unique_quotes = list(dict.fromkeys(quotes))

# 7. Output Python list to file safely
with open("all_meditations_quotes.py", "w", encoding="utf-8") as f:
    f.write("quotes = [\n")
    for q in unique_quotes:
        escaped = q.replace('"', '\\"')
        f.write(f'    "{escaped}",\n')
    f.write("]\n")

print(f"Total extracted quotes: {len(unique_quotes)}")