from pydantic import BaseModel, create_model
from agents import Agent, Runner, trace

# definition of criteria {{{
class Level(BaseModel):
    score: int
    rule: str

class Crieterion(BaseModel):
    name: str
    description: str
    levels: list[Level]

criteria = [
    Crieterion(
    name = "content_accuracy_reliability",
    description = "内容の正確性と信頼性",
    levels = [
        Level(score=1, rule="多くの事実誤認や不正確な情報が含まれており、信頼性に欠ける"),
        Level(score=2, rule="いくつかの誤りがあり、情報源が不明確または不十分"),
        Level(score=3, rule="基本的な事実は正確だが、裏付けとなる情報源や証拠が限定的"),
        Level(score=4, rule="情報が正確で、適切な情報源や証拠によって裏付けられている"),
        Level(score=5, rule="極めて正確な情報が豊富な信頼性の高い情報源と証拠によって裏付けられている")
    ]),
    Crieterion(
    name = "logical_structure_coherence",
    description = "論理構成の一貫性",
    levels = [
        Level(score=1, rule="構成が混乱しており、論理的つながりがほとんど見られない"),
        Level(score=2, rule="部分的に論理的な流れがあるが、全体的に一貫性に欠ける"),
        Level(score=3, rule="基本的な論理構造はあるが、一部のセクション間の接続が弱い"),
        Level(score=4, rule="全体的に一貫した論理構造があり、セクション間の接続も良好"),
        Level(score=5, rule="完全に一貫した論理構造で、各セクションが自然に次のセクションへと導く完璧な流れ")
    ]),
    Crieterion(
    name = "readability_engagement",
    description = "読みやすさとエンゲージメント",
    levels = [
        Level(score=1, rule="文章が難解で、読者の興味を引き付ける要素がほとんどない"),
        Level(score=2, rule="基本的な情報は伝わるが、表現が単調で読者の関心を維持しにくい"),
        Level(score=3, rule="一定の読みやすさがあり、部分的に読者の興味を引く要素がある"),
        Level(score=4, rule="読みやすく流れるような文章で、読者の興味を持続させる要素が適切に配置されている"),
        Level(score=5, rule="非常に読みやすく魅力的な文章で、読者を引き込む要素が効果的に使われている")
    ]),
    Crieterion(
    name = "seo_optimization_level",
    description = "SEO最適化の度合い",
    levels = [
        Level(score=1, rule="SEO要素がほとんど考慮されておらず、検索エンジンでの可視性が極めて低い"),
        Level(score=2, rule="基本的なキーワードは含まれているが、その配置や密度が不適切"),
        Level(score=3, rule="主要なキーワードが適切に含まれ、基本的なSEO要素が考慮されている"),
        Level(score=4, rule="キーワードの適切な配置、メタデータ、見出し構造など、多くのSEO要素が最適化されている"),
        Level(score=5, rule="すべてのSEO要素（キーワード、見出し、メタデータ、内部リンク、ユーザー体験など）が完全に最適化されている")
    ]),
    Crieterion(
    name = "target_audience_relevance",
    description = "ターゲットオーディエンスへの適合性",
    levels = [
        Level(score=1, rule="ターゲットオーディエンスのニーズや関心とほとんど合致していない"),
        Level(score=2, rule="部分的にターゲットオーディエンスに関連する内容だが、多くの部分が不適切"),
        Level(score=3, rule="ターゲットオーディエンスの基本的なニーズに対応しているが、一部のセグメントには不十分"),
        Level(score=4, rule="ターゲットオーディエンスのニーズや関心に適切に対応し、価値ある情報を提供している"),
        Level(score=5, rule="ターゲットオーディエンスの具体的なニーズ、関心、問題点に完全に対応し、特別な洞察や価値を提供している")
    ]),
    Crieterion(
    name = "grammar_expression_quality",
    description = "文法や表現の適切さ",
    levels = [
        Level(score=1, rule="多数の文法ミスや不適切な表現があり、理解を妨げる"),
        Level(score=2, rule="いくつかの文法ミスや不自然な表現があるが、基本的な内容は理解できる"),
        Level(score=3, rule="文法は概ね正確だが、表現の洗練さに欠ける部分がある"),
        Level(score=4, rule="文法的に正確で、適切かつ効果的な表現が使われている"),
        Level(score=5, rule="完璧な文法と洗練された表現で、文体に一貫性があり読み手に強い印象を与える")
    ])
]

# definition of criteria }}}

# definition of first writer {{{
class ArticleOutput(BaseModel):
    article_markdown:str
    improvement_summary:str

firstwrite_instruction = """あなたは優れたWebコンテンツライターです。以下の要件に基づいて記事の初稿を生成してください。

- 専門用語は初心者にもわかるように説明する
- 段落は短めに保ち、読みやすさを重視する
- 見出しは検索意図に合わせて作成する
- 文末は能動態を優先し、説得力のある文章にする

出力形式はマークダウン形式で、見出しの階層構造を明確にしてください。

この指示を参考に、読者にとって価値のある、情報量が豊富で魅力的な記事の初稿を作成してください。
現時点では完璧を目指さず、後の評価と改善のプロセスを前提とした基礎となる文章を作成することに集中してください。"""
first_writer = Agent(name="First Writer", instructions=firstwrite_instruction, output_type=ArticleOutput)

