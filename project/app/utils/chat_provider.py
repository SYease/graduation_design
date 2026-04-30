import json

from app.utils.chat_engine import match_answer

try:
    import requests
except ImportError:
    requests = None


class RuleBasedProvider:
    name = 'rule_based'

    def ask(self, question):
        return match_answer(question)


class LLMProvider:
    name = 'llm'

    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = (base_url or 'https://api.openai.com/v1').rstrip('/')
        self.model = model or 'gpt-3.5-turbo'

    def ask(self, question):
        if requests is None:
            return match_answer(question)

        system_prompt = (
            '你是算法与数据结构学习助手。请用中文回答用户的问题。'
            '回答应准确、简洁，适合学习者理解。'
            '仅回答与算法、数据结构、编程学习相关的问题。'
            '如果问题超出范围，请礼貌地引导用户提出算法相关的问题。'
        )

        try:
            resp = requests.post(
                f'{self.base_url}/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}',
                },
                json={
                    'model': self.model,
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': question},
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1000,
                },
                timeout=30,
            )
            resp.raise_for_status()
            body = resp.json()
            answer = body['choices'][0]['message']['content'].strip()
            topic = self._extract_topic(question)
            return (answer, topic)
        except Exception:
            return match_answer(question)

    def _extract_topic(self, question):
        """Extract knowledge topic from the question using keyword matching."""
        from app.utils.chat_engine import QA_KNOWLEDGE_BASE

        best_topic = ''
        best_score = 0
        for entry in QA_KNOWLEDGE_BASE:
            score = sum(1 for kw in entry.get('keywords', []) if kw.lower() in question.lower())
            if score > best_score:
                best_score = score
                best_topic = entry.get('topic', '')
        return best_topic


def get_provider(config):
    provider_name = (config.get('AI_PROVIDER') or 'rule_based').lower()
    if provider_name == 'llm' and config.get('AI_API_KEY'):
        return LLMProvider(
            api_key=config.get('AI_API_KEY'),
            base_url=config.get('AI_BASE_URL'),
            model=config.get('AI_MODEL'),
        )
    return RuleBasedProvider()
