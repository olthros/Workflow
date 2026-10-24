import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY", "sk-填入你的Key备用"),
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
)

class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def run(self, input_text):
        print(f"\n[{self.name}] 正在思考...")
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_text}
        ]
        try:
            response = client.chat.completions.create(
                model="deepseek-chat", 
                messages=messages,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"【{self.name} 报错】: {str(e)}"

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="编码Agent",
            system_prompt="你是一个资深程序员。请根据用户的需求，直接输出完整的Python代码，不要输出多余的解释，代码用Markdown格式包裹。"
        )

class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="审查Agent",
            system_prompt="你是一个严格的代码审查员。请检查代码的逻辑错误、Bug或安全隐患。如果代码完美，请回复'[PASS]'；如果有问题，请指出具体问题及修改建议。"
        )

class FixerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="修复Agent",
            system_prompt="你是一个代码修复专家。请根据审查意见，修改原始代码。直接输出修复后的完整代码，用Markdown格式包裹。"
        )