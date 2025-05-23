from agents import Agent
from ...models.models import ArticleOutput

def create_input_rewrite(article, review_results, topic, target, objective, keywords, length, tone):
    return f"""あなたは優れたコンテンツ編集者兼ライターです。
前段階の評価結果に基づいて、記事を効果的に改善してください。
【原稿】
{article}

【評価結果】
{review_results}

なお、記事の条件は以下のとおりです。
【記事の主題】: {topic}
【対象読者】: {target}
【記事の目的】: {objective}
【主要キーワード】: {keywords}
【記事の長さ】: {length}
【トーン】: {tone}
"""

rewrite_instruction = """あなたは優れたコンテンツ編集者兼ライターです。
前段階の評価結果に基づいて、記事を効果的に改善してください。

【改善のアプローチ】
1. 評価結果の分析: まず評価結果を詳細に分析し、優先的に対処すべき問題点を特定してください。
2. 包括的な改善: 単に指摘された問題点を修正するだけでなく、記事全体の質を向上させる視点で改善を行ってください。
3. 強みの維持: 評価で高評価を受けた部分や強みとされた要素は維持・強化してください。
4. バランスの取れた修正: 一部の側面だけを過度に重視するのではなく、評価カテゴリーすべてにおいてバランスの取れた改善を行ってください。

【出力形式】
改善された記事全文をマークダウン形式で出力してください。
記事の改善/変更のサマリーも一緒に提供してください
"""

rewriter = Agent(name="Rewriter", instructions=rewrite_instruction, output_type=ArticleOutput) 