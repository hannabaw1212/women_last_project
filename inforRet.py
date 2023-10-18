import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer

def google_custom_search(query, model,tokenizer ,api_key="", cx="", num=10):
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    
    API_KEY = "AIzaSyCrDMKsYHEUyjtBodR1ZddaO3NtiZtnbBI"
    CX = "b60632245bf074d94"
    parameters = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
        "num": num  # Number of search results to return between 1 and 10, inclusive
    }
    
    response = requests.get(base_url, params=parameters)

    search_results = response.json().get('items', [])

    if response.status_code != 200:
        return None
    
    snippets = [result["snippet"] for result in search_results]
    link = search_results[0]['link']
    combined_content = "\n".join(snippets)

    input_text = "" + combined_content
    input_tokenized = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_tokenized, max_length=350, min_length=140, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary, link
