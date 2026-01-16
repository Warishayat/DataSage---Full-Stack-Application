from typing_extensions import TypedDict
class GraphState(TypedDict):
    question: str
    context: str
    answer: str