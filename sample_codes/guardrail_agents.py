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
    instructions="Identify if the user message indicates a potential customer churn risk.",
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
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[churn_detection_tripwire],
)


# 実行例
async def main():
    # 通常のメッセージはパス
    await Runner.run(customer_support_agent, "Hello!")
    print("Hello message passed")

    # 解約の意思を示すメッセージは捕捉される
    try:
        await Runner.run(
            customer_support_agent, "I think I might cancel my subscription"
        )
        print("Guardrail didn't trip - this is unexpected")
    except InputGuardrailTripwireTriggered:
        print("Churn detection guardrail tripped")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
