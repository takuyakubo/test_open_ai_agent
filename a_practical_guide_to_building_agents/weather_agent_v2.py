from typing import Any

from agents import Agent, FunctionTool, RunContextWrapper, Runner
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class GetWeatherArgs(BaseModel):
    city: str

    class Config:
        extra = "forbid"


async def _get_weather(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = GetWeatherArgs.model_validate_json(args)

    def func(data):
        return "快晴"

    return func(data=f"目的の都市は、{parsed.city}です。")


get_weather = FunctionTool(
    name="get_weather",
    description="get weather data",
    params_json_schema=GetWeatherArgs.model_json_schema(),
    on_invoke_tool=_get_weather,
)

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
