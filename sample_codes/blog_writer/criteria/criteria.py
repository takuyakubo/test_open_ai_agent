from pydantic import BaseModel

class Level(BaseModel):
    score: int
    rule: str

class Criterion(BaseModel):
    name: str
    description: str
    levels: list[Level]

criteria = [
    Criterion(
        name="content_accuracy_reliability",
        description="内容の正確性と信頼性",
        levels=[
            Level(score=1, rule="多くの事実誤認や不正確な情報が含まれており、信頼性に欠ける"),
            Level(score=2, rule="いくつかの誤りがあり、情報源が不明確または不十分"),
            Level(score=3, rule="基本的な事実は正確だが、裏付けとなる情報源や証拠が限定的"),
            Level(score=4, rule="情報が正確で、適切な情報源や証拠によって裏付けられている"),
            Level(score=5, rule="極めて正確な情報が豊富な信頼性の高い情報源と証拠によって裏付けられている")
        ]
    ),
    Criterion(
        name="logical_structure_coherence",
        description="論理構成の一貫性",
        levels=[
            Level(score=1, rule="構成が混乱しており、論理的つながりがほとんど見られない"),
            Level(score=2, rule="部分的に論理的な流れがあるが、全体的に一貫性に欠ける"),
            Level(score=3, rule="基本的な論理構造はあるが、一部のセクション間の接続が弱い"),
            Level(score=4, rule="全体的に一貫した論理構造があり、セクション間の接続も良好"),
            Level(score=5, rule="完全に一貫した論理構造で、各セクションが自然に次のセクションへと導く完璧な流れ")
        ]
    ),
    Criterion(
        name="readability_engagement",
        description="読みやすさとエンゲージメント",
        levels=[
            Level(score=1, rule="文章が難解で、読者の興味を引き付ける要素がほとんどない"),
            Level(score=2, rule="基本的な情報は伝わるが、表現が単調で読者の関心を維持しにくい"),
            Level(score=3, rule="一定の読みやすさがあり、部分的に読者の興味を引く要素がある"),
            Level(score=4, rule="読みやすく流れるような文章で、読者の興味を持続させる要素が適切に配置されている"),
            Level(score=5, rule="非常に読みやすく魅力的な文章で、読者を引き込む要素が効果的に使われている")
        ]
    ),
    Criterion(
        name="seo_optimization_level",
        description="SEO最適化の度合い",
        levels=[
            Level(score=1, rule="SEO要素がほとんど考慮されておらず、検索エンジンでの可視性が極めて低い"),
            Level(score=2, rule="基本的なキーワードは含まれているが、その配置や密度が不適切"),
            Level(score=3, rule="主要なキーワードが適切に含まれ、基本的なSEO要素が考慮されている"),
            Level(score=4, rule="キーワードの適切な配置、メタデータ、見出し構造など、多くのSEO要素が最適化されている"),
            Level(score=5, rule="すべてのSEO要素（キーワード、見出し、メタデータ、内部リンク、ユーザー体験など）が完全に最適化されている")
        ]
    ),
    Criterion(
        name="target_audience_relevance",
        description="ターゲットオーディエンスへの適合性",
        levels=[
            Level(score=1, rule="ターゲットオーディエンスのニーズや関心とほとんど合致していない"),
            Level(score=2, rule="部分的にターゲットオーディエンスに関連する内容だが、多くの部分が不適切"),
            Level(score=3, rule="ターゲットオーディエンスの基本的なニーズに対応しているが、一部のセグメントには不十分"),
            Level(score=4, rule="ターゲットオーディエンスのニーズや関心に適切に対応し、価値ある情報を提供している"),
            Level(score=5, rule="ターゲットオーディエンスの具体的なニーズ、関心、問題点に完全に対応し、特別な洞察や価値を提供している")
        ]
    ),
    Criterion(
        name="grammar_expression_quality",
        description="文法や表現の適切さ",
        levels=[
            Level(score=1, rule="多数の文法ミスや不適切な表現があり、理解を妨げる"),
            Level(score=2, rule="いくつかの文法ミスや不自然な表現があるが、基本的な内容は理解できる"),
            Level(score=3, rule="文法は概ね正確だが、表現の洗練さに欠ける部分がある"),
            Level(score=4, rule="文法的に正確で、適切かつ効果的な表現が使われている"),
            Level(score=5, rule="完璧な文法と洗練された表現で、文体に一貫性があり読み手に強い印象を与える")
        ]
    )
] 