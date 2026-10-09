from pydantic import BaseModel, Field
class AnswerSummary(BaseModel):
    answer: str = Field(
        description="The final answer to the user's question."
    )
    tools_used: list[str] = Field(
        default_factory=list,
        description="Names of tools used while answering."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )