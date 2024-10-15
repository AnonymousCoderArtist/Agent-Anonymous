import requests
import json
from typing import Optional
from fake_useragent import UserAgent

class SambanovaAPI:
    def __init__(self, cookie_path: str, model: str = "Meta-Llama-3.2-1B-Instruct", system_prompt: Optional[str] = None, max_tokens: int = 2048):
        self.url = "https://cloud.sambanova.ai/api/completion"
        self.headers = self._get_headers()
        self.cookies = self._load_cookies(cookie_path)
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.available_models = ['Meta-Llama-3.1-405B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B-Instruct', 'Meta-Llama-3.2-1B-Instruct', 'Meta-Llama-3.2-3B-Instruct']
        if model not in self.available_models:
            raise ValueError(f"Invalid model selected.  Please choose from: {self.available_models}")
        self.model = model


    def _load_cookies(self, cookie_path: str):
        try:
            with open(cookie_path, 'r') as f:
                return {item['name']: item['value'] for item in json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading cookies: {e}")
            return {}

    def _get_headers(self):
        return {
            "accept": "text/event-stream",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://cloud.sambanova.ai",
            "priority": "u=1, i",
            "referer": "https://cloud.sambanova.ai/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": UserAgent().random
        }

    def _build_payload(self, prompt: str):
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}]
        return {
            "body": {
                "messages": messages,
                "max_tokens": self.max_tokens,
                "stop": ["<|eot_id|>"],
                "stream": True,
                "stream_options": {"include_usage": True},
                "model": self.model
            }
        }

    def chat(self, prompt: str) -> Optional[str]:
        payload = self._build_payload(prompt)
        try:
            response = requests.post(self.url, headers=self.headers, cookies=self.cookies, json=payload, stream=True)
            response.raise_for_status()
            return self._process_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def _process_response(self, response):
        result = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    if decoded_line.strip() == "data: [DONE]":
                        break
                    try:
                        data = json.loads(decoded_line[5:])
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                result += content
                    except json.JSONDecodeError as e:
                        pass
        yield result

if __name__ == "__main__":
    api = SambanovaAPI(r"G:\Anonymous-Agent\model\cookies.json", model="Meta-Llama-3.2-1B-Instruct")
    x = input(">>> ")
    result_generator = api.chat(x)
    
    if result_generator is not None:
        result = ''.join(result_generator)
        print(result)
    else:
        print("No result received.")
