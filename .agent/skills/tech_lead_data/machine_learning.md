---
skill_name: "Machine Learning para Engenharia"
agent: tech_lead_data
category: "Data Science"
difficulty: advanced
version: 1.0.0
---

# Skill: Machine Learning - Scikit-learn para Previsão de Custos

## Objetivo

Fornecer guia prático de Machine Learning com Scikit-learn para previsão de custos, classificação de itens e otimização de orçamentos.

## 1. Regressão Linear (Previsão de Custos)

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

# Dados de treinamento
df = pd.DataFrame({
    'area_m2': [50, 80, 100, 150, 200, 250, 300],
    'num_pavimentos': [1, 2, 2, 3, 4, 4, 5],
    'padrao': [1, 1, 2, 2, 3, 3, 3],  # 1=baixo, 2=médio, 3=alto
    'custo_total': [150000, 240000, 350000, 500000, 750000, 900000, 1200000]
})

# Features (X) e Target (y)
X = df[['area_m2', 'num_pavimentos', 'padrao']]
y = df['custo_total']

# Split treino/teste (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Previsões
y_pred = modelo.predict(X_test)

# Métricas
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: R$ {rmse:,.2f}")
print(f"R²: {r2:.4f}")

# Coeficientes
print("\nCoeficientes:")
for feature, coef in zip(X.columns, modelo.coef_):
    print(f"  {feature}: {coef:,.2f}")
print(f"Intercept: {modelo.intercept_:,.2f}")

# Prever nova obra
nova_obra = pd.DataFrame({
    'area_m2': [180],
    'num_pavimentos': [3],
    'padrao': [2]
})
custo_previsto = modelo.predict(nova_obra)[0]
print(f"\nPrevisão para nova obra: R$ {custo_previsto:,.2f}")
```

## 2. Regressão Polinomial

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Pipeline: Polinomial + Regressão
modelo_poly = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression())
])

modelo_poly.fit(X_train, y_train)
y_pred_poly = modelo_poly.predict(X_test)

r2_poly = r2_score(y_test, y_pred_poly)
print(f"R² (Polinomial): {r2_poly:.4f}")
```

## 3. Random Forest (Melhor para Não-Linearidades)

```python
from sklearn.ensemble import RandomForestRegressor

# Modelo Random Forest
rf_modelo = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

rf_modelo.fit(X_train, y_train)
y_pred_rf = rf_modelo.predict(X_test)

# Métricas
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest RMSE: R$ {rmse_rf:,.2f}")
print(f"Random Forest R²: {r2_rf:.4f}")

# Importância das features
importancias = pd.DataFrame({
    'feature': X.columns,
    'importancia': rf_modelo.feature_importances_
}).sort_values('importancia', ascending=False)

print("\nImportância das Features:")
print(importancias)
```

## 4. Validação Cruzada

```python
from sklearn.model_selection import cross_val_score

# Cross-validation com 5 folds
scores = cross_val_score(
    modelo,
    X,
    y,
    cv=5,
    scoring='r2'
)

print(f"R² médio (CV): {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## 5. Classificação (K-Nearest Neighbors)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Classificar itens por categoria de custo
df_class = pd.DataFrame({
    'quantidade': [10, 50, 100, 200, 500, 1000],
    'preco_unitario': [100, 50, 20, 10, 5, 2],
    'categoria': ['Alto', 'Alto', 'Médio', 'Médio', 'Baixo', 'Baixo']
})

X = df_class[['quantidade', 'preco_unitario']]
y = df_class['categoria']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Modelo KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Previsões
y_pred = knn.predict(X_test)

# Métricas
print(classification_report(y_test, y_pred))
print("\nMatriz de Confusão:")
print(confusion_matrix(y_test, y_pred))
```

## 6. Feature Engineering

```python
# Criar features derivadas
df['custo_por_m2'] = df['custo_total'] / df['area_m2']
df['area_por_pavimento'] = df['area_m2'] / df['num_pavimentos']
df['log_area'] = np.log(df['area_m2'])

# Interações
df['area_x_padrao'] = df['area_m2'] * df['padrao']

# One-Hot Encoding (variáveis categóricas)
df_encoded = pd.get_dummies(df, columns=['tipo_obra'], drop_first=True)
```

