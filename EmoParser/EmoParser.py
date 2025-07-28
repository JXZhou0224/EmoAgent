import json,os

from API import BaseLLM
from .prompt import extract_emo_pairs
from utils import dump_jsonl

WINDOW_SIZE = 4000
OVERLAP = 1000

class EmoParser:
    def __init__(self,save_dir:str,llm: BaseLLM,text,main_character,window_size = WINDOW_SIZE, overlap = OVERLAP):
        self.save_dir = save_dir
        self.text:str = text
        self.llm = llm
        self.main_character = main_character
        self.window_size = window_size  
        self.overlap = overlap
        self.emo_pairs = []

        os.makedirs(self.save_dir,exist_ok=True)

    def run(self):
        cur_loc = 0
        pronoun_mapping = {}
        lst_text = ""
        while cur_loc != len(self.text):
            cur_text, tail = self.get_text_window(cur_loc)
            pronoun_mapping = self.update_pronoun(lst_text,cur_text,pronoun_mapping)
            self.emo_pairs += self.extract_emo_pairs(cur_loc,cur_text,lst_text)
            if tail == len(self.text):
                break
            cur_loc += WINDOW_SIZE
            lst_text = cur_text
            self.save()
            
    def extract_emo_pairs(self,cur_loc: int,cur_text: str,lst_text: str) -> list[dict[str,str | int]]:
        '''
        emo_pair:
        {
            "loc": location in the novel, in terms of char,
            "ending": ending sentence of emotional reaction
            "trigger": brief description of what happened,
            "reaction": the reaction of emotion, in terms of the four dims of emotion,
            "emotion": "generic classification of emotion"
        }
        '''
        prompt = extract_emo_pairs.extract_emo_pairs_template.format(
            text = cur_text,
            main_character = self.main_character,
            lst_text = lst_text
        )
        response = self.llm.generate(prompt)
        if(response == "None"):
            return []
        ret = []
        for rsp in response.split("\n"):
            loaded=json.loads(rsp)
            loc = cur_text.find(loaded["ending"])
            if loc == -1:
                loc = cur_loc
            else:
                loc += cur_loc
            
            loaded["loc"] = loc
            ret.append(loaded)
        print(ret)
        return ret

    def update_pronoun(self,lst_text:str,cur_text,pronoun_mapping:dict[str,str]) -> dict[str,str]:
        '''
        TODO: update the pronoun mapping, return the updated mapping
        '''
        cur_prompt = extract_emo_pairs.update_pronoun_template.format(lst_text=lst_text,text=cur_text,pronoun_mapping=pronoun_mapping)
        response = self.llm.generate(cur_prompt)
        pronoun_mapping = json.loads(response)
        return pronoun_mapping
    
    def get_text_window(self,start) -> tuple[str,int]:
        if(start == len(self.text)):
            return ""
        tail = min(start+self.window_size,len(self.text))
        sliced = self.text[start:tail]
        return sliced, tail
    
    def save(self):
        with open(os.path.join(self.save_dir,"emo_pairs.jsonl"),"w") as f:
            for ins in self.emo_pairs:
                f.write(json.dumps(ins)+"\n")
        

