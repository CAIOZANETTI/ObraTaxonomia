---
skill_name: "NumPy - Computação Vetorial"
agent: tech_lead_data
category: "Data Science"
difficulty: intermediate
version: 1.0.0
---

# Skill: NumPy - Computação Vetorial e Matricial

## Objetivo

Fornecer guia prático de NumPy para operações vetoriais e matriciais eficientes, essenciais para cálculos de engenharia e análise de dados.

## Fundamentos

### 1. Arrays NumPy vs Listas Python

```python
import numpy as np

# Lista Python (lenta, flexível)
lista = [1, 2, 3, 4, 5]
quadrados_lista = [x**2 for x in lista]  # Loop explícito

# Array NumPy (rápido, otimizado)
array = np.array([1, 2, 3, 4, 5])
quadrados_array = array ** 2  # Operação vetorizada (10-100x mais rápido)

print(quadrados_array)  # [1 4 9 16 25]
```

### 2. Criação de Arrays

```python
# Arrays 1D
a = np.array([1, 2, 3])
zeros = np.zeros(5)  # [0. 0. 0. 0. 0.]
ones = np.ones(5)  # [1. 1. 1. 1. 1.]
range_array = np.arange(0, 10, 2)  # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5)  # [0. 0.25 0.5 0.75 1.]

# Arrays 2D (Matrizes)
matriz = np.array([[1, 2, 3],
                   [4, 5, 6]])

zeros_2d = np.zeros((3, 4))  # Matriz 3x4 de zeros
identidade = np.eye(3)  # Matriz identidade 3x3

# Arrays aleatórios
aleatorio = np.random.rand(3, 3)  # Uniforme [0, 1)
normal = np.random.randn(3, 3)  # Normal padrão (μ=0, σ=1)
```

### 3. Operações Vetorizadas

```python
# Cálculo de BDI para múltiplos itens
custos_diretos = np.array([10000, 25000, 50000, 100000])
taxa_bdi = 0.28

# Vetorizado (rápido)
precos_venda = custos_diretos * (1 + taxa_bdi)

# Operações elemento a elemento
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

soma = a + b  # [11 22 33 44]
produto = a * b  # [10 40 90 160]
divisao = b / a  # [10. 10. 10. 10.]
potencia = a ** 2  # [1 4 9 16]
```

### 4. Indexação e Slicing

```python
arr = np.array([10, 20, 30, 40, 50])

# Indexação
print(arr[0])  # 10
print(arr[-1])  # 50

# Slicing
print(arr[1:4])  # [20 30 40]
print(arr[::2])  # [10 30 50] (passo 2)

# Indexação booleana (filtros)
maiores_que_25 = arr[arr > 25]  # [30 40 50]

# Exemplo: Filtrar itens caros
precos = np.array([100, 250, 500, 1000, 50])
itens_caros = precos[precos > 300]  # [500 1000]
```

### 5. Operações Matriciais

```python
# Produto matricial
A = np.array([[1, 2],
              [3, 4]])

B = np.array([[5, 6],
              [7, 8]])

# Produto elemento a elemento
produto_elem = A * B

# Produto matricial (álgebra linear)
produto_mat = A @ B  # ou np.dot(A, B)

# Transposta
A_T = A.T

# Inversa
A_inv = np.linalg.inv(A)

# Determinante
det_A = np.linalg.det(A)

# Autovalores e autovetores
autovalores, autovetores = np.linalg.eig(A)
```

### 6. Estatísticas

```python
dados = np.array([10, 20, 30, 40, 50])

media = np.mean(dados)  # 30.0
mediana = np.median(dados)  # 30.0
desvio_padrao = np.std(dados)  # 14.14
variancia = np.var(dados)  # 200.0
minimo = np.min(dados)  # 10
maximo = np.max(dados)  # 50
soma = np.sum(dados)  # 150

# Estatísticas por eixo (matrizes)
matriz = np.array([[1, 2, 3],
                   [4, 5, 6]])

media_colunas = np.mean(matriz, axis=0)  # [2.5 3.5 4.5]
media_linhas = np.mean(matriz, axis=1)  # [2. 5.]
```

### 7. Broadcasting

