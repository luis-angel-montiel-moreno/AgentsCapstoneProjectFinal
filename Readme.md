# AgentsCapstoneProject

## Category 1: The Pitch (Problem, Solution, Value)

### Problem: 
When bachelor students develop their thesis, they need to fulfill a robust rubric at several stages of the process. This rubric is a set of criteria that evaluate the student's work by professors. These reviews are time consuming and require a lot of work from professors. 

### Solution: 
We provide a agentic system that helps professors to review students' work automatically, by providing as input the rubric criterias and the student's work. This system uses agentic AI to provide a feedback to the professor, including a score and a list of actionables that the student can take to improve their work. Finally, the system provides a final score based on the rubric criteria and a summary final feedback report.

### Value: 
This system provides a time saving solution for professors, by automating the review process and providing a final score and a summary final feedback report. It also provides a list of actionables that the student can take to improve their work. 

## Architecture

### System Overview

The system follows a hierarchical agent architecture that processes student documents through multiple specialized agents, ultimately generating comprehensive feedback reports. The architecture is designed for scalability, maintainability, and efficient parallel processing.

### Architectural Components

#### 1. **Orchestration Layer** (`main.py`)
- **Entry Point**: Coordinates the entire feedback generation workflow
- **Responsibilities**:
  - Loads student documents and configuration
  - Initializes the agent runner with logging plugins
  - Executes the agent workflow asynchronously
  - Extracts and consolidates feedback from all agents
  - Writes final reports to output files

#### 2. **Controller Layer** (`ReviewerAgentController`)
- **Pattern**: Controller Pattern
- **Responsibilities**:
  - Orchestrates agent initialization and composition
  - Creates the root sequential agent workflow
  - Manages the high-level execution flow: Parallel Review → Aggregation

#### 3. **Agent Layer**

##### 3.1 Base Agent Model (`ReviewerAgent`)
- **Pattern**: Template Method Pattern
- **Purpose**: Base class defining common structure for all reviewer agents
- **Responsibilities**:
  - Provides standardized instruction format
  - Defines output handling structure
  - Ensures consistent behavior across all reviewer agents

##### 3.2 Inductive Agent Model (`InductiveReviewerAgents`)
- **Pattern**: Factory Pattern + Composition Pattern
- **Purpose**: Creates and organizes reviewer agents into execution teams
- **Components**:
  - **Individual Reviewer Agents**: One agent per rubric criterion (A, B, C, D, E)
    - `PresentationReviewerAgent` (Criterion A)
    - `MathComReviewerAgent` (Criterion B)
    - `PersEngReviewerAgent` (Criterion C)
    - `ReflectionReviewerAgent` (Criterion D)
    - `UseMathReviewerAgent` (Criterion E)
  - **Parallel Feedback Team**: Executes all reviewer agents concurrently
  - **Aggregator Agent**: Synthesizes individual feedback into final report

#### 4. **RAG (Retrieval-Augmented Generation) Layer** (`RetrievalRagTool`)
- **Purpose**: Provides agents with access to rubric criteria
- **Technology**: Vertex AI RAG infrastructure
- **Components**:
  - Vector database corpus for rubric storage
  - Semantic search capabilities using text-embedding-005
  - Retrieval tool accessible by all reviewer agents

#### 5. **Configuration Layer** (`ProjectConfig`)
- **Purpose**: Centralizes all configuration settings
- **Contains**: File paths, project identifiers, and system constants

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    main.py (Orchestration)                  │
│  - Document Loading                                          │
│  - Runner Initialization                                     │
│  - Workflow Execution                                        │
│  - Result Extraction & Consolidation                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          ReviewerAgentController (Controller)               │
│  - Root Agent Composition                                    │
│  - Sequential Workflow Definition                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────────────┐   ┌──────────────────────────────┐
│  SequentialAgent      │   │  RetrievalRagTool            │
│  (FeedbackSystem)     │   │  - Corpus Creation           │
│                       │   │  - PDF Ingestion             │
│  Step 1: Parallel     │   │  - Semantic Search           │
│  Step 2: Aggregate    │   └──────────────────────────────┘
└───────┬───────────────┘               │
        │                               │
        │  ┌────────────────────────────┘
        │  │
        ▼  ▼
