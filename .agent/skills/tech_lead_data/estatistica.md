---
skill_name: "Estatística Aplicada"
agent: tech_lead_data
category: "Data Science"
difficulty: advanced
version: 1.0.0
---

# Skill: Estatística - Distribuições, Regressões e Testes de Hipótese

## Objetivo

Fornecer fundamentos estatísticos para análise de dados de engenharia, previsão de custos e tomada de decisão baseada em dados.

## 1. Estatística Descritiva

```python
import numpy as np
import pandas as pd
from scipy import stats

# Medidas de tendência central
dados = np.array([100, 150, 200, 250, 300])

media = np.mean(dados)  # 200
mediana = np.median(dados)  # 200
moda = stats.mode(dados, keepdims=True)[0][0]

# Medidas de dispersão
variancia = np.var(dados, ddof=1)  # Variância amostral
desvio_padrao = np.std(dados, ddof=1)
coef_variacao = (desvio_padrao / media) * 100  # CV%

# Quartis e percentis
q1 = np.percentile(dados, 25)
q2 = np.percentile(dados, 50)  # = mediana
q3 = np.percentile(dados, 75)
iqr = q3 - q1  # Intervalo interquartil
```

## 2. Distribuições de Probabilidade

### Distribuição Normal

```python
from scipy.stats import norm

# Parâmetros
mu = 100  # Média
sigma = 15  # Desvio padrão

# Probabilidade P(X < 110)
prob = norm.cdf(110, loc=mu, scale=sigma)

# Valor crítico (95% de confiança)
z_critico = norm.ppf(0.975)  # 1.96

# Intervalo de confiança
ic_95 = (mu - z_critico*sigma, mu + z_critico*sigma)

# Exemplo: Prazo de obra com incerteza
prazo_esperado = 180  # dias
desvio = 20

prob_atraso = 1 - norm.cdf(200, loc=prazo_esperado, scale=desvio)
print(f"Probabilidade de atraso > 200 dias: {prob_atraso*100:.2f}%")
```

### Distribuição t de Student

```python
from scipy.stats import t

# Intervalo de confiança com amostra pequena (n < 30)
amostra = np.array([95, 102, 98, 105, 100])
n = len(amostra)
media_amostra = np.mean(amostra)
erro_padrao = stats.sem(amostra)

# t crítico (95% confiança, n-1 graus de liberdade)
t_critico = t.ppf(0.975, df=n-1)

# Intervalo de confiança
margem_erro = t_critico * erro_padrao
ic = (media_amostra - margem_erro, media_amostra + margem_erro)
```

## 3. Regressão Linear

```python
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Dados: Área construída vs Custo
area_m2 = np.array([50, 80, 100, 150, 200, 250])
custo_mil = np.array([150, 240, 300, 450, 600, 750])

# Regressão linear
slope, intercept, r_value, p_value, std_err = linregress(area_m2, custo_mil)

# Equação: Custo = intercept + slope * Área
print(f"Custo = {intercept:.2f} + {slope:.2f} × Área")
print(f"R² = {r_value**2:.4f}")

# Previsão
area_nova = 120
custo_previsto = intercept + slope * area_nova
print(f"Custo previsto para 120m²: R$ {custo_previsto:.2f} mil")

# Intervalo de confiança da previsão
residuos = custo_mil - (intercept + slope * area_m2)
s_residual = np.std(residuos, ddof=2)
erro_previsao = s_residual * np.sqrt(1 + 1/len(area_m2))
ic_previsao = (custo_previsto - 1.96*erro_previsao, 
               custo_previsto + 1.96*erro_previsao)
```

## 4. Testes de Hipótese

### Teste t (Comparação de Médias)

```python
from scipy.stats import ttest_ind, ttest_rel

# Teste t independente (duas amostras)
custos_fornecedor_a = np.array([100, 105, 98, 102, 99])
custos_fornecedor_b = np.array([110, 115, 108, 112, 109])

t_stat, p_value = ttest_ind(custos_fornecedor_a, custos_fornecedor_b)

alpha = 0.05
if p_value < alpha:
    print("Diferença significativa entre fornecedores")
else:
    print("Sem diferença significativa")

# Teste t pareado (antes/depois)
produtividade_antes = np.array([10, 12, 11, 13, 12])
produtividade_depois = np.array([12, 14, 13, 15, 14])

t_stat, p_value = ttest_rel(produtividade_antes, produtividade_depois)
```

