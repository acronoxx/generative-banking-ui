# UI AI Natives — Generative Banking UI

## Overview

**UI AI Natives** is a team project exploring how AI agents and generative user interfaces can improve the way users interact with banking services.

The project aims to build a banking assistant that understands natural-language requests, selects appropriate tools, retrieves relevant information, and presents results through a dynamic and user-friendly interface.

The prototype will use synthetic banking data and simulated operations. It is intended for experimentation and demonstration, not for handling real financial transactions.

## Objectives

- Explore AI-agent architectures and tool calling.
- Build a conversational interface connected to banking services.
- Generate or adapt UI components according to the user's request.
- Separate the frontend, backend, AI orchestration, and data layers.
- Evaluate the integration, security, reliability, and maintainability of an AI-native application.

## Main Use Cases

### 1. Spending Analysis

Users can ask questions such as:

- "How much did I spend on restaurants this month?"
- "Summarize my expenses by category."
- "Compare my spending with the previous month."

The assistant retrieves relevant synthetic transaction data and presents summaries or visualizations.

### 2. Account Information

Users can request a summary of their simulated accounts, balances, and recent transactions.

### 3. Transfer Simulation

Users can request a simulated bank transfer. The system should validate the request and display the operation details before any confirmation step.

**No real transfer will be executed.**

### 4. Banking Product Information

Users can explore simulated banking products or services, such as travel insurance, and review relevant information through a conversational interface.

### 5. Contact an Advisor

The assistant can help users identify the appropriate type of support and display a simulated contact or appointment workflow.

## Planned Architecture

The architecture is modular and may evolve as the project progresses.

- **Frontend:** React-based interface and generative UI components.
- **Backend API:** Python and FastAPI for HTTP endpoints, request validation, and coordination with banking services.
- **AI Agent:** An isolated agent component responsible for natural-language interpretation, orchestration, and tool calling.
- **Data Layer:** Synthetic banking data, with PostgreSQL as the planned database.
- **Testing and Quality:** Automated tests, input validation, logging, and code-quality checks.

The frontend communicates with the backend through defined API contracts. The backend and AI-agent components will be integrated through an agreed interface.

Technologies and protocols such as Function Calling, WebMCP, A2UI, and AG-UI may be evaluated as part of the project. Their final use will depend on the architecture and implementation choices.

## Repository Structure

The repository structure will evolve as the components are implemented.

```text
generative-banking-ui/
├── backend/
│   ├── app/
│   └── tests/
├── docs/
├── .gitignore
├── README.md
└── requirements.txt
```

The AI-agent and frontend code may be maintained in dedicated directories or modules, depending on the team's final organization.

## Getting Started

### Prerequisites

- Git
- Python 3.11 or a compatible version supported by the project dependencies
- Visual Studio Code or another Python-compatible IDE

Check your Python installation:

```bash
python --version
```

### 1. Clone the repository

```bash
git clone <https://github.com/acronoxx/generative-banking-ui.git>
cd generative-banking-ui
```


### 2. Create a virtual environment

**Windows — PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

With the virtual environment activated:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `requirements.txt` file lists the Python packages required by the project.

### 4. Verify the environment

```bash
python -m pip check
```

This checks for dependency conflicts. Individual components may require additional configuration as development progresses.

## Development Guidelines

- Keep `main` stable and integrate reviewed changes through pull requests.
- Create a dedicated feature branch for each assigned component.
- Keep API contracts and integration decisions documented.
- Add tests for new functionality.
- Never commit secrets, API keys, passwords, or local environment files.
- Use synthetic data only; do not use real customer or account information.

## Project Status

**Current phase:** Initial setup and architecture definition.

Features described in this README are planned use cases and should not be considered implemented until the corresponding code and tests are available.

## License

To be defined.
