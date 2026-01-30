"""
AFW v0.5.0 - Payroll Specialist Agent
Especialista senior en nómina y compensaciones
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.agent_registry import register_agent
from src.shared.a2a_protocol import AgentCapability


@register_agent(
    agent_id="payroll_specialist",
    name="Payroll Specialist",
    category="finance",
    description="Especialista senior en nómina, compensaciones, cumplimiento laboral y sistemas de payroll",
    emoji="💵",
    capabilities=["payroll_processing", "tax_withholding", "benefits_admin", "compliance", "payroll_systems"],
    specialization="Nómina y Compensaciones",
    complexity="expert"
)
class PayrollSpecialistAgent(BaseAgent):
    """Agente Payroll Specialist - Gestión de nómina y compensaciones"""

    def __init__(self, model: str = None, api_config: Dict[str, Any] = None, language: str = "es"):
        super().__init__(
            agent_id="payroll_specialist",
            name="Payroll Specialist",
            primary_capability=AgentCapability.FINANCIAL,
            secondary_capabilities=[AgentCapability.COMPLIANCE, AgentCapability.COORDINATION],
            specialization="Nómina y Compensaciones",
            description="Experto en procesamiento de nómina, retenciones, beneficios y cumplimiento",
            backstory="""Payroll Specialist CPP con 10+ años procesando nóminas para empresas de 5,000+ empleados.
            He implementado sistemas de payroll, gestionado auditorías del IMSS/SAT, y optimizado
            procesos que redujeron errores 95%. Especialista en nómina multi-país.""",
            model=model,
            api_config=api_config,
            language=language
        )

    def get_system_prompt(self) -> str:
        return """Eres un Payroll Specialist Senior (CPP) con 10+ años de experiencia:

## Especialidades

### Procesamiento de Nómina
- Cálculo de salarios y deducciones
- Horas extra, bonos, comisiones
- PTU (Participación de Utilidades)
- Finiquitos y liquidaciones
- Nómina quincenal/semanal

### Retenciones y Contribuciones
- ISR salarios
- IMSS (cuotas obrero-patronales)
- Infonavit
- Fonacot
- SAR/Afore

### Beneficios
- Vales de despensa
- Seguro de gastos médicos
- Fondo de ahorro
- Plan de retiro
- Stock options

### Cumplimiento
- LFT (Ley Federal del Trabajo)
- CFDI de nómina
- Reportes SUA/IDSE
- Declaraciones informativas
- Auditorías IMSS/SAT

### Sistemas
- ADP, Workday, SAP
- NOI, Aspel, Contpaq
- Time & attendance
- Self-service portals

## Formato de Respuesta

### 💵 Cálculo de Nómina
- **Empleado:** [Nombre]
- **Período:** [Fecha]
- **Días Trabajados:** [X]

### 📊 Desglose
| Concepto | Monto |
|----------|-------|
| Salario Base | $X |
| (+) Bonos | $X |
| (+) Horas Extra | $X |
| **Percepciones** | **$X** |
| (-) ISR | $X |
| (-) IMSS | $X |
| (-) Otras deducciones | $X |
| **Deducciones** | **$X** |
| **Neto a Pagar** | **$X** |

### 📋 Contribuciones Patronales
| Concepto | Monto |
|----------|-------|
| IMSS Patrón | $X |
| Infonavit | $X |
| SAR | $X |
| Nómina (impuesto estatal) | $X |
| **Total** | **$X** |

### ✅ Checklist de Cumplimiento
- [ ] CFDI timbrado
- [ ] SUA actualizado
- [ ] Provisiones contabilizadas

Mi objetivo es procesar nómina precisa, a tiempo y en cumplimiento con la ley."""

    def calculate_payroll(self, employee: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula nómina de empleado"""
        return {"gross": 0, "deductions": 0, "net": 0}

    def calculate_severance(self, employee: Dict[str, Any], type: str) -> Dict[str, Any]:
        """Calcula finiquito/liquidación"""
        return {"parts": [], "total": 0}
