from pydantic import BaseModel
from agents import Agent, Runner, trace


class Review(BaseModel):
    approved: bool
    score_overall: int                # 0–100
    score_logic:   int
    score_style:   int
    score_readability: int            # Textstat
    grammar_errors: int               # LanguageTool
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
        "を含むMarkdown記事(800–1000語)を日本語で書いてください。"
        "reviewerがrejectした場合、その内容を吟味して訂正し再度書き直してください。"
    ),
    output_type=Article,
)

reviewer_agent = Agent(
    name="ReviewerAgent",
    instructions=(
        "あなたはトップジャーナルの査読者並みに厳格です。\n"
        "与えられた Article を以下のルーブリックで評価し、JSON を返してください。\n"
        "採点基準:\n"
        " 1) 論理構成（score_logic）\n"
        " 2) スタイルと語彙の豊かさ（score_style）\n"
        " 3) 可読性（score_readability: Flesch 由来、50 以上なら高評価）\n"
        " 4) 誤字・文法ミス数（grammar_errors が 0 に近いほど高評価）\n"
        "score_overall = (score_logic+score_style+score_readability)/3 で整数化。\n"
        "score_overall が 80 未満なら必ず Re-write を要求し、"
        "improve_points に具体的修正指示を 5 点以上列挙すること。"
    ),
    output_type=Review,
)
inst_rev = """以下の文章をレビューしてください。
タイトル:
{title}
内容：
{content}""".format

inst_rew = """以下のreviewを受けて書き直しをお願いします。
トピック:
{topic}
以前のタイトル:
{title}
以前の内容：
{content}
強み：
{strengths}
弱み:
{weaknesses}
改善点
{improve_points}""".format


async def reflection_loop(topic, N_max=5):
    w_results = []
    r_results = []
    best_idx = -1
    best_score = 0
    with trace("Create Blog Content"):
        for idx in range(N_max):
            if r_results == []:
                w_result = await Runner.run(writer_agent, topic)
            else:
                w_result = await Runner.run(writer_agent, inst_rew(
                    topic=topic,
                    **w_results[-1].final_output.model_dump(),
                    **r_results[-1].final_output.model_dump()))
            r_result = await Runner.run(reviewer_agent, inst_rev(**w_result.final_output.model_dump()))
            w_results.append(w_result)
            r_results.append(r_result)
            score_ = r_result.final_output.score_overall
            if best_score < score_:
                best_score = score_
                best_idx = idx
            if score_ >= 90:
                break
    return list(zip(w_results, r_results)), best_idx