## 7. Normalização e Padronização

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Padronização (média=0, desvio=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Normalização (min=0, max=1)
normalizer = MinMaxScaler()
X_normalized = normalizer.fit_transform(X)

# Pipeline com escalonamento
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

pipeline.fit(X_train, y_train)
```

## 8. Grid Search (Otimização de Hiperparâmetros)

```python
from sklearn.model_selection import GridSearchCV

# Definir grid de parâmetros
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

# Grid Search
grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print(f"Melhores parâmetros: {grid_search.best_params_}")
print(f"Melhor R²: {grid_search.best_score_:.4f}")

# Usar melhor modelo
melhor_modelo = grid_search.best_estimator_
```

## 9. Aplicação Completa: Sistema de Previsão

```python
class PrevisaoCustoObra:
    """Sistema de previsão de custo de obras usando ML."""
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.features = ['area_m2', 'num_pavimentos', 'padrao']
    
    def treinar(self, df_historico: pd.DataFrame):
        """Treina modelo com dados históricos."""
        X = df_historico[self.features]
        y = df_historico['custo_total']
        
        # Escalonar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Treinar Random Forest
        self.modelo = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.modelo.fit(X_scaled, y)
        
        # Validação cruzada
        scores = cross_val_score(self.modelo, X_scaled, y, cv=5, scoring='r2')
        
        return {
            'r2_medio': scores.mean(),
            'r2_std': scores.std()
        }
    
    def prever(self, area_m2: float, num_pavimentos: int, padrao: int) -> dict:
        """Prevê custo de nova obra."""
        if self.modelo is None:
            raise ValueError("Modelo não treinado. Execute treinar() primeiro.")
        
        # Preparar dados
        X_novo = pd.DataFrame({
            'area_m2': [area_m2],
            'num_pavimentos': [num_pavimentos],
            'padrao': [padrao]
        })
        
        X_scaled = self.scaler.transform(X_novo)
        
        # Previsão
        custo_previsto = self.modelo.predict(X_scaled)[0]
        
        # Intervalo de confiança (usando árvores individuais)
        previsoes_arvores = np.array([
            arvore.predict(X_scaled)[0]
            for arvore in self.modelo.estimators_
        ])
        
        ic_inferior = np.percentile(previsoes_arvores, 2.5)
        ic_superior = np.percentile(previsoes_arvores, 97.5)
        
        return {
            'custo_previsto': custo_previsto,
            'ic_95_inferior': ic_inferior,
            'ic_95_superior': ic_superior,
            'desvio_padrao': np.std(previsoes_arvores)
        }

# Uso
sistema = PrevisaoCustoObra()

# Treinar com dados históricos
df_historico = pd.DataFrame({
    'area_m2': [50, 80, 100, 150, 200, 250, 300, 350, 400],
    'num_pavimentos': [1, 2, 2, 3, 4, 4, 5, 5, 6],
    'padrao': [1, 1, 2, 2, 3, 3, 3, 2, 3],
    'custo_total': [150000, 240000, 350000, 500000, 750000, 900000, 1200000, 1100000, 1500000]
})

metricas = sistema.treinar(df_historico)
print(f"R² médio: {metricas['r2_medio']:.4f}")

# Prever nova obra
resultado = sistema.prever(area_m2=180, num_pavimentos=3, padrao=2)
print(f"\nPrevisão: R$ {resultado['custo_previsto']:,.2f}")
print(f"IC 95%: [R$ {resultado['ic_95_inferior']:,.2f}, R$ {resultado['ic_95_superior']:,.2f}]")
```

## 10. Checklist

Ao usar Machine Learning:

- [ ] Dividir dados em treino/teste (80/20 ou 70/30)
- [ ] Escalonar features (StandardScaler ou MinMaxScaler)
- [ ] Validar com cross-validation
- [ ] Avaliar múltiplas métricas (RMSE, R², MAE)
- [ ] Verificar overfitting (treino vs teste)
- [ ] Interpretar importância das features
- [ ] Documentar hiperparâmetros escolhidos
- [ ] Salvar modelo treinado (pickle ou joblib)

## Referências

- **Scikit-learn Documentation**: https://scikit-learn.org/
- **Hands-On Machine Learning** (Aurélien Géron)
- **Introduction to Statistical Learning** (James et al.)
