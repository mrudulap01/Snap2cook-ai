import json
import logging
from openai import AsyncOpenAI
from pydantic import BaseModel
from config.settings import settings

logger = logging.getLogger("AIClient")

class ModelUnavailableError(Exception):
    pass

class AIClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.AI_BASE_URL,
            api_key=settings.AI_API_KEY
        )
        
    async def generate_vision(self, messages, response_model=None):
        return await self._generate(
            messages=messages, 
            primary_model=settings.VISION_MODEL, 
            fallback_model=settings.FALLBACK_VISION_MODEL,
            response_model=response_model
        )
        
    async def generate_text(self, messages, response_model=None):
        return await self._generate(
            messages=messages, 
            primary_model=settings.TEXT_MODEL, 
            fallback_model=settings.FALLBACK_TEXT_MODEL,
            response_model=response_model
        )
        
    async def _generate(self, messages, primary_model, fallback_model, response_model=None):
        kwargs = {
            "messages": messages,
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
            "top_p": settings.TOP_P
        }
        
        if response_model:
            kwargs["response_format"] = {"type": "json_object"}
            
        try:
            logger.info(f"Attempting to generate with primary model: {primary_model}")
            response = await self.client.chat.completions.create(
                model=primary_model,
                **kwargs
            )
            return self._parse_response(response, response_model)
        except Exception as e:
            logger.warning(f"Primary model {primary_model} failed: {e}. Trying fallback: {fallback_model}")
            
            if not fallback_model:
                raise ModelUnavailableError("The selected AI model is currently unavailable and no fallback was configured.")
                
            try:
                response = await self.client.chat.completions.create(
                    model=fallback_model,
                    **kwargs
                )
                return self._parse_response(response, response_model)
            except Exception as e2:
                logger.error(f"Fallback model {fallback_model} also failed: {e2}")
                raise ModelUnavailableError("The selected AI models are currently unavailable. Please choose another model in the configuration.")

    def _parse_response(self, response, response_model):
        response_text = response.choices[0].message.content.strip()
        if not response_model:
            return response_text
            
        try:
            parsed_data = json.loads(response_text)
            return response_model(**parsed_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parsing Error: {e}\nResponse: {response_text}")
            raise ValueError(f"Failed to parse AI response: {e}")
        except Exception as e:
            logger.error(f"Pydantic Validation Error: {e}\nResponse: {response_text}")
            raise ValueError(f"Failed to validate AI response into {response_model.__name__}: {e}")
