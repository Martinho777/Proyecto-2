from py2neo import Graph

# Conexión a Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "DinoPythons3000"))

print("Conexión exitosa a Neo4j.")