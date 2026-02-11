import json
import os
from datetime import datetime
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama

class State(TypedDict):
    messages: list
    user_id: str
    question: str
    response: str
    feedback: str
    learned_patterns: dict
    confidence_score: float

class ContinuousLearningAssistant:
    def __init__(self, knowledge_file="knowledge.json", model="llama3.2"):
        self.knowledge_file = knowledge_file
        self.llm = Ollama(model=model, temperature=0.7)
        self.knowledge = self._load_knowledge()
        self.graph = self._build_graph()

    def _load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        return {
            "successful_responses": {},
            "user_preferences": {},
            "feedback_history": [],
            "learned_patterns": {}
        }

    def _save_knowledge(self):
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)

    def _build_graph(self):
        workflow = StateGraph(State)

        workflow.add_node("retrieve_context", self.retrieve_context)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("collect_feedback", self.collect_feedback)
        workflow.add_node("update_knowledge", self.update_knowledge)

        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("retrieve_context", "generate_response")
        workflow.add_edge("generate_response", "collect_feedback")
        workflow.add_edge("collect_feedback", "update_knowledge")
        workflow.add_edge("update_knowledge", END)

        return workflow.compile()

    def retrieve_context(self, state: State) -> State:
        user_id = state.get("user_id", "default")
        question = state["question"]

        user_prefs = self.knowledge["user_preferences"].get(user_id, {})

        similar_responses = []
        for q, data in self.knowledge["successful_responses"].items():
            if any(word in question.lower() for word in q.lower().split()):
                if data.get("positive_feedback", 0) > data.get("negative_feedback", 0):
                    similar_responses.append(data["response"])

        state["learned_patterns"] = {
            "user_preferences": user_prefs,
            "similar_successful": similar_responses[:3],
            "total_interactions": len(self.knowledge["feedback_history"])
        }

        return state

    def generate_response(self, state: State) -> State:
        question = state["question"]
        learned = state["learned_patterns"]

        context = ""
        if learned["similar_successful"]:
            context = f"\n\nPreviously successful responses to similar questions:\n" + "\n".join(learned["similar_successful"])

        if learned["user_preferences"]:
            context += f"\n\nUser preferences: {learned['user_preferences']}"

        prompt = f"""You are an educational AI assistant helping students on a SaaS platform.
Answer questions, guide navigation, and recommend resources.{context}

Question: {question}

Provide a helpful, concise answer:"""

        response = self.llm.invoke(prompt)
        state["response"] = response
        state["messages"].append({"role": "user", "content": question})
        state["messages"].append({"role": "assistant", "content": response})

        return state

    def collect_feedback(self, state: State) -> State:
        return state

    def update_knowledge(self, state: State) -> State:
        if state.get("feedback"):
            user_id = state.get("user_id", "default")
            question = state["question"]
            response = state["response"]
            feedback = state["feedback"]

            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "question": question,
                "response": response,
                "feedback": feedback
            }
            self.knowledge["feedback_history"].append(feedback_entry)

            if question not in self.knowledge["successful_responses"]:
                self.knowledge["successful_responses"][question] = {
                    "response": response,
                    "positive_feedback": 0,
                    "negative_feedback": 0,
                    "last_updated": datetime.now().isoformat()
                }

            if feedback == "positive":
                self.knowledge["successful_responses"][question]["positive_feedback"] += 1
                self.knowledge["successful_responses"][question]["response"] = response
                self.knowledge["successful_responses"][question]["last_updated"] = datetime.now().isoformat()
            elif feedback == "negative":
                self.knowledge["successful_responses"][question]["negative_feedback"] += 1

            if user_id not in self.knowledge["user_preferences"]:
                self.knowledge["user_preferences"][user_id] = {}

            self._apply_safeguards()
            self._save_knowledge()

        return state

    def _apply_safeguards(self):
        for question, data in list(self.knowledge["successful_responses"].items()):
            total_feedback = data["positive_feedback"] + data["negative_feedback"]
            if total_feedback > 5:
                confidence = data["positive_feedback"] / total_feedback
                if confidence < 0.3:
                    del self.knowledge["successful_responses"][question]

        if len(self.knowledge["feedback_history"]) > 1000:
            self.knowledge["feedback_history"] = self.knowledge["feedback_history"][-1000:]

    def chat(self, question: str, user_id: str = "default") -> str:
        state = {
            "messages": [],
            "user_id": user_id,
            "question": question,
            "response": "",
            "feedback": "",
            "learned_patterns": {},
            "confidence_score": 0.0
        }

        result = self.graph.invoke(state)
        return result["response"]

    def provide_feedback(self, question: str, response: str, feedback: str, user_id: str = "default"):
        state = {
            "messages": [],
            "user_id": user_id,
            "question": question,
            "response": response,
            "feedback": feedback,
            "learned_patterns": {},
            "confidence_score": 0.0
        }

        self.update_knowledge(state)

    def get_stats(self):
        total_responses = len(self.knowledge["successful_responses"])
        total_feedback = len(self.knowledge["feedback_history"])
        positive = sum(1 for f in self.knowledge["feedback_history"] if f["feedback"] == "positive")
        negative = sum(1 for f in self.knowledge["feedback_history"] if f["feedback"] == "negative")

        return {
            "total_learned_responses": total_responses,
            "total_feedback_received": total_feedback,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "unique_users": len(self.knowledge["user_preferences"])
        }

if __name__ == "__main__":
    print("Initializing with local Ollama LLM...")
    assistant = ContinuousLearningAssistant()

    print("=== Educational AI Assistant (Local LLM) ===\n")

    response1 = assistant.chat("How do I submit my assignment?", user_id="student1")
    print(f"Q: How do I submit my assignment?")
    print(f"A: {response1}\n")

    assistant.provide_feedback(
        "How do I submit my assignment?",
        response1,
        "positive",
        user_id="student1"
    )

    response2 = assistant.chat("Where can I find my grades?", user_id="student1")
    print(f"Q: Where can I find my grades?")
    print(f"A: {response2}\n")

    assistant.provide_feedback(
        "Where can I find my grades?",
        response2,
        "positive",
        user_id="student1"
    )

    response3 = assistant.chat("How do I submit homework?", user_id="student2")
    print(f"Q: How do I submit homework?")
    print(f"A: {response3}\n")

    print("Stats:", assistant.get_stats())
