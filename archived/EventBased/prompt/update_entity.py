identify_character_prompt="""
You will be given a segment of text, which is a part of a novel.
Your task is to identify the new characters and the new aliases of the existing characters in the text.

name should be a unique identifier for the character, and alias should be a list of names that the character is known by.
If the character is new, you should create a new name for it.
If the character is already known, you should add the new alias to the existing character.

Here are the existing characters and their aliases:
{character_list}

Here is the text:
{text}

If there are any pronouns in the text you are not sure about, please refer to the below pronoun mapping.
{pronoun_mapping}

If the pronoun mapping is empty and you see an uncertain pronoun equivalent to "I", then you are allowed to create a new character named "I", indicating this the story is written in first person. In this case, this character's actual name should be place in the alias section later, if his real name were to appear.

your valid action are as follows:
1. {{"action": "new", "name": "<character_name>", "alias": ["<alias1>", "<alias2>"]}} (alias can be empty [])
2. {{"action": "alias", "name": "<character_name>", "alias": ["<alias1>", "<alias2>"]}}(only the newly added alias of the existing character)
3. {{"action": "end"}} this means the end of your action sequence. If there are no new names or characters, simply output this action
Now, please output your actions in jsonl format, one action per line. Do NOT include "```jsonl" or "```".
"""

