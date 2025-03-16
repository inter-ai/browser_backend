# app/nlp_service.py

from transformers import pipeline
from app.config import FLAN_T5_MODEL_NAME
import json

class NLPService:
    def __init__(self):
        """
        Loads a Flan-T5 model for text2text generation.
        Make sure FLAN_T5_MODEL_NAME is defined in app/config.py,
        e.g., FLAN_T5_MODEL_NAME = "google/flan-t5-small"
        """
        self.model = pipeline("text2text-generation", model=FLAN_T5_MODEL_NAME)

    def parse_command(self, command: str) -> dict:
        """
        Attempts to extract 'location' and 'severity' from a user command
        by prompting Flan-T5 with a structured format.

        Example usage:
          command = "There's a massive wildfire near RedwoodForest. It's quite severe."
          result = parse_command(command)
          # result might look like {"location": "RedwoodForest", "severity": "HighSeverity"}

        If the model returns unparseable or incomplete JSON, we handle errors gracefully
        and return a fallback dict.
        """
        prompt = (
            "Extract wildfire severity and location from this text as JSON:\n"
            f"'{command}'\n"
            "Return output in the form {\"location\":..., \"severity\":...}"
        )
        output = self.model(prompt, max_length=128, do_sample=False)
        generated_text = output[0]["generated_text"].strip()

        # Attempt to parse the model's output as JSON.
        # If parsing fails, fallback to a basic structure.
        try:
            parsed = json.loads(generated_text)
            if "location" not in parsed or "severity" not in parsed:
                # If we don't see the required keys, fallback.
                return {"location": "Unknown", "severity": "Unknown", "raw": generated_text}
            return parsed
        except (json.JSONDecodeError, TypeError):
            # If the model output isn't valid JSON
            return {"location": "Unknown", "severity": "Unknown", "raw": generated_text}
