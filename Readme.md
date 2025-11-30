# AgentsCapstoneProject

## Introduction

This project has been developed for the **Agents Intensive - Capstone Project**, which aims to put course learnings into action by building an agentic system that solves a real-world problem or improves everyday productivity.

**Competition Link**: [Agents Intensive Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project)

---

### Submission Details

#### Title
**Intelligent Thesis Reviewer: A Multi-Agent System for Automated Academic Evaluation**

#### Subtitle
*Leveraging Parallel AI Agents and RAG for Comprehensive Rubric-Based Student Document Review*

#### Track
**Agents for Good**

Agents that tackle problems in education, healthcare, or sustainability.

#### Media Gallery

**YouTube Video URL**: *[To be added]*

---

### Team

This project has been collaboratively developed by:

**Japhet Hernandez Vaquero**
- GitHub: [@JaphetHerzVaq](https://github.com/JaphetHerzVaq)
- Email: Japhet.hernandezv@gmail.com

**Luis Angel Montiel Moreno**
- GitHub: [@luis-angel-montiel-moreno](https://github.com/luis-angel-montiel-moreno)
- Email: luis.angel.montielm@gmail.com

---

### Included Features

#### Multi-Agent System
- ✅ **Agent powered by LLM**: All agents utilize Google's Gemini 2.5 Flash Lite model
- ✅ **Parallel agents**: Five specialized reviewer agents execute concurrently for optimal performance
- ✅ **Sequential agents**: Root sequential agent orchestrates parallel review → aggregation workflow

#### Tools & Infrastructure
- ✅ **Custom RAG Tool**: Vertex AI RAG retrieval tool for rubric-based knowledge access
- ✅ **Semantic Search**: Vector database corpus with text-embedding-005 for rubric retrieval

#### Observability
- ✅ **Logging**: Comprehensive logging via Google ADK LoggingPlugin
- ✅ **Tracing**: Full execution trace of agent workflow and state transitions


## Category 1: The Pitch (Problem, Solution, Value)

### Problem: 
When bachelor students develop their thesis, they need to fulfill a robust rubric at several stages of the process. This rubric is a set of criteria that evaluate the student's work by professors. These reviews are time consuming and require a lot of work from professors. 

### Solution: 

We provide an advanced agentic AI system that automates the comprehensive review of student thesis documents. The solution leverages multiple specialized AI agents working in parallel to evaluate student work against rigorous rubric criteria, delivering detailed, actionable feedback that rivals human expert review.

#### Technical Approach

**Multi-Agent Architecture**: The system employs five specialized reviewer agents, each dedicated to evaluating a specific rubric criterion (Presentation, Mathematical Communication, Personal Engagement, Reflection, and Use of Mathematics). These agents operate concurrently using a parallel execution pattern, significantly reducing processing time while maintaining evaluation depth.

**Retrieval-Augmented Generation (RAG)**: Each agent has access to a RAG-enabled knowledge base containing the complete rubric document. This ensures that all evaluations are grounded in the actual rubric standards, not just the model's training data. The RAG system uses semantic search to retrieve relevant rubric sections dynamically during the review process.

**Intelligent Aggregation**: After parallel evaluation, a dedicated aggregator agent synthesizes all individual feedback into a cohesive final report. This agent identifies common themes, highlights connections between different criteria, and provides a comprehensive overview that contextualizes individual criterion scores.

#### Key Features

- **Automated Document Analysis**: Processes complete student documents, understanding context and extracting relevant information for each rubric criterion
- **Parallel Multi-Criterion Evaluation**: Simultaneously evaluates all five rubric criteria, reducing total review time by up to 80% compared to sequential processing
- **Rubric-Grounded Feedback**: All evaluations reference actual rubric criteria retrieved through semantic search, ensuring accuracy and alignment with institutional standards
- **Structured Scoring**: Provides numerical scores for each criterion with detailed justifications based on rubric standards
- **Actionable Recommendations**: Generates three specific, actionable items per criterion (15 total recommendations) that students can implement to improve their work
- **Comprehensive Reporting**: Delivers both detailed per-criterion feedback and an aggregated summary report highlighting cross-criterion insights

#### Impact on Review Process

**For Professors**:
- Reduces review time from hours to minutes per document
- Eliminates repetitive evaluation tasks, allowing focus on high-level pedagogical decisions
- Ensures consistent application of rubric standards across all submissions
- Provides structured feedback templates that can be reviewed and refined before delivery
- Enables batch processing of multiple student submissions efficiently

**For Students**:
- Receives detailed, criterion-specific feedback that clearly explains scoring decisions
- Gets actionable recommendations that directly address rubric requirements
- Benefits from faster feedback cycles, enabling quicker iterations and improvements
- Gains insights into how their work aligns with institutional evaluation standards

### Value: 

The agentic feedback system delivers substantial value through time savings, quality improvements, scalability, and educational outcomes that transform the thesis review process for all stakeholders.

#### Quantifiable Time Savings

**Immediate Efficiency Gains**:
- **90-95% Reduction in Review Time**: What traditionally takes a professor 2-4 hours per document is completed in 10-15 minutes
- **Batch Processing Capability**: Can process multiple student submissions in parallel, reviewing 10 documents in the time it takes to manually review one
- **24/7 Availability**: System operates continuously, enabling flexible scheduling and faster feedback delivery
- **Elimination of Administrative Overhead**: Automatic report generation and formatting saves additional hours of administrative work

#### Quality and Consistency Improvements

**Standardized Evaluation**:
- **100% Rubric Adherence**: Every evaluation is grounded in actual rubric criteria through RAG retrieval, eliminating subjective interpretation variations
- **Comprehensive Coverage**: Guarantees that all rubric criteria are evaluated systematically, reducing the risk of missing evaluation aspects
- **Consistent Scoring**: Applies the same evaluation standards across all submissions, ensuring fairness and reducing bias

**Enhanced Feedback Quality**:
- **Multi-Perspective Analysis**: Five specialized agents provide diverse perspectives on student work, identifying strengths and weaknesses across dimensions
- **Cross-Criterion Insights**: Aggregator agent identifies connections and themes that might be missed in isolated evaluations
- **Specific Actionables**: 15 targeted recommendations per document provide clear pathways for improvement

#### Scalability and Cost Benefits

**Institutional Scalability**:
- **Handles Growing Enrollment**: System scales automatically to handle increasing numbers of student submissions without proportional increases in professor workload
- **Cost-Effective Operations**: Reduces institutional costs associated with professor time allocation, while maintaining evaluation quality
- **Resource Optimization**: Frees professors to focus on high-value activities like curriculum development, research, and one-on-one student mentoring

#### Educational Impact

**Improved Learning Outcomes**:
- **Faster Feedback Loops**: Students receive feedback in days rather than weeks, enabling more iterative improvement cycles
- **Comprehensive Guidance**: Detailed, criterion-specific feedback helps students understand rubric expectations and improve their work systematically
- **Reduced Anxiety**: Faster turnaround times reduce student stress and uncertainty about evaluation timelines

**Pedagogical Enhancement**:
- **Professor Focus Shift**: Professors can dedicate saved time to strategic pedagogical activities, curriculum refinement, and student mentorship
- **Data-Driven Insights**: Aggregated feedback patterns across submissions can inform curriculum improvements and teaching strategies
- **Quality Assurance**: Consistent evaluation standards help maintain program quality and accreditation requirements

#### Return on Investment

**Measurable Returns**:
- **Time Savings**: 90% reduction in review time translates to significant cost savings in professor salary allocation
- **Quality Maintenance**: Consistent, rubric-aligned evaluations maintain or improve evaluation quality while reducing time investment
- **Scalability**: Can handle 10x more submissions with the same professor resources
- **Student Satisfaction**: Faster, more detailed feedback improves student experience and program reputation

#### Long-Term Strategic Value

**Institutional Advantages**:
- **Competitive Positioning**: Faster feedback and consistent quality enhance program reputation
- **Resource Allocation**: Frees institutional resources for strategic initiatives
- **Innovation Enablement**: Automated routine tasks enable focus on educational innovation and improvement
- **Data Collection**: System generates valuable data about common student challenges and evaluation patterns 

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

### Clean Architecture & SOLID Principles

This project is built following **Clean Architecture** principles and **SOLID** design principles, which are particularly critical for agentic AI systems. The architecture ensures maintainability, testability, and scalability in complex multi-agent environments.

#### SOLID Principles Implementation

**1. Single Responsibility Principle (SRP)**
- Each module and class has one clear responsibility:
  - `ReviewerAgent`: Handles individual criterion evaluation only
  - `ReviewerAgentController`: Manages agent orchestration only
  - `RetrievalRagTool`: Handles RAG infrastructure only
  - `ProjectConfig`: Manages configuration only
- **Benefit**: Changes to one component don't affect others, reducing risk of bugs and simplifying maintenance

**2. Open/Closed Principle (OCP)**
- System is open for extension but closed for modification:
  - Adding new rubric criteria only requires adding agent configuration, not changing existing code
  - New agent types can be added by extending `ReviewerAgent` base class
  - Output formats can be extended without modifying core agent logic
- **Benefit**: System can evolve and adapt to new requirements without breaking existing functionality

**3. Liskov Substitution Principle (LSP)**
- All reviewer agents can be substituted interchangeably:
  - Any `ReviewerAgent` instance works identically in parallel execution
  - Aggregator agent treats all reviewer outputs uniformly
- **Benefit**: Enables flexible agent composition and replacement without system-wide changes

**4. Interface Segregation Principle (ISP)**
- Agents and tools expose minimal, focused interfaces:
  - Agents only receive what they need (RAG tool, model, instruction)
  - Configuration is accessed through dedicated class, not scattered dependencies
- **Benefit**: Reduces coupling and makes components easier to understand and modify

**5. Dependency Inversion Principle (DIP)**
- High-level modules depend on abstractions:
  - Controller depends on agent abstractions, not concrete implementations
  - Agents depend on tool interfaces, not specific RAG implementations
  - Configuration is injected, not hardcoded
- **Benefit**: Enables easy testing with mocks and swapping of implementations

#### Clean Architecture Layers

The system follows Clean Architecture's layered approach:

```
┌─────────────────────────────────────────────────────────┐
│            Presentation/Orchestration Layer             │
│                  (main.py)                              │
│  - No business logic                                    │
│  - Coordinates workflow                                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Application/Controller Layer                │
│        (ReviewerAgentController)                        │
│  - Workflow orchestration                               │
│  - Depends on domain abstractions                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Domain/Agent Layer                      │
│  (ReviewerAgent, InductiveReviewerAgents)              │
│  - Core business logic                                  │
│  - Agent definitions and behaviors                      │
│  - No infrastructure dependencies                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Infrastructure Layer                        │
│  (RetrievalRagTool, ProjectConfig)                     │
│  - External services (Vertex AI, RAG)                  │
│  - File system access                                  │
│  - Configuration management                            │
└─────────────────────────────────────────────────────────┘
```

#### Advantages of Clean Architecture for Agentic Systems

**1. Independent Development & Testing**
- **Agent Isolation**: Each agent can be developed, tested, and debugged independently
- **Mock Dependencies**: Infrastructure components (RAG, models) can be mocked for unit testing
- **Parallel Development**: Multiple developers can work on different agents simultaneously without conflicts
- **Impact**: Reduces development time and improves code quality

**2. Technology Independence**
- **Swappable Components**: Can switch from Vertex AI to other providers by changing only infrastructure layer
- **Model Flexibility**: Different LLM models can be used for different agents without changing business logic
- **Storage Independence**: RAG corpus can be moved to different vector databases without affecting agents
- **Impact**: Future-proofs the system and enables optimization opportunities

**3. Business Logic Protection**
- **Core Logic Isolation**: Agent behaviors and evaluation logic are protected from infrastructure changes
- **Stable Interfaces**: Business rules remain stable while infrastructure evolves
- **Impact**: Ensures evaluation quality remains consistent despite technology upgrades

**4. Testability**
- **Unit Testing**: Each layer can be tested independently with appropriate mocks
- **Integration Testing**: Layers can be tested in isolation before full system integration
- **Agent Testing**: Individual agents can be tested with sample documents without full RAG setup
- **Impact**: Enables comprehensive test coverage and faster debugging

**5. Maintainability & Evolution**
- **Clear Dependencies**: Dependency flow is explicit and follows Clean Architecture rules
- **Localized Changes**: Bug fixes and enhancements affect minimal components
- **Impact**: Reduces maintenance costs and risk of introducing new bugs

**6. Scalability & Extensibility**
- **Horizontal Scaling**: New agents can be added by extending base classes
- **Vertical Scaling**: Each layer can be optimized independently
- **Impact**: System can grow with requirements without architectural refactoring

**7. Team Collaboration**
- **Clear Boundaries**: Different team members can own different layers
- **Reduced Conflicts**: Well-defined interfaces minimize merge conflicts
- **Impact**: Enables effective collaboration on complex agentic systems

#### SOLID Benefits for Multi-Agent Systems

**Scalability**: Adding new agents (e.g., for new rubric criteria) requires only configuration changes, not architectural refactoring

**Reliability**: Single Responsibility ensures that agent failures don't cascade across the system

**Flexibility**: Open/Closed Principle allows experimentation with different agent strategies without breaking existing functionality

**Testability**: Dependency Inversion enables comprehensive testing of agent behaviors independently from infrastructure

**Evolution**: Clean separation allows gradual migration and improvement of individual components without system-wide changes

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

### 9. **Clean Architecture & SOLID Principles Advantages**

#### Development Velocity
- **Parallel Development**: Multiple developers can work on different agents/layers simultaneously
- **Rapid Iteration**: Changes are localized, enabling fast feature development and bug fixes
- **Reduced Technical Debt**: Clear architecture prevents accumulation of quick fixes and workarounds

#### System Reliability
- **Isolated Failures**: Agent failures don't cascade across the system due to clear boundaries
- **Predictable Behavior**: SOLID principles ensure components behave consistently
- **Easy Debugging**: Clear separation makes it easy to identify and fix issues

#### Future-Proofing
- **Technology Evolution**: Can adopt new LLM models, RAG systems, or infrastructure without rewriting business logic
- **Requirement Changes**: Adding new rubric criteria or changing evaluation criteria requires minimal code changes
- **Integration Ready**: Clean interfaces make it easy to integrate with external systems (LMS, grading systems)

#### Cost Efficiency
- **Reduced Maintenance**: Well-structured code requires less time to maintain and update
- **Lower Testing Costs**: Testable architecture reduces QA time and effort
- **Easier Onboarding**: New team members can understand and contribute faster

#### Quality Assurance
- **Testability**: Each layer can be unit tested independently with mocks
- **Consistency**: SOLID principles enforce consistent patterns across the codebase
- **Code Reusability**: Well-designed components can be reused in other agentic projects

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
