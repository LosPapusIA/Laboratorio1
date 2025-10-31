# Laboratorio 1 - Algoritmos de Búsqueda

## 📋 Contenido
- [Problema 1: Ratón Hambriento en el Laberinto](#problema-1-ratón-hambriento-en-el-laberinto)
- [Problema 2: Juego de Damas](#problema-2-juego-de-damas)
- [Conclusiones Generales](#conclusiones-generales)

---

## Problema 1: Ratón Hambriento en el Laberinto

### 🐭 Descripción del Problema
Se encuentra un ratón hambriento al inicio de un laberinto. El ratón siente el olor del queso y quiere llegar a él tomando el camino más corto posible. El laberinto está representado por una matriz donde:
- `R` = Posición inicial del ratón
- `Q` = Posición del queso (objetivo)
- `0` = Camino libre
- `1` = Pared (obstáculo)

**Estado Inicial S(x):**
```
Posición del Ratón: (0, 0)
Posición del Queso: (5, 6)
```

**Objetivo:** Encontrar el camino más corto desde el ratón hasta el queso.

---

### 🔍 Metodologías Implementadas

#### 1. Búsqueda en Anchura (BFS - Breadth-First Search)

**Descripción:**
- Algoritmo de búsqueda no informada que explora el espacio de estados nivel por nivel
- Utiliza una estructura de datos tipo cola (FIFO - First In, First Out)
- Expande todos los nodos a una profundidad antes de pasar al siguiente nivel
- No utiliza conocimiento del dominio (heurística)

**Características:**

| Propiedad | Valor |
|-----------|-------|
| **Completo** | ✅ Sí - Siempre encuentra una solución si existe |
| **Óptimo** | ✅ Sí - Encuentra el camino más corto (cuando el costo es uniforme) |
| **Complejidad Temporal** | O(b^d) donde b=factor de ramificación, d=profundidad de la solución |
| **Complejidad Espacial** | O(b^d) - Debe almacenar todos los nodos en memoria |

**Restricciones de Movimiento:**
- Movimientos permitidos: **Arriba, Abajo, Izquierda, Derecha** (4 direcciones)
- Orden de exploración: Derecha → Abajo → Izquierda → Arriba
- No se permiten movimientos diagonales

**Costo de Ruta:**
- Cada movimiento tiene costo 1
- Costo total: Número de pasos en el camino

---

#### 2. Búsqueda A* (A-Star)

**Descripción:**
- Algoritmo de búsqueda informada que utiliza una función heurística
- Combina el costo acumulado g(n) con una estimación heurística h(n)
- Función de evaluación: f(n) = g(n) + h(n)
- Utiliza la heurística de **Distancia Manhattan**: h(n) = |x₁ - x₂| + |y₁ - y₂|

**Características:**

| Propiedad | Valor |
|-----------|-------|
| **Completo** | ✅ Sí - Con heurística admisible |
| **Óptimo** | ✅ Sí - Con heurística admisible y consistente |
| **Complejidad Temporal** | O(b^d) en el peor caso, pero generalmente mucho mejor |
| **Complejidad Espacial** | O(b^d) - Mantiene todos los nodos generados en memoria |

**Heurística Utilizada:**
```
h(n) = |fila_actual - fila_objetivo| + |col_actual - col_objetivo|
```
Esta heurística es **admisible** (nunca sobreestima) y **consistente**.

**Restricciones de Movimiento:**
- Movimientos permitidos: **Arriba, Abajo, Izquierda, Derecha** (4 direcciones)
- Prioriza movimientos que minimicen f(n)
- No se permiten movimientos diagonales

**Costo de Ruta:**
- Cada movimiento tiene costo 1
- Costo total: g(n) = número de pasos desde el inicio

---

### 📊 Resultados del Problema 1

```
BFS:
- Nodos explorados: 28
- Longitud del camino: 12
- Tiempo de ejecución: 0.002227 segundos

A*:
- Nodos explorados: 15
- Longitud del camino: 12
- Tiempo de ejecución: 0.001303 segundos

Eficiencia de A*: 46.4% más eficiente que BFS
```

**Camino encontrado (ambos algoritmos):**
```
(0,0) → (0,1) → (1,1) → (2,1) → (2,2) → (2,3) → (3,3) →
(3,4) → (3,5) → (4,5) → (5,5) → (5,6)
```

---

### 🎯 Conclusiones del Problema 1

**Estado Inicial:** S(x) = (0, 0) - Posición del ratón
**Estado Objetivo:** (5, 6) - Posición del queso

**Restricciones:**
- Espacio de búsqueda: Matriz 6×7
- Movimientos: 4 direcciones cardinales (no diagonales)
- Obstáculos: Paredes que bloquean el paso
- Costo uniforme: Cada paso = 1 unidad

**Costo de Ruta:**
- Costo mínimo encontrado: **12 pasos**
- Ambos algoritmos encontraron la solución óptima

**Análisis Comparativo:**
1. **BFS** exploró más nodos (28) pero garantiza optimalidad
2. **A*** exploró menos nodos (15) gracias a su heurística
3. **A*** fue significativamente más rápido (46.4% de mejora)
4. La heurística Manhattan guió eficientemente la búsqueda hacia el objetivo
5. Para laberintos más grandes, la diferencia sería aún más notable

---

## Problema 2: Juego de Damas

### ♟️ Descripción del Problema
Implementación de un agente inteligente que juega damas (checkers) utilizando algoritmos de búsqueda adversarial. El juego se desarrolla en un tablero de 8×8 con dos jugadores (blancas y negras) que alternan turnos. El objetivo es capturar todas las fichas del oponente o bloquear sus movimientos.

**Reglas del Juego:**
- Fichas normales se mueven diagonalmente hacia adelante
- Al llegar al extremo opuesto, las fichas se coronan como "damas"
- Las damas pueden moverse en cualquier dirección diagonal
- Las capturas son obligatorias cuando están disponibles
- Se puede capturar saltando sobre una ficha enemiga

**Estado Inicial S(x):**
```
Tablero 8×8:
- Fichas blancas en filas 5, 6, 7 (12 fichas)
- Fichas negras en filas 0, 1, 2 (12 fichas)
- Turno inicial: Blancas (jugador maximizante)
```

---

### 🔍 Metodologías Implementadas

#### 1. Minimax

**Descripción:**
- Algoritmo de búsqueda adversarial para juegos de suma cero con dos jugadores
- Explora recursivamente el árbol de juego completo
- Asume que ambos jugadores juegan de manera óptima
- El jugador MAX intenta maximizar la evaluación
- El jugador MIN intenta minimizar la evaluación
- Utiliza backtracking para propagar valores hacia la raíz

**Características:**

| Propiedad | Valor |
|-----------|-------|
| **Completo** | ✅ Sí - Explora todo el árbol hasta la profundidad límite |
| **Óptimo** | ✅ Sí - Encuentra la mejor jugada asumiendo juego perfecto del oponente |
| **Complejidad Temporal** | O(b^m) donde b=movimientos promedio por posición, m=profundidad máxima |
| **Complejidad Espacial** | O(b×m) - Solo mantiene el camino actual en la recursión |

**Función de Evaluación:**
```
Puntuación = Σ(valor_fichas_blancas) - Σ(valor_fichas_negras)

Valores:
- Ficha normal: 10 puntos
- Dama: 30 puntos
- Bonificación por avance: +1 por cada fila avanzada
```

**Restricciones:**
- Movimientos: Diagonales (4 direcciones para damas, 2 para fichas normales)
- Profundidad de búsqueda: Limitada a 4 niveles (configurable)
- Capturas obligatorias tienen prioridad

**Costo de Ruta:**
- No aplica concepto de "costo" en términos tradicionales
- Se evalúa la "utilidad" de cada estado del tablero

---

#### 2. Poda Alfa-Beta (Alpha-Beta Pruning)

**Descripción:**
- Optimización del algoritmo Minimax
- Mantiene dos valores: α (mejor opción para MAX) y β (mejor opción para MIN)
- Poda ramas del árbol que no pueden influir en la decisión final
- Produce el mismo resultado que Minimax pero explorando menos nodos
- La eficiencia depende del orden de exploración de los movimientos

**Características:**

| Propiedad | Valor |
|-----------|-------|
| **Completo** | ✅ Sí - Idéntico a Minimax |
| **Óptimo** | ✅ Sí - Encuentra exactamente la misma mejor jugada que Minimax |
| **Complejidad Temporal** | O(b^(m/2)) en el mejor caso (orden perfecto) |
| **Complejidad Espacial** | O(b×m) - Igual que Minimax |

**Mecanismo de Poda:**
```
Si β ≤ α:
  PODAR (no explorar hermanos restantes)

Donde:
- α = Mejor valor garantizado para MAX
- β = Mejor valor garantizado para MIN
```

**Restricciones:**
- Idénticas a Minimax
- Movimientos: Diagonales según tipo de ficha
- Profundidad de búsqueda: 4 niveles
- Mismo sistema de evaluación

**Costo de Ruta:**
- Evaluación heurística del estado del tablero
- Función de utilidad idéntica a Minimax

---

### 📊 Resultados del Problema 2

```
Minimax:
- Tiempo de ejecución: 0.0838 segundos
- Evaluación del tablero: 0 (equilibrado)
- Mejor movimiento: (5,0) → (4,1)

Alfabeta:
- Tiempo de ejecución: 0.0125 segundos
- Evaluación del tablero: 0 (equilibrado)
- Mejor movimiento: (5,0) → (4,1)

Aceleración: 6.70x más rápido
Mejora de eficiencia: 85.1%
```

---

### 🎯 Conclusiones del Problema 2

**Estado Inicial:** S(x) = Tablero estándar de damas con 12 fichas por jugador
**Estado Objetivo:** Maximizar ventaja posicional/material sobre el oponente

**Restricciones:**
- Espacio de búsqueda: Tablero 8×8 con reglas de damas
- Movimientos: Diagonales únicamente
  - Fichas blancas: Adelante-izquierda, Adelante-derecha
  - Fichas negras: Abajo-izquierda, Abajo-derecha
  - Damas: 4 direcciones diagonales
- Orden de prioridad: Capturas obligatorias > Movimientos normales
- Profundidad de análisis: 4 niveles (4 movimientos por adelantado)

**Costo de Ruta:**
- No hay "costo" tradicional en juegos adversariales
- Se utiliza función de **utilidad/evaluación**:
  - Evaluación = 0: Juego equilibrado
  - Evaluación > 0: Ventaja para blancas
  - Evaluación < 0: Ventaja para negras

**Análisis Comparativo:**
1. **Minimax** explora exhaustivamente todos los nodos del árbol
2. **Alfabeta** poda aproximadamente 85% de los nodos innecesarios
3. Ambos algoritmos encuentran la **misma mejor jugada** (optimalidad garantizada)
4. **Alfabeta** es 6.7 veces más rápido sin sacrificar calidad
5. Con mayor profundidad, la ventaja de Alfabeta sería exponencialmente mayor
6. La eficiencia de Alfabeta depende del orden de exploración de movimientos
7. Para juegos con árboles grandes (ajedrez, go), la poda es esencial

**Ventajas de cada algoritmo:**
- **Minimax**: Más simple de implementar y entender
- **Alfabeta**: Mucho más eficiente, permite mayor profundidad de búsqueda

---

## 📈 Conclusiones Generales

### Comparación entre Problemas

| Aspecto | Problema 1 (Laberinto) | Problema 2 (Damas) |
|---------|------------------------|---------------------|
| **Tipo de Búsqueda** | Espacio de estados simple | Juego adversarial |
| **Algoritmos** | BFS (no informado) + A* (informado) | Minimax + Alfabeta |
| **Heurística** | Distancia Manhattan | Función de evaluación de tablero |
| **Optimalidad** | Ambos encuentran camino más corto | Ambos encuentran mejor jugada |
| **Eficiencia** | A* 46% más eficiente | Alfabeta 85% más eficiente |

### Lecciones Aprendidas

1. **Búsqueda Informada vs No Informada:**
   - Las heurísticas bien diseñadas mejoran drásticamente la eficiencia
   - A* demostró ser superior a BFS en exploración de nodos

2. **Optimización de Algoritmos:**
   - La poda Alfa-Beta es una optimización fundamental en juegos
   - No sacrifica calidad por velocidad (mismo resultado, menos trabajo)

3. **Aplicabilidad:**
   - BFS/A*: Ideal para pathfinding, navegación, planificación
   - Minimax/Alfabeta: Esencial para juegos de dos jugadores

4. **Escalabilidad:**
   - Para problemas más complejos, las optimizaciones se vuelven críticas
   - La diferencia de eficiencia se amplifica con el tamaño del problema

---

## 🚀 Ejecución

### Problema 1: Ratón y Queso
```bash
python raton-queso.py
```

### Problema 2: Juego de Damas
```bash
python juego-damas.py
```

---

## 📚 Referencias

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Algoritmos de búsqueda: BFS, A*, Minimax, Alfa-Beta
- Heurísticas: Distancia Manhattan, Función de evaluación en juegos

---

## 👨‍💻 Autor

Laboratorio 1 - Inteligencia Artificial
Implementación de Algoritmos de Búsqueda
