import json
from utils.mapping_utils import map_to_cv_extraction, map_to_job_description_extraction
from mistralai import Mistral
from pydantic import ValidationError
from models.cv_model import CVExtraction
from models.job_post_model import JobDescriptionExtraction

class MistralLanguageModel:
    def __init__(self, api_key: str, model_choice: str, temperature=0.5):
        if api_key is None:
            raise ValueError("The Mistral API KEY must be provided as an argument or an environment variable.")
        self.api_key = api_key
        self.model_choice = model_choice
        self.temperature = temperature
        self.client = Mistral(api_key=self.api_key)

        # Model costs
        self.model_costs = {
            'mistral-small-latest': {'input': 0.9, 'output': 2.8},
            'mistral-large-latest': {'input': 2.7, 'output': 8.2},
            'open-mistral-7b': {'input': 0.25, 'output': 0.25},
            'open-mixtral-8x7b': {'input': 0.7, 'output': 9.0},
            'open-mixtral-8x22b': {'input': 2.0, 'output': 6.0},
            'ministral-3b-latest': {'input': 0.04, 'output': 0.04}
        }
        
        if self.model_choice not in self.model_costs:
            raise ValueError(f"Model '{self.model_choice}' not recognized.")

    def generate(self, prompt: str, output_format=None):
        messages = [{"role": "user", "content": prompt}]
        params = {
            "model": self.model_choice,
            "messages": messages,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"}
        }
        response = self.client.chat.complete(**params)
        response_content = response.choices[0].message.content

        if output_format:
            try:
                parsed_data = json.loads(response_content)
                
                # Apply appropriate mapping based on the output format
                if output_format == CVExtraction:
                    transformed_data = map_to_cv_extraction(parsed_data)
                elif output_format == JobDescriptionExtraction:
                    transformed_data = map_to_job_description_extraction(parsed_data)
                else:
                    transformed_data = parsed_data  # No transformation needed

                # Validate transformed data with Pydantic model
                validated_data = output_format(**transformed_data)
                return validated_data
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Invalid response format: {e}")
        else:
            return response_content

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        input_cost_per_token = self.model_costs[self.model_choice]['input'] / 1_000_000
        output_cost_per_token = self.model_costs[self.model_choice]['output'] / 1_000_000

        input_cost = prompt_tokens * input_cost_per_token
        output_cost = completion_tokens * output_cost_per_token

        return input_cost + output_cost
