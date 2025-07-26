from tiktoken import get_encoding
import json

def count_tokens(text, model="gpt-4o-mini"):
    """
    Count the number of tokens in a text using the specified model's tokenizer.
    """
    encoding = get_encoding(model)
    return len(encoding.encode(text))

def load_text(file, encoding="utf-8"):
    # this should be able to load chinese
    with open(file, "r", encoding=encoding) as f:
        return f.read()

def load_jsonl(dir):
    ret = []
    with open(dir,"r") as f:
        txt = f.readlines()
        ret = [json.loads(ins) for ins in txt]
    return ret

def dump_jsonl(list_dict,dir):
    with open(dir,"w") as f:
        for ins in list_dict:
            f.write(json.dumps(ins)+"\n")
            

