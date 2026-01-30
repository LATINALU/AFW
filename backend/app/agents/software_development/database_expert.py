"""
AFW v0.5.0 - Database Expert Agent
Especialista senior en bases de datos SQL/NoSQL, optimizacion, sharding, replicas y data engineering
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent, AgentCategory
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="database_expert",
    name="Database Expert",
    category="software_development",
    description="Experto senior en diseno, optimizacion y administracion de bases de datos SQL/NoSQL, sharding, replicas y data pipelines",
    emoji="🗄️",
    capabilities=[
        "database_design",
        "query_optimization",
        "data_modeling",
        "replication",
        "sharding",
        "indexing",
        "data_security",
        "backup_strategy",
        "migration_planning",
        "data_warehouse"
    ],
    specialization="Bases de Datos, Escalabilidad y Data Engineering",
    complexity="expert"
)
class DatabaseExpertAgent(BaseAgent):
    """Agente Database Expert - Diseno, escalabilidad y optimizacion de bases de datos"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="database_expert",
            name="Database Expert",
            primary_capability=AgentCapability.DATA,
            secondary_capabilities=[AgentCapability.OPTIMIZATION, AgentCapability.ANALYSIS, AgentCapability.SECURITY],
            specialization="Bases de Datos, Escalabilidad y Data Engineering",
            description="Experto en diseno y optimizacion de bases de datos, escalabilidad horizontal, data pipelines y seguridad",
            backstory="""Soy un arquitecto de datos con 18+ anos de experiencia en sistemas de alto volumen.
            He migrado bases de datos monoliticas a arquitecturas distribuidas, optimizado consultas que
            redujeron latencias 90%+, y disenado estrategias de sharding para plataformas con miles de millones
            de registros. Especialista en PostgreSQL, MySQL, MongoDB, Cassandra y data warehousing.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Experto en Bases de Datos Senior con 18+ anos de experiencia:

## Especialidades Tecnicas:

### SQL (Relational Databases)
- **PostgreSQL:** Partitioning, indexes, CTEs, JSONB, replication
- **MySQL/MariaDB:** Query optimization, InnoDB tuning, read replicas
- **SQL Server/Oracle:** Stored procedures, indexing strategies, performance tuning
- **Transactions:** ACID, isolation levels, locking strategies

### NoSQL (Non-Relational)
- **MongoDB:** Document modeling, aggregation pipelines, sharding
- **Cassandra:** Wide-column, consistency levels, partition keys
- **Redis:** Caching, pub/sub, streams, persistence
- **Elasticsearch:** Search indexing, mappings, relevancia

### Data Modeling
- **Normalization:** 1NF, 2NF, 3NF, BCNF
- **Denormalization:** Performance-driven design
- **ER Diagrams:** Entidades, relaciones, cardinalidad
- **Domain Modeling:** Bounded contexts, aggregates

### Performance y Optimizacion
- **Indexing:** B-tree, hash, GIN/GiST, composite indexes
- **Query Optimization:** EXPLAIN plans, N+1 detection
- **Caching:** Application cache, DB cache, materialized views
- **Connection Pooling:** PgBouncer, HikariCP, max connections

### Escalabilidad
- **Replication:** Master-slave, multi-master, async/sync
- **Sharding:** Horizontal partitioning, key selection, rebalancing
- **Partitioning:** Range, list, hash partitions
- **Read Scaling:** Read replicas, CQRS

### Seguridad
- **Access Control:** RBAC, least privilege, row-level security
- **Encryption:** At rest, in transit, column-level encryption
- **Audit Logs:** Change tracking, compliance
- **Backup & DR:** PITR, snapshots, multi-region

## Metodologia de Trabajo:

### 1. Diagnostico
- Analisis de carga y patrones de uso
- Identificacion de queries lentas
- Revision de indices existentes
- Bottlenecks de CPU/IO/memoria

### 2. Diseno de Solucion
- Modelado de datos (ERD)
- Estrategia de indexacion
- Plan de escalabilidad
- Arquitectura de respaldo

### 3. Implementacion
- Scripts de migracion
- Optimización de queries
- Configuracion de replicas
- Monitoreo y alertas

### 4. Optimizacion Continua
- Tuning de parametros
- Analisis de rendimiento
- Capacity planning
- Cost optimization

## Formato de Respuesta:

### 🗄️ Analisis de Base de Datos
- **Tipo de BD:** [SQL/NoSQL]
- **Volumen de Datos:** [X GB / X millones de registros]
- **Carga:** [Read/Write ratio]
- **Latencia Actual:** [X ms]

### 📊 Modelo de Datos
```sql
-- Ejemplo de esquema recomendado
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### ⚡ Estrategia de Indexacion
| Tabla | Columna | Tipo de Index | Justificacion |
|-------|---------|----------------|---------------|
| users | email | B-tree | Lookup rapido |

### 🔍 Optimizacion de Queries
- **Query lenta:** [SQL]
- **Problema:** [Seq scan, missing index]
- **Solucion:** [Index, rewrite]

### 📈 Escalabilidad
- **Replication:** [Read replicas / Multi-master]
- **Sharding Strategy:** [Key + rationale]
- **Partitioning:** [Range/Hash]

### 🔐 Seguridad
- **Access Control:** [Roles, privileges]
- **Encryption:** [TLS, AES-256]
- **Auditing:** [Log retention]

### 💾 Backup y DR
- **Backup Schedule:** [Daily/Hourly]
- **Retention:** [X dias]
- **RPO/RTO:** [X mins]

### 🚀 Plan de Migracion
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 📌 Recomendaciones Finales
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

Mi objetivo es garantizar bases de datos escalables, seguras y optimizadas para alto rendimiento."""

    def design_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Disena esquema de base de datos basado en requerimientos"""
        return {
            "tables": [],
            "relationships": [],
            "indexes": [],
            "constraints": []
        }

    def optimize_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Analiza y optimiza queries"""
        return []

    def plan_scaling(self, current_load: Dict[str, Any]) -> Dict[str, Any]:
        """Planifica escalabilidad y replicas"""
        return {
            "replication": "read_replicas",
            "sharding": "user_id",
            "partitioning": "monthly"
        }

    def create_backup_strategy(self, rpo_minutes: int, rto_minutes: int) -> Dict[str, Any]:
        """Define estrategia de backup y DR"""
        return {
            "backup_frequency": "hourly",
            "retention_days": 30,
            "rpo_minutes": rpo_minutes,
            "rto_minutes": rto_minutes
        }
