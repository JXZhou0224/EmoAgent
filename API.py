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
    def get_llm(self, provider, model_name, base_url: str = None,temperature=0.0) -> BaseLLM:
        if provider not in self._registry:
            raise ValueError(f"Model {provider} is not registered.")
        if(base_url is None):
            return self._registry[provider](model_name, temperature)
        else:
            return self._registry[provider](model_name, temperature=temperature, base_url=base_url)
    

@LLMFactory.register("dummy")
class Dummy(BaseLLM):
    def generate(self, prompt):
        return "haha"

@LLMFactory.register("openai")
class Openai(BaseLLM):
    def __init__(self, model_name, base_url = None,temperature=0):
        self.model_name = model_name
        self.temperature = temperature
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = "https://api.openai.com/v1"

    def generate(self, prompt):
        print("-"*10, "Generating with OpenAI", "-"*10)
        print(prompt)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=self.base_url)
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

