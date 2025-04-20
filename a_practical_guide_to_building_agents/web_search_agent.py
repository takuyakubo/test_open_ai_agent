import uuid
from pathlib import Path

from agents import Agent, Runner, WebSearchTool, function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool
def save_results(output: str):
    # db.insert({"output": output, "timestamp": datetime.time()})
    filename = str(uuid.uuid4()) + ".txt"
    with Path(filename).open("w") as f:
        f.write(f"調査結果は以下のとおりです。\n\n {output}")
    return f"File saved; filename: {filename}"


search_agent = Agent(
    name="Search agent",
    instructions="あなたはユーザーがインターネットで検索し、要求に応じて結果を保存するのを支援するAgentです。",
    tools=[WebSearchTool(), save_results],
)


async def main():
    result = await Runner.run(
        search_agent,
        input="最新のOpenAIのLLMの名前は？結果をファイルに保存して下さい。",
    )
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
