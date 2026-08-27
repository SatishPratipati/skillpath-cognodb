# SkillPath — Graph-Powered Career Explorer

SkillPath is a small web application backed by **CognoDB**, a managed openCypher graph database. It helps users explore how skills connect to technologies, projects, and career roles.

## Why a graph database?

The useful questions in SkillPath are about **connections**: which projects use a skill, which technologies are reached through those projects, and which skills connect to a target role. A relational design would require several join tables and increasingly complex multi-table joins for these traversals. A graph model expresses the same questions directly as paths.

The career-path query is especially graph-native: it searches for a shortest path between a starting skill and a target role across multiple relationship types.

## Data model

```text
(:Skill)-[:RELATED_TO]->(:Skill)
   │
   ├──[:LEADS_TO]──> (:Technology)
   │
   └──<-[REQUIRES]-(:Role)

(:Project)-[:USES]->(:Skill)
(:Project)-[:USES]->(:Technology)
```

## Main graph queries

### 1. Skill exploration
`cypher/explore_skill.cypher` combines multiple relationships around a skill and returns related skills, roles, projects and technologies.

### 2. Multi-hop career path
`cypher/career_path.cypher` finds a shortest path from a starting skill to a target role. This traverses more than one hop and uses graph topology rather than a fixed set of relational joins.

All application queries are parameterized through the official Neo4j Python driver.

## Tech stack

- Python
- Django
- Official Neo4j Python driver
- CognoDB / openCypher
- HTML/CSS

## Run locally

### 1. Create the CognoDB instance

Create a free c0 instance in CognoDB Cloud and keep the generated password private.

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and set:

```text
COGNODB_URI=bolt+s://YOUR_INSTANCE.databases.cognodb.com
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=YOUR_PASSWORD
SECRET_KEY=any-long-random-value
DEBUG=True
```

The repository never contains real credentials.

### 4. Seed the graph

PowerShell:

```powershell
$env:COGNODB_URI="your-uri"
$env:COGNODB_USERNAME="cognodb"
$env:COGNODB_PASSWORD="your-password"
python scripts/seed_database.py
```

Or load the variables using your preferred `.env` workflow.

### 5. Start Django

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Error handling

If CognoDB is unreachable or credentials are missing, the application displays a user-friendly database error instead of exposing connection details or a Python traceback.

## Screenshots

Add final screenshots here after the UI is running:

- Home page
- Skill exploration result
- Career path result

## Project structure

```text
skillpath/
├── explorer/
│   ├── services/graph_service.py
│   ├── templates/
│   └── static/
├── scripts/seed_database.py
├── cypher/
├── skillpath/
├── manage.py
├── requirements.txt
└── README.md
```

## Demo

Add the hosted demo URL here before submission.

## Submission

Repository: add your GitHub URL.

Demo: add your hosted application URL.

Screen recording: add the recording link/file according to the assignment instructions.
