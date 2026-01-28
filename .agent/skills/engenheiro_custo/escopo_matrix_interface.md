---
skill_name: "Matriz de Interfaces de Escopo"
agent: engenheiro_custo
category: "Gestão de Escopo"
difficulty: intermediate
version: 1.0.0
---

# Skill: Matriz de Interfaces de Escopo

## Objetivo

Definir e documentar interfaces entre diferentes disciplinas e responsáveis em projetos de construção (cliente, civil, elétrica, mecânica, projeto, etc.).

## Estrutura da Matriz

```
┌──────────┬────────┬────────┬──────────┬──────────┐
│ Interface│ Cliente│ Civil  │ Elétrica │ Mecânica │
├──────────┼────────┼────────┼──────────┼──────────┤
│ Fundações│   F    │   E    │    C     │    C     │
│ Estrutura│   C    │   E    │    C     │    C     │
│ Elétrica │   F    │   C    │    E     │    I     │
│ HVAC     │   F    │   C    │    I     │    E     │
└──────────┴────────┴────────┴──────────┴──────────┘

Legenda:
E = Executa
F = Fornece
C = Coordena
I = Interfaceia
```

## Exemplo de Interfaces Críticas

### Civil x Elétrica
- Furação de lajes para passagem de eletrodutos
- Caixas de passagem embutidas
- Quadros elétricos (espaço e fixação)

### Civil x Mecânica
- Bases de equipamentos
- Aberturas para dutos de ar condicionado
- Drenos de condensado

### Cliente x Empreiteira
- Fornecimento de materiais importados
- Aprovações de projeto
- Liberação de frentes de trabalho

## Outputs Esperados

1. **Matriz de Responsabilidades (RACI)**
2. **Lista de Interfaces Críticas**
3. **Cronograma de Coordenação**

## Referências
- **PMBOK** - Gestão de interfaces
- **ISO 9001** - Gestão da qualidade
