import os        
import openai
import anthropic

class BaseLLM:
    def __init__(self, model_name, temperature=0.0):
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")

class LLMFactory:   
    _registry: dict[str,BaseLLM] = {}

    @classmethod   
    def register(cls,provider):
        def wrapper(llm_class):
            cls._registry[provider] = llm_class
            return llm_class
        return wrapper
    
    @classmethod
    def get_llm(self, provider, model_name, temperature=0.0) -> BaseLLM:
        if provider not in self._registry:
            raise ValueError(f"Model {provider} is not registered.")
        return self._registry[provider](model_name, temperature)
    

@LLMFactory.register("dummy")
class Dummy(BaseLLM):
    def generate(self, prompt):
        return "haha"

@LLMFactory.register("openai")
class Openai(BaseLLM):

    def generate(self, prompt):
        print("-"*10, "Generating with OpenAI", "-"*10)
        print(prompt)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        print("-"*10, "Result", "-"*10)
        print(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()
        


@LLMFactory.register("anthropic")
class Anthropic(BaseLLM):

    def generate(self, prompt):
        client = anthropic.Anthropic(# defaults to os.environ.get("ANTHROPIC_API_KEY")
            )
        message = client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content.strip()