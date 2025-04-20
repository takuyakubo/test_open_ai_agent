from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class ChurnDetectionOutput(BaseModel):
    is_churn_risk: bool
    reasoning: str


# Agentの定義
churn_detection_agent = Agent(
    name="Churn Detection Agent",
    instructions="メッセージからその顧客が解約するリスクがあるかを判断して下さい。",
    output_type=ChurnDetectionOutput,
)


# ガードレールの定義
@input_guardrail
async def churn_detection_tripwire(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # ここで入力を検査し、解約リスクを検出する
    result = await Runner.run(churn_detection_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_churn_risk,
    )


# メインのAgentにガードレールを適用
customer_support_agent = Agent(
    name="Customer support agent",
    instructions="あなたはカスタマーサービスの顧客対応エージェントです。お客様が質問されるのでその質問に答えて下さい。",
    input_guardrails=[churn_detection_tripwire],
)


# 実行例
async def main():
    # 通常のメッセージはパス
    msg = "こんにちは！"
    output = await Runner.run(customer_support_agent, msg)
    print("挨拶のメッセージはそのまま答えられます。")
    print(f"質問: {msg}")
    print(f"回答: {output.final_output}")

    # 解約の意思を示すメッセージは捕捉される
    try:
        msg = "サブスクリプションのキャンセルをお願いしたいのですが。"
        output = await Runner.run(customer_support_agent, msg)
        print("ガードレールが機能しませんでした。 - これは異常系です。")
        print(f"質問: {msg}")
        print(f"回答: {output.final_output}")
    except InputGuardrailTripwireTriggered:
        print("解約検知ガードレールが機能しました。")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# => 挨拶のメッセージはそのまま答えられます。
# => 質問: こんにちは！
# => 回答: こんにちは！どのようにお手伝いできますか？
# => 解約検知ガードレールが機能しました。
