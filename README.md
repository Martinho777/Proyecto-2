
# Sistema de Recomendación de Ejercicios

Este proyecto implementa un sistema de recomendación de ejercicios usando *Neo4j* como base de datos, *Cypher* como lenguaje de consulta, y *Flask (Python)* como backend para recibir las solicitudes de los usuarios.

##  Objetivo

El sistema genera una rutina de ejercicios personalizada para cada usuario, basada en:
•⁠  ⁠Los *grupos musculares* que desea entrenar (máximo 3).
•⁠  ⁠El *nivel de entrenamiento* del usuario ("Principiante", "Intermedio", o "Avanzado").

El sistema recomienda ejercicios de forma ordenada, priorizando los *ejercicios compuestos* sobre los *aislados*, y limita la cantidad de ejercicios dependiendo del nivel del usuario.

---

##  Modelo de Datos (Nodos y Relaciones en Neo4j)

###  Nodos

•⁠  ⁠⁠ Ejercicio ⁠
•⁠  ⁠⁠ GrupoMuscular ⁠
•⁠  ⁠⁠ SubMusculo ⁠
•⁠  ⁠⁠ Usuario ⁠
•⁠  ⁠⁠ Tipo ⁠
•⁠  ⁠⁠ Nivel ⁠

### 🔗 Relaciones

| Relación          | Desde              | Hacia            |
|-------------------|-------------------|------------------|
| ⁠ ACTIVA_PRIMARIO ⁠ | Ejercicio         | SubMusculo       |
| ⁠ ACTIVA_SECUNDARIA ⁠ | Ejercicio       | SubMusculo       |
| ⁠ ES_TIPO ⁠         | Ejercicio         | Tipo             |
| ⁠ PERTENECE_A ⁠     | SubMusculo        | GrupoMuscular    |
| ⁠ REQUIERE_NIVELL ⁠ | Ejercicio         | Nivel            |

---

## Información de Referencia

###  Grupos Musculares

•⁠  ⁠"Espalda"
•⁠  ⁠"Pecho"
•⁠  ⁠"Hombros"
•⁠  ⁠"Brazos"
•⁠  ⁠"Antebrazo"
•⁠  ⁠"Core"
•⁠  ⁠"Pierna"

###  SubMúsculos

•⁠  ⁠"Dorsal ancho"
•⁠  ⁠"Trapecio"
•⁠  ⁠"Romboides"
•⁠  ⁠"Erectores espinales"
•⁠  ⁠"Pectoral mayor"
•⁠  ⁠"Pectoral superior"
•⁠  ⁠"Pectoral inferior"
•⁠  ⁠"Deltoide anterior"
•⁠  ⁠"Deltoide medio"
•⁠  ⁠"Deltoide posterior"
•⁠  ⁠"Bíceps braquial"
•⁠  ⁠"Tríceps braquial"
•⁠  ⁠"Braquial anterior"
•⁠  ⁠"Flexores del antebrazo"
•⁠  ⁠"Extensores del antebrazo"
•⁠  ⁠"Recto abdominal"
•⁠  ⁠"Oblicuos externos"
•⁠  ⁠"Oblicuos internos"
•⁠  ⁠"Transverso abdominal"
•⁠  ⁠"Cuádriceps"
•⁠  ⁠"Isquiotibiales"
•⁠  ⁠"Glúteo mayor"
•⁠  ⁠"Glúteo medio"
•⁠  ⁠"Aductores"
•⁠  ⁠"Abductores"
•⁠  ⁠"Soleo"
•⁠  ⁠"Gastrocnemio"

###  Niveles de Usuario

•⁠  ⁠"Principiante"
•⁠  ⁠"Intermedio"
•⁠  ⁠"Avanzado"

###  Tipos de Ejercicio

•⁠  ⁠"Aislado"
•⁠  ⁠"Compuesto"

---

## Lógica de Recomendación (Query Cypher)

El sistema recibe:
•⁠  ⁠Un *array de grupos musculares* (mínimo 1, máximo 3).
•⁠  ⁠Un *string de nivel de usuario*.

El algoritmo:
1.⁠ ⁠Filtra los ejercicios según el *nivel* del usuario.
2.⁠ ⁠Filtra los ejercicios por *submúsculos relacionados* con los *grupos musculares seleccionados*.
3.⁠ ⁠Ordena los ejercicios: primero los *compuestos, luego los **aislados*.
4.⁠ ⁠Limita la cantidad de ejercicios:
   - "Principiante" → hasta 4 ejercicios.
   - "Intermedio" → hasta 6 ejercicios.
   - "Avanzado" → hasta 8 ejercicios.

---

Ejemplo de solicitud esperada en el backend:
```json
{
  "gruposMusculares": ["Espalda", "Pecho"],
  "nivelUsuario": "Intermedio"
}