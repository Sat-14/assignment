

# Continuous Learning AI Assistant

AI Internship Assignment: Educational SaaS Platform Conversational AI with Continuous Learning

## Overview

A domain-specific conversational AI assistant that learns from user interactions without retraining the base model. Built using LangGraph for orchestration with support for multiple LLM backends (Ollama local models, OpenAI, or mock for testing).

**Three Implementation Options:**
- **Local LLM** (Recommended) - Free, no API key, uses Ollama
- **Cloud LLM** - OpenAI GPT-3.5-turbo for best quality
- **Mock** - Testing version with simulated responses

## What is Continuous Learning?

In this context, continuous learning means the assistant improves over time by:
- Storing successful response patterns based on user feedback
- Building user preference profiles
- Adapting future responses based on historical data
- Maintaining a feedback loop without model fine-tuning

**Key Insight:** The system learns by updating its *retrieval context and prompts*, not by retraining the base model. This enables fast, safe adaptation without expensive model updates.

## Architecture

### Learning Signals Used
1. **Explicit Feedback**: Thumbs up/down on responses
2. **Conversation Outcomes**: Success rate of similar queries
3. **User Preferences**: Per-user interaction history
4. **Pattern Recognition**: Similar questions get similar successful answers

### What Updates Over Time
- **Memory**: Successful response patterns stored in JSON
- **Prompts**: Context injection with learned patterns
- **User Preferences**: Individual user interaction history
- **Response Selection**: Context retrieval based on past success
- **Confidence Scores**: Weighted by positive vs negative feedback

### Safeguards
1. **Confidence Thresholds**: Responses with <30% positive feedback are removed
2. **Data Decay**: Feedback history capped at 1000 entries
3. **Human Review Ready**: All feedback logged with timestamps
4. **Rollback Capable**: JSON-based storage allows easy version control

## LangGraph Implementation

### Graph Flow
```
Entry → retrieve_context → generate_response → collect_feedback → update_knowledge → END
```

### Node Responsibilities
- **retrieve_context**: Loads learned patterns and user preferences from knowledge base
- **generate_response**: Generates AI response with learned context injected into prompt
- **collect_feedback**: Placeholder for feedback capture (extensible for UI integration)
- **update_knowledge**: Stores feedback, updates patterns, and applies safeguards

### Separation of Concerns
- **Core Inference**: LLM generation in `generate_response` node
- **Learning Logic**: Pattern matching and updates in `update_knowledge` node
- **Stored Knowledge**: JSON file with responses, preferences, and feedback history

## Use Cases Implemented

### 1. Response Quality Improvement via Feedback
- Users provide thumbs up/down on responses
- Positive responses are stored and reused for similar questions
- Low-confidence responses are automatically removed
- Confidence scores guide response selection

### 2. Adaptive Recommendations
- Similar questions retrieve previously successful responses
- Context injection improves relevance over time
- User-specific preferences influence response generation
- Pattern matching enables knowledge transfer

## Installation

### Option 1: Local LLM (Recommended - Free & No API Key)

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2

# Install dependencies
pip install -r requirements_local.txt

# Run
python main_local.py
```

**Why Local LLM?**
- ✓ Completely free
- ✓ No API key required
- ✓ Privacy-preserving (data stays local)
- ✓ Works offline
- ✓ Fast responses (no network latency)

See [SETUP_LOCAL.md](SETUP_LOCAL.md) for detailed setup and model options.

### Option 2: OpenAI API

```bash
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_key_here
```

```bash
python main.py
```

### Option 3: Mock (Testing - No LLM Required)

```bash
pip install -r requirements_local.txt

# Run demo
python main_mock.py

# Run tests
python test_mock.py
```

## Usage

### Basic Example (Local LLM)
```python
from main_local import ContinuousLearningAssistant

assistant = ContinuousLearningAssistant()

response = assistant.chat("How do I submit my assignment?", user_id="student1")
print(response)

assistant.provide_feedback(
    "How do I submit my assignment?",
    response,
    "positive",
    user_id="student1"
)

similar_response = assistant.chat("How do I submit homework?", user_id="student2")
print(similar_response)
```

### Basic Example (OpenAI)
```python
from main import ContinuousLearningAssistant

