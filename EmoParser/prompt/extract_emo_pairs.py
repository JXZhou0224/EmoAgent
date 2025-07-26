extract_emo_pairs_template = '''
You are an expert in emotional psychology and an experienced novel reader.
Your task is to extract all the emotional reaction of the character: {main_character} from a text segment sliced from a novel.

Here is the text segment:
{text}

-----

Here are some requirements:

1. A reaction of the character constitutes an emotional reaction only when the author explicitly indicates that the character react in an emotional way (in words, physical reactions, or thoughts), do not over interpret.
2. It is fine if the whole text doesn't contain any emotional reaction of the character at all. In that case simply output "None".
3. Pay attention to the detailed description of the character.
4. However, if some other characters interact with {main_character}, but the {main_character} does not react emotionally, do not include it in the output.

Your extraction of emotional reaction should contain the following dimensions:
- ending: you should copy the original part in the text segment that indicates that character: {main_character} is expressing an emotion. 
    If the part is too long, take the most crucial section of it. Typically, you should only copy less then 5 words. As long as user can uniquely identify the part you are refering to, it is acceptable.
- trigger: What specific incident triggerred the emotion. 
    Remember, triggerring event is direct and specific, such as hearing a sentence from another character, seeing particular things or recalling past events. Be sure to include details that may contribute to the formation of emotion.
- reaction: extraction of the character's emotional reaction towards the trigger event.
    You may include the character's thought, experssions, actions, physicial responses if applicable.
- emotion: a general classifcation of emotion expressed through the reaction.
    Both a single word to describe the emotion, and multiple words to express a mixed feeling are acceptable.

Now, please output a list of emotional reactions you observe in the above text. You should output in the following jsonl format, omitting the "```jsonl" and "```":
{{"ending":"", "trigger":"","reaction":"","emotion":""}}
{{"ending":"", "trigger":"","reaction":"","emotion":""}}
...
or output only "None" if there are no emotional reaction of the character observed.
'''