identify_next_event_prompt="""
You will be given a segment of text, which is a part of a novel.
Your task is to identify the next unit event. 
An unit event is an event that occurred in the novel that cannot be further decomposed, such as a discussion on a same topic, a continuous set of actions for a same purpose and an internal monologue of a character.
An event is not necessarily an incident that happened. Typically, a unit event is less than 300 words.

Here are the characters appeared in the novel:
{characters}

Here are the past events happened before the text segment:
{past_events}

As some of the pronouns maybe unclear here, here is the pronoun mapping summarized from text before the text segment. This may subject to change throughout the text:
{pronoun_mapping}

Here is the text segment you need to identify event from:
{text}

Your task is to identify the ending sentence of the next unit event, or report that this event is still ongoing upto the last line of the text. If the ending sentence exists, you should provide summary of the event in the following format. Sometimes, information such as time and place maybe unavailable in the text, you may seek information from the last event, if the two events are closely connected.

You should output in the following json format:
{{
    "reasoning": "",
    "end": "True"
    "ending_sentence": "" (copy the ending sentence of the first unit event here, up to puncuation)
    "event":{{
        "time": ""
        "place": ""
        "character": ["<name1>","<name2>"] (character involved in the event. You must copy the exact "name" from the character list)
        "summary": "" (a summary of what happened)
        "reaction": "" (the reaction of the main character or "I")
    }}
}}

"""