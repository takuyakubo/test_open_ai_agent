from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool
def get_weather(city: str) -> str:
    return f"{city} の天気は快晴です。"


weather_agent = Agent(
    name="Weather agent",
    instructions="あなたは天気について答えることができるAgentです。",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(weather_agent, input="今日の東京の天気を教えて下さい。")
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