┌─────────────────────────────────────────────────────────────┐
│      ParallelAgent (ParallelFeedbackTeamAgent)              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │ Agent A  │ Agent B  │ Agent C  │ Agent D  │ Agent E  │  │
│  │(Reviewer)│(Reviewer)│(Reviewer)│(Reviewer)│(Reviewer)│  │
│  │          │          │          │          │          │  │
│  │  [RAG]   │  [RAG]   │  [RAG]   │  [RAG]   │  [RAG]   │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│                                                              │
│  All agents execute in parallel for optimal performance      │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ (Individual Feedback)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│     Agent (ParallelReviewersAggregatorAgent)                │
│  - Receives feedback from all reviewer agents               │
│  - Identifies common themes                                 │
│  - Highlights connections between criteria                  │
│  - Generates final consolidated report                      │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns Used

1. **Controller Pattern**: `ReviewerAgentController` centralizes orchestration logic
2. **Factory Pattern**: `InductiveReviewerAgents` creates agent instances dynamically
3. **Template Method Pattern**: `ReviewerAgent` base class defines common structure
4. **Composition Pattern**: Agents are composed into parallel and sequential workflows
5. **Singleton Pattern**: Root agent is stored as a class variable for global access

### Execution Flow

1. **Initialization Phase**:
   - Load configuration and environment variables
   - Initialize RAG corpus and upload rubric PDF
   - Create RAG retrieval tool
   - Instantiate all reviewer agents with RAG access
   - Compose agents into parallel team
   - Create aggregator agent
   - Compose root sequential agent

2. **Execution Phase**:
   - Load student document
   - Construct task prompt
   - Execute parallel reviewer team (all agents run concurrently)
   - Execute aggregator agent (synthesizes all feedback)
   - Extract feedback from all agents

3. **Consolidation Phase**:
   - Format individual feedback per criterion
   - Include aggregated final summary
   - Write consolidated report to output file

## Advantages

### 1. **Time Efficiency**
- **Parallel Processing**: All reviewer agents execute simultaneously, reducing total execution time from sequential sum to parallel maximum
- **Automated Workflow**: Eliminates manual review steps, saving hours of professor time per document
- **Consistent Output**: Structured feedback generation reduces time spent on formatting and organization

### 2. **Scalability and Maintainability**
- **Modular Architecture**: Each component (agents, RAG, configuration) is independently maintainable
- **Easy Extension**: Adding new rubric criteria requires minimal code changes (just add agent configuration)
- **Separation of Concerns**: Clear boundaries between orchestration, agent logic, and data access

### 3. **Accuracy and Consistency**
- **RAG-Enhanced Evaluations**: Agents ground their feedback in actual rubric criteria retrieved from the corpus
- **Standardized Criteria**: All agents use the same rubric source, ensuring consistent evaluation standards
- **Retry Mechanisms**: Built-in retry logic handles API failures gracefully, improving system reliability

### 4. **Comprehensive Feedback**
- **Multi-Dimensional Analysis**: Each criterion is evaluated by a specialized agent with focused expertise
- **Detailed Actionables**: Each agent provides 3 specific, actionable recommendations for improvement
- **Aggregated Insights**: The aggregator identifies cross-criterion themes and connections

### 5. **Flexibility**
- **Adaptable Rubrics**: Changing rubric criteria only requires updating the PDF - no code changes needed
- **Configurable Models**: Easy to switch LLM models or adjust parameters
- **Extensible Output**: Output format can be customized without changing core logic

### 6. **Cost-Effective**
- **Efficient Resource Usage**: Parallel execution optimizes API call timing
- **Reduced Professor Workload**: Frees professors to focus on higher-level pedagogical tasks
- **Scalable Infrastructure**: Uses managed Vertex AI services that scale automatically

### 7. **Developer Experience**
- **Clear Structure**: Well-organized codebase with clear module boundaries
- **Comprehensive Documentation**: Extensive comments explain architecture and design decisions
- **Error Handling**: Graceful error handling with informative messages

### 8. **Student Benefits**
- **Detailed Feedback**: Students receive comprehensive feedback on all rubric criteria
- **Actionable Recommendations**: Specific, actionable items help students improve their work
- **Faster Turnaround**: Automated reviews enable faster feedback cycles

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Create a Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install Requirements

Install all required packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

To verify that all packages have been installed correctly, run:

```bash
pip list
```

You should see the following packages listed:
- google-adk
- load-dotenv
- vertexai

### Step 5: Configure Google Cloud Credentials

This project uses Vertex AI, which requires Google Cloud authentication.

1. **Install the Google Cloud SDK (gcloud):**
   Follow the instructions here: https://cloud.google.com/sdk/docs/install

2. **Authenticate:**
   Run the following command and follow the browser prompts:
   ```bash
   gcloud auth application-default login
   ```
   This sets up the Application Default Credentials (ADC) needed by the Python client libraries.

## Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```