### Teste Qui-Quadrado

```python
from scipy.stats import chi2_contingency

# Tabela de contingência: Tipo de obra vs Atraso
tabela = np.array([
    [30, 10],  # Residencial: [No prazo, Atrasado]
    [20, 15]   # Comercial: [No prazo, Atrasado]
])

chi2, p_value, dof, expected = chi2_contingency(tabela)

if p_value < 0.05:
    print("Há associação entre tipo de obra e atraso")
```

## 5. Correlação

```python
# Correlação de Pearson
custo = np.array([100, 200, 300, 400, 500])
prazo = np.array([30, 45, 60, 75, 90])

correlacao, p_value = stats.pearsonr(custo, prazo)
print(f"Correlação: {correlacao:.4f}")

# Interpretação
if abs(correlacao) > 0.8:
    print("Correlação forte")
elif abs(correlacao) > 0.5:
    print("Correlação moderada")
else:
    print("Correlação fraca")
```

## 6. Análise de Outliers

```python
def detectar_outliers_iqr(dados):
    """Detecta outliers pelo método IQR."""
    q1 = np.percentile(dados, 25)
    q3 = np.percentile(dados, 75)
    iqr = q3 - q1
    
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    
    outliers = dados[(dados < limite_inferior) | (dados > limite_superior)]
    
    return outliers, limite_inferior, limite_superior

# Exemplo
custos = np.array([100, 105, 98, 102, 99, 200, 101, 103])  # 200 é outlier
outliers, li, ls = detectar_outliers_iqr(custos)
print(f"Outliers: {outliers}")
```

## 7. Aplicação: Previsão de Custos

```python
def prever_custo_com_intervalo(
    dados_historicos: pd.DataFrame,
    area_nova: float,
    confianca: float = 0.95
) -> dict:
    """
    Prevê custo de obra com intervalo de confiança.
    
    Args:
        dados_historicos: DataFrame com colunas 'area_m2' e 'custo_total'
        area_nova: Área da nova obra (m²)
        confianca: Nível de confiança (0.95 = 95%)
    
    Returns:
        dict com previsão e intervalo
    """
    X = dados_historicos['area_m2'].values
    y = dados_historicos['custo_total'].values
    
    # Regressão
    slope, intercept, r_value, p_value, std_err = linregress(X, y)
    
    # Previsão pontual
    custo_previsto = intercept + slope * area_nova
    
    # Erro padrão da previsão
    residuos = y - (intercept + slope * X)
    s_residual = np.std(residuos, ddof=2)
    
    n = len(X)
    x_mean = np.mean(X)
    sxx = np.sum((X - x_mean)**2)
    
    erro_previsao = s_residual * np.sqrt(1 + 1/n + (area_nova - x_mean)**2 / sxx)
    
    # Intervalo de confiança
    t_critico = t.ppf((1 + confianca) / 2, df=n-2)
    margem = t_critico * erro_previsao
    
    return {
        'custo_previsto': custo_previsto,
        'limite_inferior': custo_previsto - margem,
        'limite_superior': custo_previsto + margem,
        'r_quadrado': r_value**2,
        'equacao': f"Custo = {intercept:.2f} + {slope:.2f} × Área"
    }

# Uso
df_historico = pd.DataFrame({
    'area_m2': [50, 80, 100, 150, 200],
    'custo_total': [150000, 240000, 300000, 450000, 600000]
})

resultado = prever_custo_com_intervalo(df_historico, area_nova=120)
print(f"Previsão: R$ {resultado['custo_previsto']:,.2f}")
print(f"IC 95%: [R$ {resultado['limite_inferior']:,.2f}, R$ {resultado['limite_superior']:,.2f}]")
```

## Referências

- **Scipy Stats Documentation**: https://docs.scipy.org/doc/scipy/reference/stats.html
- **Statistics for Engineers** (Montgomery & Runger)
- **Practical Statistics for Data Scientists** (Bruce & Bruce)
