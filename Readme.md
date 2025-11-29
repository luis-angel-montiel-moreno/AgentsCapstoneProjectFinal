# AgentsCapstoneProject

## Category 1: The Pitch (Problem, Solution, Value)

### Problem: 
When bachelor students develop their thesis, they need to fulfill a robust rubric at several stages of the process. This rubric is a set of criteria that evaluate the student's work by professors. These reviews are time consuming and require a lot of work from professors. 

### Solution: 
We provide a agentic system that helps professors to review students' work automatically, by providing as input the rubric criterias and the student's work. This system uses agentic AI to provide a feedback to the professor, including a score and a list of actionables that the student can take to improve their work. Finally, the system provides a final score based on the rubric criteria and a summary final feedback report.

### Value: 
This system provides a time saving solution for professors, by automating the review process and providing a final score and a summary final feedback report. It also provides a list of actionables that the student can take to improve their work. 


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
