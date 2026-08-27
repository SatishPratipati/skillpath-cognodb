import os
from neo4j import GraphDatabase


class GraphDatabaseError(Exception):
    pass


class GraphService:
    def __init__(self):
        uri = os.getenv("COGNODB_URI")
        username = os.getenv("COGNODB_USERNAME", "cognodb")
        password = os.getenv("COGNODB_PASSWORD")

        if not uri or not password:
            raise GraphDatabaseError(
                "CognoDB credentials are not configured. Check your .env file."
            )

        try:
            self.driver = GraphDatabase.driver(
                uri,
                auth=(username, password)
            )
            self.driver.verify_connectivity()
        except Exception as exc:
            raise GraphDatabaseError(
                "Unable to reach CognoDB. Check the instance status and connection settings."
            ) from exc

    def close(self):
        if getattr(self, "driver", None):
            self.driver.close()

    def explore_skill(self, skill):
        query = """
        MATCH (s:Skill)
        WHERE toLower(s.name) = toLower($skill)

        OPTIONAL MATCH (s)-[:RELATED_TO]-(related:Skill)
        OPTIONAL MATCH (s)<-[:REQUIRES]-(role:Role)
        OPTIONAL MATCH (s)<-[:USES]-(project:Project)-[:USES]->(tech:Technology)

        RETURN s.name AS skill,
               collect(DISTINCT related.name) AS related_skills,
               collect(DISTINCT role.name) AS roles,
               collect(DISTINCT project.name) AS projects,
               collect(DISTINCT tech.name) AS technologies
        """

        try:
            with self.driver.session() as session:
                record = session.run(
                    query,
                    skill=skill
                ).single()

                if not record or not record["skill"]:
                    return None

                return dict(record)

        except Exception as exc:
            raise GraphDatabaseError(
                "The graph query could not be completed."
            ) from exc

        finally:
            self.close()

    def find_career_path(self, start, role):
        query = """
        MATCH (start:Skill), (target:Role)
        WHERE toLower(start.name) = toLower($start)
          AND toLower(target.name) = toLower($role)

        MATCH p = shortestPath(
            (start)-[:RELATED_TO|REQUIRES*1..5]-(target)
        )

        RETURN [n IN nodes(p) | coalesce(n.name, n.title)] AS path,
               length(p) AS hops
        ORDER BY hops
        LIMIT 1
        """

        try:
            with self.driver.session() as session:
                record = session.run(
                    query,
                    start=start,
                    role=role
                ).single()

                if not record:
                    return None

                return {
                    "path": record["path"],
                    "hops": record["hops"]
                }

        except Exception as exc:
            raise GraphDatabaseError(
                "The career-path query could not be completed."
            ) from exc

        finally:
            self.close()