from py2neo import Graph

try:
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "DinoPythons3000"))
    result = graph.run("RETURN 'Conexión exitosa' AS mensaje").data()
    print(result)
except Exception as e:
    print("Error al conectar con Neo4j:")
    print(e)