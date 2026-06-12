import operator
import os
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Schema for Structured Output
class EvaluationSchema(BaseModel):
    feedback: str = Field(description='Detailed feedback for the essay')
    score: int = Field(description='Score out of 10', ge=0, le=10)

# Graph State
class UPSEState(TypedDict):
    essay: str 
    language_feedback: str 
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str 
    individual_score: Annotated[list[int], operator.add]
    avg_score: float

def build_workflow():
    # Model definition
    model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
    structured_model = model.with_structured_output(EvaluationSchema)

    def evaluate_language(state: UPSEState):
        prompt = f"Evaluate the essay below with professional rigor. Analyze language quality across grammar, vocabulary, sentence structure, and logical flow. Provide detailed feedback in a formal tone, and assign a definitive score out of 10 with justification.\n\n{state['essay']}"
        output = structured_model.invoke(prompt)
        return {'language_feedback': output.feedback, 'individual_score': [output.score]}

    def evaluate_analysis(state: UPSEState):
        prompt = f"Evaluate the essay below with professional rigor. Analyze the depth of its analysis across dimensions such as argument strength, evidence usage, logical coherence, and originality of insight. Provide detailed feedback in a formal tone, and assign a precise score out of 10 with justification.\n\n{state['essay']}"
        output = structured_model.invoke(prompt)
        return {'analysis_feedback': output.feedback, 'individual_score': [output.score]}

    def evaluate_thought(state: UPSEState):
        # Using the refined prompt from your notebook
        prompt = f"You are tasked with rigorously evaluating the following essay. Assess the clarity of thought demonstrated, focusing on logical flow, organization of ideas, precision of expression, and overall coherence. Provide structured feedback that highlights both strengths and weaknesses, and assign a definitive score out of 10 with clear justification.\n\n{state['essay']}"
        output = structured_model.invoke(prompt)
        return {'clarity_feedback': output.feedback, 'individual_score': [output.score]}

    def final_evaluation(state: UPSEState):
        prompt = f"Based on the following feedbacks create a summarized feedback:\nLanguage feedback - {state['language_feedback']}\nDepth of analysis feedback - {state['analysis_feedback']}\nClarity of thought feedback - {state['clarity_feedback']}" 
        overall_feedback = model.invoke(prompt).content
        
        scores = state.get('individual_score', [])
        avg_score = sum(scores) / len(scores) if scores else 0.0

        return {'overall_feedback': overall_feedback, 'avg_score': avg_score}

    # Build Graph
    graph = StateGraph(UPSEState)
    graph.add_node('evaluate_language', evaluate_language)
    graph.add_node('evaluate_analysis', evaluate_analysis)
    graph.add_node('evaluate_thought', evaluate_thought)
    graph.add_node('final_evaluation', final_evaluation)

    # Parallel Fan-out
    graph.add_edge(START, 'evaluate_language')
    graph.add_edge(START, 'evaluate_analysis')
    graph.add_edge(START, 'evaluate_thought')

    # Fan-in
    graph.add_edge('evaluate_language', 'final_evaluation')
    graph.add_edge('evaluate_analysis', 'final_evaluation')
    graph.add_edge('evaluate_thought', 'final_evaluation')
    graph.add_edge('final_evaluation', END)

    return graph.compile()