input_topic = """
あなたは優れたWebコンテンツライターです。以下の要件に基づいて記事の初稿を生成してください。
【記事の主題】: {topic}
【対象読者】: {target}
【記事の目的】: {objective}
【主要キーワード】: {keywords}
【記事の長さ】: {length}
【トーン】: {tone}
【構成要素】: 
- 導入部（読者の興味を引く書き出し）
- 本文（3〜5つの主要セクションに分ける）
- 具体例や事例を含める
- データや統計を適切に引用する
- 視覚的な要素の提案（図表やイメージの説明）
- まとめと次のアクション
""".format
# definition of first writer }}}

# definition of reviewer {{{
def create_review_instruction_from_(criteria):
    instruction = """あなたは高品質なコンテンツ評価の専門家です。記事を客観的に評価し、改善点を特定してください。
    次につながる改善プロセスのために一切の忖度なしで評価してください。

    【評価基準】
    以下の{length_of_criteria}つの観点から、記事を1〜5段階で評価してください（5が最高評価）。
    各項目について具体的な根拠と改善点を詳細に説明してください。
    """.format(length_of_criteria = len(criteria))
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

def create_review_output_model_from_(criteria):
    output_dict = dict()
    for c in criteria:
        output_dict.update(
            {f"{c.name}_score": int,
            f"{c.name}_strengths": str,
            f"{c.name}_weaknesses": str,
            f"{c.name}_suggestions":str})

    model_name = "ReviewOutPut"
    return create_model(model_name, **output_dict)

review_instruction = create_review_instruction_from_(criteria)
review_output_format_class = create_review_output_model_from_(criteria)

reviewer = Agent(name="Reviewer", instructions=review_instruction, output_type=review_output_format_class)

input_review = """
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
""".format

def get_average_score_from_(review_data):
    # review_data = review_result.final_output.model_dump()
    total_score = 0
    for k in review_data:
        if not k.endswith("_score"):
            continue
        total_score += review_data[k]
    return total_score / (len(criteria) * 5)

def get_review_result_text_from(review_data, criteria):
    # review_data = review_result.final_output.model_dump()
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
        review_results += f"  - strengths: {review_data[f"{c.name}_strengths"]}\n"
        review_results += f"  - weaknesses: {review_data[f"{c.name}_weaknesses"]}\n"
        review_results += f"  - suggestions: {review_data[f"{c.name}_suggestions"]}\n\n"
    return review_results
 # definition of reviewer }}}

 # definition of rewriter {{{
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
input_rewrite = """あなたは優れたコンテンツ編集者兼ライターです。
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
""".format
# definition of rewriter }}}

# definition of prompt_engineer {{{
meta_instruction = """あなたは卓越したプロンプエンジニアです。
これまでの会話をまとめて精度高く最終的な文章を得るためにはどのようなプロンプトを書くべきか示してください。
また、改善するにあって、他の記事制作にも活かせる知見をkowledgeとしてmarkdownにまとめてください。
"""

class MetaOutput(BaseModel):
    prompt:str
    comment:str
    knowledge: str

prompt_engineer = Agent(name="PromptEngineer", instructions=meta_instruction, output_type=MetaOutput)
# definition of prompt_engineer }}}


sample_topic = {
    "topic": "AIのreflection loopに関する紹介",
    "target": "ITエンジニア",
    "objective": "reflection loopを用いた実装のポイント紹介",
    "keywords": "reflection loop, rubric, AI agent",
    "length": "2000文字程度で",
    "tone": "カジュアル"
}

async def reflection_loop(topic, N_max=5):
    w_results = []
    r_results = []
    history = []
    best_idx = -1
    best_score = 0
    base_article = ""
    review_results = ""
    with trace("Create Blog Content"):
        for idx in range(N_max):
            if r_results == []:
                w_input = input_topic(**topic)
                w_result = await Runner.run(first_writer, w_input)
            else:
                w_input = input_rewrite(article=base_article,
                                        review_results=review_results,
                                        **topic)
                w_result = await Runner.run(rewriter, w_input)
            history += w_result.to_input_list()
            w_results.append(w_result)
            base_article = w_result.final_output.article_markdown
            
            r_input = input_review(article=w_result.final_output.article_markdown, **topic)
            r_result = await Runner.run(reviewer, r_input)
            history += r_result.to_input_list()
            r_results.append(r_result)

            review_data = r_result.final_output.model_dump()
            score_ = get_average_score_from_(review_data)
            if best_score < score_:
                best_score = score_
                best_idx = idx
            if score_ >= .9:
                break
            review_results = get_review_result_text_from(review_data, criteria)
    return list(zip(w_results, r_results)), best_idx