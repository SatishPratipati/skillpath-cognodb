MATCH (start:Skill {name: $start}), (target:Role {name: $role})
MATCH p = shortestPath((start)-[:RELATED_TO|REQUIRES*1..5]-(target))
RETURN [n IN nodes(p) | coalesce(n.name, n.title)] AS path,
       length(p) AS hops
ORDER BY hops
LIMIT 1
