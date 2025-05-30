from py2neo import Graph
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "DinoPythons3000")


try:
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # Verifica conexión al menos una vez
    graph.run("RETURN 1")
    print("[✔] Conexión exitosa a Neo4j.")
except Exception as e:
    print("[✖] Error conectando a Neo4j:")
    print(e)
    graph = None  # Se puede manejar condicionalmente en otros módulos