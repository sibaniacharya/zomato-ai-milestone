import json
import logging
from typing import Set
from src.models.recommendation import LLMResponse

logger = logging.getLogger(__name__)

class ParseError(Exception):
    pass

class ResponseParser:
    def parse(self, raw: str, candidate_ids: Set[str]) -> LLMResponse:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {raw[:200]}")
            raise ParseError("Response is not valid JSON.") from e

        if "summary" not in data or "recommendations" not in data:
            raise ParseError("JSON missing 'summary' or 'recommendations' keys.")

        for item in data["recommendations"]:
            if "id" not in item or "rank" not in item or "explanation" not in item:
                raise ParseError(f"Recommendation item missing required fields: {item}")
            
            if str(item["id"]) not in candidate_ids:
                raise ParseError(f"LLM hallucinated restaurant ID: {item['id']}")

        return data
