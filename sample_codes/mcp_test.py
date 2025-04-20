import asyncio

from agents import Agent, OpenAIProvider, RunConfig, Runner, set_tracing_disabled
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

set_tracing_disabled(disabled=True)

run_config = RunConfig(
    model_provider=OpenAIProvider(
        api_key="hogehoge",  # ダミーキー
        base_url="http://localhost:1234/v1/",  # LM Studioのアドレス
        use_responses=False,  # LM Studioはresponse APIを持っていないためFalseにしておく
    ),
    model="phi-4",  # 使用するモデル名
)

mcp_params = {
    "command": "/opt/homebrew/bin/npx",
    "args": ["-y", "@anaisbetts/mcp-youtube"],
    "env": None,
}

agent = Agent(
    name="Simple Agent", instructions="あなたは与えられたタスクを行うAgentです。"
)

msg = "https://www.youtube.com/watch?v=skw3ShGu3_0 の内容をまとめて**日本語で**説明してください。"


async def main():
    async with MCPServerStdio(params=mcp_params) as server:
        agent.mcp_servers = [server]
        result = await Runner.run(agent, msg, run_config=run_config)
        print(result.final_output)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.TimeoutError:
        print("操作がタイムアウトしました")
    except Exception as e:
        print("予期せぬエラーが発生しました: %s", e)
