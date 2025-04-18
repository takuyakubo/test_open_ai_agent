from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

weather_agent = Agent(
    name="Simple Agent",
    instructions="あなたは質問について答えるAgentです。",
)


async def main():
    result = await Runner.run(weather_agent, input="アメリカの首都はどこですか？")
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
# => アメリカの首都はワシントンD.C.です。
