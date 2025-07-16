from tiktoken import get_encoding

def count_tokens(text, model="gpt-4o-mini"):
    """
    Count the number of tokens in a text using the specified model's tokenizer.
    """
    encoding = get_encoding(model)
    return len(encoding.encode(text))
