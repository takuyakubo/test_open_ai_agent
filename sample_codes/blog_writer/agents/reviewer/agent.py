from agents import Agent
from ...models.models import create_review_output_model
from ...criteria.criteria import criteria

def get_average_score_from_(review_data):
    total_score = 0
    for k in review_data:
        if not k.endswith("_score"):
            continue
        total_score += review_data[k]
    return total_score / (len(criteria) * 5)

def get_review_result_text_from(review_data, criteria):
    def get_rule(criterion, score):
        for l in criterion.levels:
            if l.score == score:
                return l.rule
        return None

    review_results = ""
    for c in criteria:
        review_results += f"{c.name}({c.description})\n"
        score = review_data[f"{c.name}_score"]
        rule = get_rule(c, score)
        if rule is None:
            review_results += f"  - score: - (測定失敗) \n\n"
            continue
        review_results += f"  - score: {score} ({rule}) \n"
        review_results += f"  - strengths: {review_data[f'{c.name}_strengths']}\n"
        review_results += f"  - weaknesses: {review_data[f'{c.name}_weaknesses']}\n"
        review_results += f"  - suggestions: {review_data[f'{c.name}_suggestions']}\n\n"
    return review_results

def create_review_instruction(criteria):
    instruction = """あなたは高品質なコンテンツ評価の専門家です。記事を客観的に評価し、改善点を特定してください。
    次につながる改善プロセスのために一切の忖度なしで評価してください。

    【評価基準】
    以下の{length_of_criteria}つの観点から、記事を1〜5段階で評価してください（5が最高評価）。
    各項目について具体的な根拠と改善点を詳細に説明してください。
    """.format(length_of_criteria=len(criteria))
    
    for c in criteria:
        instruction += f"\n- {c.name} ({c.description}):\n"
        for l in c.levels:
            instruction += f"  {l.score}: {l.rule}\n"

    instruction += "\n【出力形式】\n各評価項目について以下の形式で評価結果を出力してください：\n\n"
    for c in criteria:
        instruction += f"- {c.name}_score: [1-5の評価]\n"
        instruction += f"- {c.name}_strengths: [強みの具体例]\n"
        instruction += f"- {c.name}_weaknesses: [弱点の具体例]\n"
        instruction += f"- {c.name}_suggestions: [具体的な改善提案]\n"
    return instruction

def create_input_review(article, topic, target, objective, keywords, length, tone):
    return f"""
あなたは高品質なコンテンツ評価の専門家です。記事を客観的に評価し、改善点を特定してください。
次につながる改善プロセスのために一切の忖度なしで評価してください。
【記事】
{article}

なお、記事の条件は以下のとおりです。
【記事の主題】: {topic}
【対象読者】: {target}
【記事の目的】: {objective}
【主要キーワード】: {keywords}
【記事の長さ】: {length}
【トーン】: {tone}
"""

review_instruction = create_review_instruction(criteria)
review_output_format_class = create_review_output_model(criteria)
reviewer = Agent(name="Reviewer", instructions=review_instruction, output_type=review_output_format_class) 