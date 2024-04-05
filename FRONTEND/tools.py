import re


def break_into_chunks(text, max_words=200, overlap=30):

    words = re.findall(r'\w+', text)
    chunks = []
    current_chunk = []
    
    for i, word in enumerate(words):
        if len(current_chunk) + 1 > max_words:
            chunks.append(' '.join(current_chunk[:-overlap]))
            current_chunk = current_chunk[-overlap:]
        
        current_chunk.append(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    chunks = [chunk for chunk in chunks if len(chunk) > 80]
    return chunks