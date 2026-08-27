import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME", "cognodb")
PASSWORD = os.getenv("COGNODB_PASSWORD")

if not URI or not PASSWORD:
    raise SystemExit("Set COGNODB_URI and COGNODB_PASSWORD first.")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
driver.verify_connectivity()

skills = [
    "Python", "SQL", "Django", "Pandas", "Machine Learning",
    "Data Modeling", "APIs", "Docker", "Git", "JavaScript",
    "Statistics", "ETL"
]

technologies = [
    "PostgreSQL", "Redis", "Airflow", "FastAPI",
    "NumPy", "scikit-learn", "AWS"
]

roles = [
    "Backend Developer",
    "Data Engineer",
    "ML Engineer",
    "Full Stack Developer"
]

projects = [
    ("E-commerce API", ["Python", "Django", "PostgreSQL", "Docker"]),
    ("Spam Classifier", ["Python", "Machine Learning", "Pandas", "scikit-learn"]),
    ("Analytics Pipeline", ["Python", "SQL", "ETL", "Airflow"]),
    ("Recommendation API", ["Python", "APIs", "FastAPI", "Redis"]),
    ("Customer Dashboard", ["Python", "SQL", "JavaScript", "PostgreSQL"]),
]


def write(tx, query, params=None):
    tx.run(query, params or {}).consume()


def seed(tx):

    # Clear existing graph
    write(tx, """
        MATCH (n)
        DETACH DELETE n
        RETURN count(*) AS deleted
    """)

    # Skills
    for name in skills:
        write(tx, """
            CREATE (:Skill {name: $name})
            RETURN 1 AS created
        """, {"name": name})

    # Technologies
    for name in technologies:
        write(tx, """
            CREATE (:Technology {name: $name})
            RETURN 1 AS created
        """, {"name": name})

    # Roles
    for name in roles:
        write(tx, """
            CREATE (:Role {name: $name})
            RETURN 1 AS created
        """, {"name": name})

    # Projects
    for name, items in projects:

        write(tx, """
            CREATE (:Project {name: $name})
            RETURN 1 AS created
        """, {"name": name})

        write(tx, """
            MATCH (p:Project {name: $project_name})
            MATCH (t:Technology)
            WHERE t.name IN $items
            CREATE (p)-[:USES]->(t)
            RETURN count(*) AS created
        """, {
            "project_name": name,
            "items": items
        })

        write(tx, """
            MATCH (p:Project {name: $project_name})
            MATCH (s:Skill)
            WHERE s.name IN $items
            CREATE (p)-[:USES]->(s)
            RETURN count(*) AS created
        """, {
            "project_name": name,
            "items": items
        })

    # Skill-to-skill relationships
    related = [
        ("Python", "Pandas"),
        ("Python", "Django"),
        ("Python", "Machine Learning"),
        ("Python", "APIs"),
        ("SQL", "Data Modeling"),
        ("SQL", "ETL"),
        ("Machine Learning", "Statistics"),
        ("Machine Learning", "Pandas"),
        ("Django", "APIs"),
        ("Docker", "Git"),
        ("ETL", "Airflow"),
        ("JavaScript", "APIs")
    ]

    for a, b in related:
        write(tx, """
            MATCH (a:Skill {name: $a})
            MATCH (b:Skill {name: $b})
            CREATE (a)-[:RELATED_TO]->(b)
            RETURN 1 AS created
        """, {"a": a, "b": b})

    # Role requirements
    role_skills = {
        "Backend Developer": [
            "Python", "Django", "APIs", "SQL", "Docker"
        ],
        "Data Engineer": [
            "Python", "SQL", "ETL", "Data Modeling", "Docker"
        ],
        "ML Engineer": [
            "Python", "Machine Learning", "Statistics", "Pandas"
        ],
        "Full Stack Developer": [
            "Python", "Django", "JavaScript", "APIs", "SQL"
        ]
    }

    for role, required_skills in role_skills.items():

        for skill in required_skills:

            write(tx, """
                MATCH (r:Role {name: $role})
                MATCH (s:Skill {name: $skill})
                CREATE (r)-[:REQUIRES]->(s)
                RETURN 1 AS created
            """, {
                "role": role,
                "skill": skill
            })

    # Skill-to-technology relationships
    skill_technology = {
        "Python": ["NumPy", "scikit-learn"],
        "SQL": ["PostgreSQL"],
        "ETL": ["Airflow"],
        "APIs": ["FastAPI"],
        "Django": ["Redis"]
    }

    for skill, techs in skill_technology.items():

        for tech in techs:

            write(tx, """
                MATCH (s:Skill {name: $skill})
                MATCH (t:Technology {name: $tech})
                CREATE (s)-[:LEADS_TO]->(t)
                RETURN 1 AS created
            """, {
                "skill": skill,
                "tech": tech
            })


with driver.session() as session:
    session.execute_write(seed)

driver.close()

print("SkillPath graph seeded successfully.")