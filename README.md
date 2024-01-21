# sleepless

# Challenges: 

- Text to speech has, at most, 4096 characters per request.
This means that we will need to batch requests and stitch MP3's together.

- Although gpt-4-1106-preview has a 128k context window, 
this does not mean it can output up to 128k output tokens.
This just means that you could fit something like 300 pages of text into the _prompt_.

# Concepts to understand:

"Context window": The context window for a large language model (LLM) like OpenAI’s GPT refers to the maximum amount of text the model can consider at any one time when generating a response. This includes both the prompt provided by the user and the model’s generated text.
In practical terms, the context window limits how much previous dialogue the model can “remember” during an interaction.

Imagine you are a business with hundreds of pages of documents: which model best suits you?