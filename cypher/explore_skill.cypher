MATCH (s:Skill {name: $skill})
OPTIONAL MATCH (s)-[:RELATED_TO]-(related:Skill)
OPTIONAL MATCH (s)<-[:REQUIRES]-(role:Role)
OPTIONAL MATCH (s)<-[:USES]-(project:Project)-[:USES]->(tech:Technology)
RETURN s.name AS skill,
       collect(DISTINCT related.name) AS related_skills,
       collect(DISTINCT role.name) AS roles,
       collect(DISTINCT project.name) AS projects,
       collect(DISTINCT tech.name) AS technologies
