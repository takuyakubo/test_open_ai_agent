from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

translater_instruction = "あなたは{lang}語の専門家です。翻訳をお願いされるので、{lang}語に翻訳して下さい。".format

spanish_agent = Agent(
    name="spanish_agent", instructions=translater_instruction(lang="スペイン")
)

french_agent = Agent(
    name="french_agent", instructions=translater_instruction(lang="フランス")
)

italian_agent = Agent(
    name="italian_agent", instructions=translater_instruction(lang="イタリア")
)

tool_description = "ユーザーのメッセージを{lang}語に翻訳して下さい".format
manager_agent = Agent(
    name="manager_agent",
    instructions=(
        "あなたは翻訳エージェントです。 与えられたツールを使って翻訳をして下さい。"
        "もし複数語に翻訳することを指示された場合は, 関連するツールを順に使って答えて下さい。"
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description=tool_description(lang="スペイン"),
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description=tool_description(lang="フランス"),
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description=tool_description(lang="イタリア"),
        ),
    ],
)


async def main():
    msg = "「こんにちは」をスペイン語、フランス語、イタリア語に翻訳して下さい。"
    orchestrator_output = await Runner.run(manager_agent, input=msg)
    for message in orchestrator_output.new_items:
        print(f"  -- 翻訳 step: {message.raw_item}")

    print()
    print(orchestrator_output.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# =>  -- 翻訳 step: ResponseFunctionToolCall(arguments='{"input":"こんにちは"}', call_id='call_Js9RqaxV1hzlaU8qtKitIETb', name='translate_to_spanish', type='function_call', id='fc_***7846', status='completed')
# =>  -- 翻訳 step: ResponseFunctionToolCall(arguments='{"input":"こんにちは"}', call_id='call_ME3p2wz***UmR92Gp5u', name='translate_to_french', type='function_call', id='fc_***77846', status='completed')
# =>  -- 翻訳 step: ResponseFunctionToolCall(arguments='{"input":"こんにちは"}', call_id='call_5yrzo3W***ZzGJUuw', name='translate_to_italian', type='function_call', id='fc_s***846', status='completed')
# =>  -- 翻訳 step: {'call_id': 'call_Js9R***itIETb', 'output': 'Hola', 'type': 'function_call_output'}
# =>  -- 翻訳 step: {'call_id': 'call_ME3p2wz***UmR92Gp5u', 'output': 'Bonjour', 'type': 'function_call_output'}
# =>  -- 翻訳 step: {'call_id': 'call_5yrzo3W***ZzGJUuw', 'output': 'こんにちは', 'type': 'function_call_output'}
# =>  -- 翻訳 step: ResponseOutputMessage(id='msg_***7846', content=[ResponseOutputText(annotations=[], text='「こんにちは」は以下のように翻訳されます：\n\n- スペイン語: Hola\n- フランス語: Bonjour\n- イタリア語: Ciao', type='output_text')], role='assistant', status='completed', type='message')
# =>
# => 「こんにちは」は以下のように翻訳されます：
# =>
# => - スペイン語: Hola
# => - フランス語: Bonjour
# => - イタリア語: Ciao
