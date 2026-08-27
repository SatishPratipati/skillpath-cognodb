# SkillPath — Graph-Powered Career Explorer

SkillPath is a web application backed by **CognoDB**, a managed openCypher graph database. It helps users explore how skills connect to technologies, projects, and career roles.

## Why a graph database?

The useful questions in SkillPath are about **connections** rather than isolated records.

For example:

- Which roles require a particular skill?
- Which projects use that skill?
- Which technologies are used by those projects?
- What skills can lead toward a target career role?
- What is the shortest connection between a starting skill and a target role?

A relational design would require several join tables and increasingly complex multi-table joins for these traversals. A graph model represents these connections directly as relationships and makes multi-hop traversal natural.

The career-path query is especially graph-native because it searches for a shortest path across multiple relationship types rather than relying on a fixed sequence of relational joins.

## Data Model

```text
(:Skill)-[:RELATED_TO]->(:Skill)

(:Role)-[:REQUIRES]->(:Skill)

(:Project)-[:USES]->(:Skill)

(:Project)-[:USES]->(:Technology)