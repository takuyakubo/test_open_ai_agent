from pydantic import BaseModel, create_model
from typing import Dict, Any

class ArticleOutput(BaseModel):
    article_markdown: str
    improvement_summary: str

class MetaOutput(BaseModel):
    prompt: str
    comment: str
    knowledge: str

def create_review_output_model(criteria: list) -> type:
    output_dict = {}
    for c in criteria:
        output_dict.update({
            f"{c.name}_score": int,
            f"{c.name}_strengths": str,
            f"{c.name}_weaknesses": str,
            f"{c.name}_suggestions": str
        })
    return create_model("ReviewOutput", **output_dict) 