```python
# Broadcasting: operações entre arrays de shapes diferentes
a = np.array([[1, 2, 3],
              [4, 5, 6]])  # Shape: (2, 3)

b = np.array([10, 20, 30])  # Shape: (3,)

# NumPy "expande" b para (2, 3) automaticamente
resultado = a + b
# [[11 22 33]
#  [14 25 36]]

# Exemplo prático: Aplicar diferentes taxas de BDI por categoria
custos = np.array([[1000, 2000],
                   [3000, 4000],
                   [5000, 6000]])  # 3 categorias, 2 itens cada

taxas_bdi = np.array([0.25, 0.28, 0.30]).reshape(-1, 1)  # Shape: (3, 1)

precos = custos * (1 + taxas_bdi)  # Broadcasting!
```

### 8. Aplicações em Engenharia

#### Cálculo de Cargas em Estrutura

```python
def calcular_reacoes_viga_simples(carga_kN: float, vao_m: float, posicao_carga_m: float):
    """
    Calcula reações de apoio em viga biapoiada com carga concentrada.
    
    Returns:
        np.array com [R_A, R_B] em kN
    """
    a = posicao_carga_m
    b = vao_m - a
    
    # Matriz de equilíbrio
    A = np.array([[1, 1],          # ΣFy = 0
                  [0, vao_m]])      # ΣM_A = 0
    
    b_vec = np.array([carga_kN, carga_kN * a])
    
    reacoes = np.linalg.solve(A, b_vec)
    
    return reacoes

# Exemplo
R_A, R_B = calcular_reacoes_viga_simples(carga_kN=100, vao_m=6, posicao_carga_m=2)
print(f"R_A = {R_A:.2f} kN, R_B = {R_B:.2f} kN")
```

#### Análise de Custos Vetorizada

```python
def analisar_orcamento_vetorizado(quantidades: np.ndarray, precos_unitarios: np.ndarray, bdi: float = 0.28):
    """
    Analisa orçamento de forma vetorizada (eficiente).
    
    Args:
        quantidades: Array de quantidades
        precos_unitarios: Array de preços unitários
        bdi: Taxa de BDI
    
    Returns:
        dict com análise completa
    """
    custos_diretos = quantidades * precos_unitarios
    custos_com_bdi = custos_diretos * (1 + bdi)
    
    return {
        'custo_direto_total': np.sum(custos_diretos),
        'custo_com_bdi_total': np.sum(custos_com_bdi),
        'custo_medio_item': np.mean(custos_diretos),
        'custo_maximo_item': np.max(custos_diretos),
        'desvio_padrao': np.std(custos_diretos)
    }

# Exemplo
qtds = np.array([100, 50, 200, 30])
precos = np.array([10.5, 25.0, 5.0, 100.0])

resultado = analisar_orcamento_vetorizado(qtds, precos)
```

### 9. Performance

```python
import time

# Comparação: Loop vs Vetorização
n = 1_000_000

# Com loop (lento)
start = time.time()
resultado_loop = []
for i in range(n):
    resultado_loop.append(i ** 2)
tempo_loop = time.time() - start

# Vetorizado (rápido)
start = time.time()
resultado_numpy = np.arange(n) ** 2
tempo_numpy = time.time() - start

print(f"Loop: {tempo_loop:.4f}s")
print(f"NumPy: {tempo_numpy:.4f}s")
print(f"Speedup: {tempo_loop/tempo_numpy:.1f}x")
# Típico: 50-100x mais rápido
```

### 10. Checklist

Ao usar NumPy:

- [ ] Usar arrays NumPy em vez de listas para cálculos
- [ ] Vetorizar operações (evitar loops explícitos)
- [ ] Usar broadcasting quando possível
- [ ] Especificar dtype apropriado (float64, int32, etc.)
- [ ] Usar funções NumPy (np.sum, np.mean) em vez de built-ins
- [ ] Pré-alocar arrays quando tamanho é conhecido
- [ ] Usar views em vez de cópias quando possível

## Referências

- **NumPy Documentation**: https://numpy.org/doc/
- **NumPy for MATLAB Users**: Guia de transição
- **Python Data Science Handbook** (Jake VanderPlas)
