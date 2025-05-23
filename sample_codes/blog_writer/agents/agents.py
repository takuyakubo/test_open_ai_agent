from agents import Agent
from ..models.models import ArticleOutput, MetaOutput, create_review_output_model
from ..criteria.criteria import criteria

# First Writer Agent
firstwrite_instruction = """あなたは優れたWebコンテンツライターです。以下の要件に基づいて記事の初稿を生成してください。

- 専門用語は初心者にもわかるように説明する
- 段落は短めに保ち、読みやすさを重視する
- 見出しは検索意図に合わせて作成する
- 文末は能動態を優先し、説得力のある文章にする

出力形式はマークダウン形式で、見出しの階層構造を明確にしてください。

この指示を参考に、読者にとって価値のある、情報量が豊富で魅力的な記事の初稿を作成してください。
現時点では完璧を目指さず、後の評価と改善のプロセスを前提とした基礎となる文章を作成することに集中してください。"""

first_writer = Agent(name="First Writer", instructions=firstwrite_instruction, output_type=ArticleOutput)

# Reviewer Agent
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

review_instruction = create_review_instruction(criteria)
review_output_format_class = create_review_output_model(criteria)
reviewer = Agent(name="Reviewer", instructions=review_instruction, output_type=review_output_format_class)

# Rewriter Agent
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

# Prompt Engineer Agent
meta_instruction = """あなたは卓越したプロンプエンジニアです。
これまでの会話をまとめて精度高く最終的な文章を得るためにはどのようなプロンプトを書くべきか示してください。
また、改善するにあって、他の記事制作にも活かせる知見をkowledgeとしてmarkdownにまとめてください。
"""

prompt_engineer = Agent(name="PromptEngineer", instructions=meta_instruction, output_type=MetaOutput) 