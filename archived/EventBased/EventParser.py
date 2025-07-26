from API import LLMFactory, BaseLLM
from Entity import Character, Context
from PlotGraph import Event, Timeline
import prompt.identify_next_event
import prompt.update_entity

import os
import json

import prompt.update_hints

WINDOW_SIZE = 1000
INCREMENT = 700


class EventParser:
    def __init__(self,save_dir:str,text: str,llm:BaseLLM, increment = INCREMENT, window_size = WINDOW_SIZE):
        self.save_dir = save_dir
        self.text = text
        self.llm = llm
        self.increment = increment
        self.window_size = window_size
        self.timeline = Timeline()
        self.context = Context()
        self.characters:dict[str,Character] = {}

    def run(self):
        '''
        input: text
        output: The timeline of event, accompanied reaction
        '''
        # iterate with sliding window
        # fill in the blank for events, one or many, or none
        # update the entities, environment changes
        # identify the pronoun's and references at tail
        text = self.text
        text_start = 0
        pronoun_mapping = {}
        current_event = self.timeline.get_init_event()
        while(text_start < len(text)):
            cur_text = text[text_start:text_start+self.window_size]
            self.update_entity(cur_text,pronoun_mapping)
            event_length, event = self.identify_next_event(cur_text,current_event,pronoun_mapping)
            pronoun_mapping = self.update_pronoun(cur_text,pronoun_mapping)
            if event_length == -1:
                #TODO: this event is larger than the window. generate a temporary summary.
                raise NotImplementedError()
                text_start+=self.window_size
                continue

            event.original_text_start = text_start
            event.original_text_end = text_start+event_length

            self.timeline.insert_event(event,current_event)

            current_event = event
            text_start += event_length


    def update_entity(self,text,pronoun_mapping):
        '''
        identify new character, update context 
        '''
        character_list = "\n".join([f"{character.name}: {str(character.alias)}"for character in self.characters.values()])
        cur_prompt = prompt.update_entity.identify_character_prompt.format(character_list=character_list,text=text,pronoun_mapping=pronoun_mapping)
        response = self.llm.generate(cur_prompt)
        for action in response.split("\n"):
            loaded_action = json.loads(action)
            if(loaded_action["action"] == "new"):
                self.characters[loaded_action["name"]]=Character(
                        name = loaded_action["name"],
                        alias = loaded_action["alias"]
                    )
            elif(loaded_action["action"] == "alias"):
                flag = False
                for character in self.characters.values():
                    if character.name == loaded_action["name"]:
                        flag = True
                        character.alias = character.alias + loaded_action["alias"]
                        break
                if flag == False:
                    raise Exception("LLM generated invalid response")
            elif(loaded_action["action"] == "end"):
                break
            else:
                raise Exception(f"LLM generated invalid action:{action}")
            
        #TODO: update context here
            

    def identify_next_event(self,text:str,last_event:Event,pronoun_mapping:dict[str,str]) -> tuple[int, Event]:
        '''
        1. identify the separation of event, output the starting location of the next new event
        2. fill in the events
        TODO: make past_events into real events
        '''
        cur_prompt = prompt.identify_next_event.identify_next_event_prompt.format(
            characters=self.dump_characters(),
            past_events = last_event.model_dump_json(),
            pronoun_mapping = pronoun_mapping,
            text = text
        )
        response = json.loads(self.llm.generate(cur_prompt))
        if response["end"] == "False":
            return -1,None
        loc = text.find(response["ending_sentence"])
        if(loc == -1):
            raise Exception("LLM generated invalid ending sentence")
        length = loc+len(response["ending_sentence"])
        
        for event_character in response["event"]["character"]:
            if not event_character in self.characters:
                raise Exception("LLM generated invalid character not in the list")

        ret_event = Event(
            time = response["event"]["time"],
            place = response["event"]["place"],
            character = response["event"]["character"],
            summary = response["event"]["summary"],
            reaction = response["event"]["reaction"]
        )
        return length, ret_event


    def update_pronoun(self,text, pronoun_mapping:dict[str,str]):
        cur_prompt = prompt.update_hints.update_pronoun_prompt.format(
            characters = self.dump_characters(),
            pronoun_mapping = pronoun_mapping,
            text = text
        )

    def save(self):
        with open(os.path.join(self.save_dir, "timeline.json"), "w") as f:
            f.write(self.timeline.model_dump_json(indent=2))
        for character in self.characters.values():
            with open(os.path.join(self.save_dir, "characters", f"{character.name}.json"), "w") as f:
                f.write(character.model_dump_json(indent=2))
        with open(os.path.join(self.save_dir, "context.json"), "w") as f:
            f.write(self.context.model_dump_json(indent=2))
    
    def dump_characters(self) -> str:
        return "\n".join([character.model_dump_json() for character in self.characters.values()])