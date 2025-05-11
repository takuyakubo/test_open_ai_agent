from agents import Agent, Runner
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel as Model_
from dotenv import load_dotenv
from openai import AsyncOpenAI

import os

load_dotenv()


# Anthropic 
anthropic_client = AsyncOpenAI(base_url="https://api.anthropic.com/v1/", api_key=os.getenv("ANTHROPIC_API_KEY"))
anthropic_model = Model_(model="claude-3-5-haiku-latest", openai_client=anthropic_client)

# Gemini
gemini_client = AsyncOpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = Model_(model="gemini-2.0-flash", openai_client=gemini_client)

# LMStudio
lms_client = AsyncOpenAI(base_url="http://localhost:1234/v1/")
lms_model = Model_(model="phi-4", openai_client=lms_client)

simple_agent = Agent(
    name="Simple Agent",
    instructions="あなたは質問について答えるAgentです。",
    model=lms_model,
)


async def main():
    result = await Runner.run(simple_agent, input="アメリカの首都はどこですか？")
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
# => アメリカの首都はワシントンD.C.です。
