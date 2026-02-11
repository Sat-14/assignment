# Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Educational AI Assistant                      │
│                   (Continuous Learning System)                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      LangGraph Workflow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   Entry     │─────▶│  Retrieve   │─────▶│  Generate   │     │
│  │   Point     │      │  Context    │      │  Response   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                             │                      │             │
│                             │                      │             │
│                             ▼                      ▼             │
│                       ┌──────────┐          ┌──────────┐        │
│                       │ Learned  │          │   LLM    │        │
│                       │ Patterns │          │Generation│        │
│                       └──────────┘          └──────────┘        │
│                                                   │              │
│                                                   ▼              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │     END     │◀─────│   Update    │◀─────│  Collect    │     │
│  │             │      │  Knowledge  │      │  Feedback   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                             │                                    │
│                             ▼                                    │
│                       ┌──────────┐                              │
│                       │Safeguards│                              │
│                       └──────────┘                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Data Flow & Learning                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Question ──────────────────────────────┐                  │
│                                               │                  │
│                                               ▼                  │
│  ┌──────────────────┐              ┌───────────────────┐        │
│  │  Knowledge Base  │◀────────────▶│  State Manager   │        │
│  │  (knowledge.json)│              │   (LangGraph)    │        │
│  └──────────────────┘              └───────────────────┘        │
│         │                                    │                  │
│         │ Contains:                          │                  │
│         │ - Successful responses             ▼                  │
│         │ - User preferences        ┌─────────────────┐         │
│         │ - Feedback history        │   LLM (GPT)     │         │
│         │ - Confidence scores       │   or Mock       │         │
│         │                           └─────────────────┘         │
│         │                                    │                  │
│         │                                    ▼                  │
│         └─────────────────────────────▶ Response                │
│                                             │                   │
│                                             ▼                   │
│                                        User Feedback            │
│                                    (👍 positive / 👎 negative) │
│                                             │                   │
│                                             ▼                   │
│                                    ┌─────────────────┐          │
│                                    │ Update Learning │          │
│                                    │   + Safeguards  │          │
│                                    └─────────────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Learning Mechanism                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Similar Question Detection                                      │
│  ────────────────────────                                        │
│  "How do I submit assignment?" ─┐                               │
│                                  ├─▶ Word overlap matching       │
│  "How do I submit homework?"   ─┘                               │
│                                                                   │
│  Context Injection                                               │
│  ─────────────────                                               │
│  System Prompt + Learned Patterns ──▶ Enhanced Response         │
│                                                                   │
│  Confidence Scoring                                              │
│  ──────────────────                                              │
│  Positive Feedback / Total Feedback = Confidence                 │
│  If Confidence < 30% ──▶ Remove from knowledge base             │
│                                                                   │
│  Data Decay                                                      │
│  ──────────                                                      │
│  Feedback History > 1000 ──▶ Keep only latest 1000              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Component Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               ContinuousLearningAssistant                  │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  - __init__(knowledge_file)                               │  │
│  │  - chat(question, user_id) -> response                    │  │
│  │  - provide_feedback(question, response, feedback)         │  │
│  │  - get_stats() -> dict                                    │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  Private Methods:                                          │  │
│  │  - _load_knowledge()                                      │  │
│  │  - _save_knowledge()                                      │  │
│  │  - _build_graph()                                         │  │
│  │  - _apply_safeguards()                                    │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  Node Methods (LangGraph):                                │  │
│  │  - retrieve_context(state)                                │  │
│  │  - generate_response(state)                               │  │
│  │  - collect_feedback(state)                                │  │
│  │  - update_knowledge(state)                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    State Structure                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  {                                                               │
│    "messages": [],              # Conversation history           │
│    "user_id": "string",         # Current user identifier       │
│    "question": "string",        # User's question               │
│    "response": "string",        # AI's response                 │
│    "feedback": "string",        # "positive" | "negative"       │
│    "learned_patterns": {        # Retrieved context             │
│      "user_preferences": {},                                    │
│      "similar_successful": [],                                  │
│      "total_interactions": int                                  │
│    },                                                            │
│    "confidence_score": float    # Response confidence           │
│  }                                                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Safeguards & Safety                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Confidence Threshold                                         │
│     ───────────────────                                          │
│     • Minimum 30% positive feedback to retain                   │
│     • Requires at least 6 total feedback entries                │
│     • Automatic removal of low-quality patterns                 │
│                                                                   │
│  2. Data Decay                                                   │
│     ──────────                                                   │
│     • Feedback history capped at 1000 entries                   │
│     • Oldest entries removed first (FIFO)                       │
│     • Prevents unbounded memory growth                          │
│                                                                   │
│  3. Traceability                                                 │
│     ─────────────                                                │
│     • All feedback timestamped (ISO 8601)                       │
│     • User ID tracking for audit                                │
│     • JSON format for easy human review                         │
│                                                                   │
│  4. Rollback Capability                                          │
│     ──────────────────                                           │
│     • JSON-based storage = version control friendly             │
│     • Easy to revert to previous states                         │
│     • Manual override capability                                │
│                                                                   │
│  5. Isolation                                                    │
│     ─────────                                                    │
│     • Per-user preferences don't affect others                  │
│     • No cross-user contamination                               │
│     • Privacy-preserving design                                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌────────────────────────────────────────────┐
│          Application Layer                 │
│  ┌──────────────────────────────────────┐  │
│  │  ContinuousLearningAssistant         │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│       Orchestration Layer                  │
│  ┌──────────────────────────────────────┐  │
│  │  LangGraph (StateGraph)              │  │
│  │  - Workflow Management               │  │
│  │  - State Transitions                 │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│          LLM Layer                         │
│  ┌──────────────────────────────────────┐  │
│  │  OpenAI GPT-3.5-turbo (Production)   │  │
│  │  MockLLM (Testing)                   │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│        Persistence Layer                   │
│  ┌──────────────────────────────────────┐  │
│  │  JSON File Storage                   │  │
│  │  - knowledge.json                    │  │
│  │  - Lightweight & Portable            │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

## Deployment Options

```
Development/Testing
├── main_mock.py (No API key required)
└── test_mock.py (Full test suite)

Production
├── main.py (Requires OpenAI API key)
└── .env (API configuration)

Future Scaling
├── Replace JSON with SQLite/PostgreSQL
├── Add Redis for caching
├── Horizontal scaling with load balancer
└── MLOps pipeline for model updates
```