assistant = ContinuousLearningAssistant()
response = assistant.chat("What resources are available?", user_id="student1")
```

### Basic Example (Mock)
```python
from main_mock import ContinuousLearningAssistant

assistant = ContinuousLearningAssistant()
response = assistant.chat("How do I access the platform?", user_id="student1")
```

### Run Demos
```bash
python main_local.py    # Local LLM demo
python main_mock.py     # Mock demo
python main.py          # OpenAI demo (requires API key)
```

### Run Tests
```bash
python test_mock.py     # All 8 tests (recommended)
```

## Evaluation

### Measuring Learning Effectiveness
1. **Feedback Rate**: Ratio of positive to negative feedback
2. **Response Reuse**: How often learned patterns are applied
3. **User Engagement**: Repeated interactions from same users
4. **Confidence Trends**: Average confidence score over time

**Implementation:**
```python
stats = assistant.get_stats()
print(stats)
# {
#   'total_learned_responses': 5,
#   'positive_feedback': 8,
#   'negative_feedback': 2,
#   'unique_users': 3
# }
```

### Risks and Mitigation

**Risk: Response Drift**
- Mitigation: Confidence threshold filtering (30%), human review logs

**Risk: Bias Amplification**
- Mitigation: Per-user preferences prevent global bias, feedback decay

**Risk: Stale Information**
- Mitigation: Timestamp tracking, manual review capability via JSON

**Risk: Privacy**
- Mitigation: User IDs anonymized, no PII stored in responses

**Risk: Memory Bloat**
- Mitigation: 1000 entry cap with FIFO removal

## Key Features

- ✓ LangGraph-based workflow orchestration
- ✓ Multiple LLM backend support (Ollama, OpenAI, Mock)
- ✓ JSON-based lightweight persistence
- ✓ Feedback-driven learning without model retraining
- ✓ Multi-user support with preference tracking
- ✓ Built-in safeguards and confidence scoring
- ✓ Complete test coverage (8 tests)
- ✓ No API key required (local version)
- ✓ Privacy-preserving (local version)

## Files

### Core Implementation
- **main_local.py**: Local LLM version (Ollama) - **Recommended**
- **main_mock.py**: Mock version for testing
- **main.py**: OpenAI API version
- **test_mock.py**: Comprehensive test suite (8 tests)

### Documentation
- **README.md**: This file - technical design and usage
- **ARCHITECTURE.md**: System architecture diagrams
- **PROJECT_SUMMARY.md**: Implementation summary
- **SETUP_LOCAL.md**: Local LLM setup guide
- **QUICKSTART.md**: Quick comparison guide
- **ASSIGNMENT_CHECKLIST.md**: Requirement coverage checklist

### Configuration
- **requirements_local.txt**: Dependencies for local/mock versions
- **requirements.txt**: Full dependencies (includes OpenAI)
- **.env.example**: Environment variable template
- **.gitignore**: Git ignore rules

### Data (Auto-generated)
- **knowledge.json**: Persistent knowledge storage

## Technical Stack

- **Framework**: LangGraph (StateGraph)
- **LLM Options**:
  - Ollama (llama3.2, phi3, gemma2) - Local
  - OpenAI GPT-3.5-turbo - Cloud
  - Mock - Testing
- **Language**: Python 3.8+
- **Persistence**: JSON files
- **State Management**: TypedDict with LangGraph State
- **Dependencies**: LangChain, LangGraph, langchain-community

## Long-term Behavior

The system evolves by:
1. Accumulating successful response patterns
2. Building confidence scores through repeated feedback
3. Pruning low-quality patterns automatically (confidence < 30%)
4. Personalizing per user without affecting others
5. Maintaining traceability through timestamped logs

**Evolution Phases:**
- **Initial Phase** (0-100 interactions): Rapid learning, building knowledge base
- **Stabilization** (100-1000 interactions): Confidence scores stabilize, quality improves
- **Maintenance** (1000+ interactions): Data decay kicks in, steady-state operation

This design balances adaptability with safety, ensuring the assistant improves while preventing harmful drift or bias accumulation.

## Quick Start

```bash
# Fastest: Test the architecture
python test_mock.py

# Best: Real AI, no cost
ollama pull llama3.2
python main_local.py

# Optional: Cloud AI
echo "OPENAI_API_KEY=your_key" > .env
python main.py
```


## License

MIT License - Free for educational use
