update_pronoun_prompt = """
You will be given a segment of text, which is a part of a novel.
Your task is identify changes of reference of pronouns.

Here are the characters appeared in the novel:
{characters}

Here is the pronoun mapping summarized from the text before the text segment.
{pronoun_mapping}

Here is the text segment you need to recognize pronoun references.
{text}

Now, please output the latest mapping of pronoun based on the text segment. This will be used to clarify pronoun references for future texts.
You are allowed to add new pronouns to the output

You should output in the following format:
{{
    "<pronoun>": "<reference character or entity>"
    "<pronoun>": "<reference character or entity>"
    ...
}}

"""