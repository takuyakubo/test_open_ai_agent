from pydantic import BaseModel
from agents import Agent, handoff
from agents import Runner

from agents import (
    output_guardrail,
    GuardrailFunctionOutput,
)
MAX_TOKENS = 3000

@output_guardrail
async def length_guardrail(ctx, agent, response):
    token_len = ctx.usage.output_tokens          # 応答分だけ見る
    return GuardrailFunctionOutput(
        output_info={"token_len": token_len},
        tripwire_triggered=token_len > MAX_TOKENS,
    )

class Review(BaseModel):
    verdict: str          # "approve" | "revise"
    strengths: list[str]
    weaknesses: list[str]
    improve_points: str

class Article(BaseModel):
    content: str
    title: str

writer_agent = Agent(
    name="WriterAgent",
    instructions=(
        "あなたは熟練ブロガーです。受け取ったTOPICで "
        "見出し(H1)＋導入＋3〜5のH2構成＋まとめ箇条書き "
        "を含むMarkdown記事(800–1000語)を書いてください。"
        "書き上がったら、そのままユーザーに渡さず,reviewerに渡してください。"
        "reviewerがrejectした場合、その内容を吟味して訂正しまたreviewerに提出してください。"
    ),
    output_type=Article,
    output_guardrails=[length_guardrail],
)

reviewer_agent = Agent(
    name="ReviewerAgent",
    instructions=(
        "記事 ARTICLE を受け取り、以下JSONで返答:\n"
        "verdict ('approve'/'revise'), strengths[], weaknesses[], "
        "improve_points(修正時のみどこを改善すべきか指摘すること)"
        "1万人の読者に堪えるように厳しいレビューをすること"
    ),
    output_type=Review,
)
write_tool   = writer_agent.as_tool(
    tool_name="write_article",
    tool_description="トピックから記事を生成、または修正案を反映して書き直す"
)
review_tool  = reviewer_agent.as_tool(
    tool_name="review_article",
    tool_description="記事を校正し、approve / revise を判定"
)

orchestrator_agent = Agent(
    name="Orchestrator",
    instructions=(
        "ステップ:\n"
        "1. write_article を呼んで草稿を作る。\n"
        "2. review_article に渡して判定させる。\n"
        "3. verdict='revise' なら improved_article を write_article へ再入力。\n"
        "4. verdict='approve' になったら final_article をユーザーへ返す。\n"
        "このループは最大 5 回まで。"
    ),
    tools=[write_tool, review_tool],
    output_type=str,
)