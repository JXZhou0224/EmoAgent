general_context = """
You are an expert in emotional psychology and an experienced novel reader.
"""

extract_emo_pairs_template =general_context + """'''
Your task is to extract all the emotional reaction of the character: {main_character} from the target text segment sliced from a novel.

----

For continunity purposes, here are the text before the target text segment, if there are anything unclear, this previous text may provide hints:
{lst_text}

----

Here is the target text segment, you should extract emotional reactions from below:
{text}


-----



-----

Your extraction should follow the following scheme:
1. For every sentence, identify whether it is describing the character's, {main_character}. If the sentence is describing other characters talking or interacting with {main_character}, you should ignore it.
2. If the sentence is describing {main_character}, identify whether it is expressing the emotion of {main_character}, specific emotional reaction must be identified explicitly in the text, do not over interpret. If there is no explicit, written down description of emotion of {main_character}, you should ignore it.
3. If it is expressing an emotion, extract the following information:

Your extraction of emotional reaction should contain the following dimensions:
- ending: you should copy the original part in the text segment that indicates that character: {main_character} is expressing an emotion. 
    If the part is too long, take the most crucial section of it,depicting how {main_character} acted. Typically, you should only copy less then 5 words. As long as user can uniquely identify the part you are refering to, it is acceptable.
- trigger: What specific incident triggerred the emotion. 
    Remember, triggerring event is direct and specific, such as hearing a sentence from another character, seeing particular things or recalling past events. Be sure to include details that may contribute to the formation of emotion.
- reaction: extraction of the character's emotional reaction towards the trigger event.
    You may include the character's thought, experssions, actions, physicial responses if applicable.
- emotion: a general classifcation of emotion expressed through the reaction.
    Both a single word to describe the emotion, and multiple words to express a mixed feeling are acceptable.

Now, please output a list of emotional reactions you observe in the above text. You should output in the following jsonl format, omitting the "```jsonl" and "```":
case1: when no emotion reaction found:
None
Case2: when emotion reaction found:
{{"ending":"", "trigger":"","reaction":"","emotion":""}}
{{"ending":"", "trigger":"","reaction":"","emotion":""}}
...
"""

update_pronoun_template =general_context+"""
Your task is to generate the correspondence of pronouns and characters that occurred in the target text segment.

----

For continunity purposes, here are the text before the target text segment, if there are anything unclear, this previous text may provide hints:
{lst_text}

----

For your reference, here is the pronoun mapping of the previous text segment.
{pronoun_mapping}

----

Here is the target text segment, you should extract the pronoun mapping from below:
{text}

----

Your extraction should followig the scheme below:
1. You must identify all the pronouns that appeared in the text
2. for all of the pronouns spotted, deduce what entity they are referring to. If the referent of a single pronoun changes within the text, take the lastest one as the answer
3. If you cannot deduce the referent directly from the target text and previous text. You may take what's in the reference mapping of previous text segment for hint.
4. pay close attention to who "I" refers to, whether it is within someone's dialogue, or it is the story's narrative.

Please output in the following json format, omitting the ```json and ```.
{{
"pronoun1": "referent1",
...
}}
"""