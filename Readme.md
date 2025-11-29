# AgentsCapstoneProject

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
