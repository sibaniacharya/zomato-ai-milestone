import logging
import time
from groq import Groq
from src.config import Settings

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.fallback_model = settings.GROQ_FALLBACK_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        self.max_retries = settings.GROQ_MAX_RETRIES

    def complete(self, system_prompt: str, user_prompt: str, use_fallback: bool = False, low_temp: bool = False) -> str:
        model_to_use = self.fallback_model if use_fallback else self.model
        temp_to_use = 0.1 if low_temp else self.temperature
        
        backoff = [1, 2, 4]
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = self.client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temp_to_use,
                    response_format={"type": "json_object"}
                )
                duration = int((time.time() - start_time) * 1000)
                usage = response.usage
                logger.info(f"Groq API call: model={model_to_use}, latency={duration}ms, prompt_tokens={usage.prompt_tokens if usage else '?'}, completion_tokens={usage.completion_tokens if usage else '?'}")
                
                content = response.choices[0].message.content
                if content is None:
                    raise ValueError("Groq returned empty content.")
                return content
            except Exception as e:
                logger.warning(f"Groq API attempt {attempt+1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(backoff[attempt])
                else:
                    if not use_fallback:
                        logger.warning("Switching to fallback model...")
                        return self.complete(system_prompt, user_prompt, use_fallback=True, low_temp=low_temp)
                    raise Exception("Groq API calls exhausted.") from e
