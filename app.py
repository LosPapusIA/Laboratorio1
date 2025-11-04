import streamlit as st
import time
from collections import deque
import heapq
import copy

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(
    page_title="Laboratorio IA - Algoritmos de Búsqueda", page_icon="🤖", layout="wide"
)


# ===========================
# CLASE LABERINTO (Problema 1)
# ===========================
class Laberinto:
    def __init__(self, matriz):
        self.matriz = matriz
        self.filas = len(matriz)
        self.columnas = len(matriz[0])
        self.inicio = None
        self.objetivo = None

        for i in range(self.filas):
            for j in range(self.columnas):
                if matriz[i][j] == "R":
                    self.inicio = (i, j)
                elif matriz[i][j] == "Q":
                    self.objetivo = (i, j)

    def es_valido(self, pos):
        fila, col = pos
        return (
            0 <= fila < self.filas
            and 0 <= col < self.columnas
            and self.matriz[fila][col] != 1
        )

    def obtener_vecinos(self, pos):
        fila, col = pos
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        vecinos = []

        for mov_fila, mov_col in movimientos:
            nueva_pos = (fila + mov_fila, col + mov_col)
            if self.es_valido(nueva_pos):
                vecinos.append(nueva_pos)

        return vecinos

    def reconstruir_camino(self, padres, inicio, objetivo):
        camino = []
        actual = objetivo

        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual)

        camino.reverse()
        return camino

    def busqueda_anchura(self):
        inicio_tiempo = time.time()

        cola = deque([self.inicio])
        visitados = {self.inicio}
        padres = {self.inicio: None}
        nodos_explorados = 0

        while cola:
            actual = cola.popleft()
            nodos_explorados += 1

            if actual == self.objetivo:
                tiempo_total = time.time() - inicio_tiempo
                camino = self.reconstruir_camino(padres, self.inicio, self.objetivo)
                return camino, nodos_explorados, tiempo_total

            for vecino in self.obtener_vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.append(vecino)

        return None, nodos_explorados, time.time() - inicio_tiempo

    def heuristica_manhattan(self, pos):
        return abs(pos[0] - self.objetivo[0]) + abs(pos[1] - self.objetivo[1])

    def busqueda_a_estrella(self):
        inicio_tiempo = time.time()

        contador = 0
        cola_prioridad = [(0, contador, self.inicio)]
        heapq.heapify(cola_prioridad)

        visitados = set()
        padres = {self.inicio: None}
        g_score = {self.inicio: 0}
        nodos_explorados = 0

        while cola_prioridad:
            _, _, actual = heapq.heappop(cola_prioridad)

            if actual in visitados:
                continue

            visitados.add(actual)
            nodos_explorados += 1

            if actual == self.objetivo:
                tiempo_total = time.time() - inicio_tiempo
                camino = self.reconstruir_camino(padres, self.inicio, self.objetivo)
                return camino, nodos_explorados, tiempo_total

            for vecino in self.obtener_vecinos(actual):
                nuevo_g = g_score[actual] + 1

                if vecino not in g_score or nuevo_g < g_score[vecino]:
                    g_score[vecino] = nuevo_g
                    h = self.heuristica_manhattan(vecino)
                    f = nuevo_g + h

                    contador += 1
                    heapq.heappush(cola_prioridad, (f, contador, vecino))
                    padres[vecino] = actual

        return None, nodos_explorados, time.time() - inicio_tiempo


# ===========================
# CLASE DAMAS (Problema 2)
# ===========================
class Damas:
    def __init__(self):
        self.tablero = self.crear_tablero_inicial()
        self.turno = 1

    def crear_tablero_inicial(self):
        tablero = [[0 for _ in range(8)] for _ in range(8)]

        for fila in range(3):
            for col in range(8):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = -1

        for fila in range(5, 8):
            for col in range(8):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = 1

        return tablero

    def obtener_movimientos(self, tablero, jugador):
        movimientos = []
        capturas = self.obtener_capturas(tablero, jugador)
        if capturas:
            return capturas

        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]
                if (jugador > 0 and pieza > 0) or (jugador < 0 and pieza < 0):
                    movs = self.obtener_movimientos_pieza(tablero, fila, col, pieza)
                    movimientos.extend(movs)

        return movimientos

    def obtener_movimientos_pieza(self, tablero, fila, col, pieza):
        movimientos = []
        es_dama = abs(pieza) == 2

        if pieza > 0:
            direcciones = [(-1, -1), (-1, 1)]
            if es_dama:
                direcciones.extend([(1, -1), (1, 1)])
        else:
            direcciones = [(1, -1), (1, 1)]
            if es_dama:
                direcciones.extend([(-1, -1), (-1, 1)])

        for df, dc in direcciones:
            nueva_fila = fila + df
            nueva_col = col + dc

            if (
                0 <= nueva_fila < 8
                and 0 <= nueva_col < 8
                and tablero[nueva_fila][nueva_col] == 0
            ):
                movimientos.append(
                    {
                        "desde": (fila, col),
                        "hasta": (nueva_fila, nueva_col),
                        "captura": None,
                    }
                )

        return movimientos

    def obtener_capturas(self, tablero, jugador):
        capturas = []
        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]
                if (jugador > 0 and pieza > 0) or (jugador < 0 and pieza < 0):
                    caps = self.obtener_capturas_pieza(tablero, fila, col, pieza)
                    capturas.extend(caps)
        return capturas

    def obtener_capturas_pieza(self, tablero, fila, col, pieza):
        capturas = []
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for df, dc in direcciones:
            enemigo_fila = fila + df
            enemigo_col = col + dc
            destino_fila = fila + 2 * df
            destino_col = col + 2 * dc

            if (
                0 <= enemigo_fila < 8
                and 0 <= enemigo_col < 8
                and 0 <= destino_fila < 8
                and 0 <= destino_col < 8
            ):
                enemigo = tablero[enemigo_fila][enemigo_col]
                destino = tablero[destino_fila][destino_col]

                if (
                    enemigo != 0
                    and destino == 0
                    and ((pieza > 0 and enemigo < 0) or (pieza < 0 and enemigo > 0))
                ):
                    capturas.append(
                        {
                            "desde": (fila, col),
                            "hasta": (destino_fila, destino_col),
                            "captura": (enemigo_fila, enemigo_col),
                        }
                    )

        return capturas

    def aplicar_movimiento(self, tablero, movimiento):
        nuevo_tablero = copy.deepcopy(tablero)
        desde_fila, desde_col = movimiento["desde"]
        hasta_fila, hasta_col = movimiento["hasta"]

        pieza = nuevo_tablero[desde_fila][desde_col]
        nuevo_tablero[desde_fila][desde_col] = 0
        nuevo_tablero[hasta_fila][hasta_col] = pieza

        if movimiento["captura"]:
            cap_fila, cap_col = movimiento["captura"]
            nuevo_tablero[cap_fila][cap_col] = 0

        if pieza == 1 and hasta_fila == 0:
            nuevo_tablero[hasta_fila][hasta_col] = 2
        elif pieza == -1 and hasta_fila == 7:
            nuevo_tablero[hasta_fila][hasta_col] = -2

        return nuevo_tablero

    def evaluar_tablero(self, tablero):
        puntuacion = 0
        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]
                if pieza == 1:
                    puntuacion += 10 + fila
                elif pieza == 2:
                    puntuacion += 30
                elif pieza == -1:
                    puntuacion -= 10 + (7 - fila)
                elif pieza == -2:
                    puntuacion -= 30
        return puntuacion

    def es_terminal(self, tablero, jugador):
        movimientos = self.obtener_movimientos(tablero, jugador)
        return len(movimientos) == 0

    def minimax(self, tablero, profundidad, maximizando, jugador):
        if profundidad == 0 or self.es_terminal(tablero, jugador):
            return self.evaluar_tablero(tablero), None

        movimientos = self.obtener_movimientos(tablero, jugador)

        if maximizando:
            max_eval = float("-inf")
            mejor_mov = None

            for movimiento in movimientos:
                nuevo_tablero = self.aplicar_movimiento(tablero, movimiento)
                evaluacion, _ = self.minimax(
                    nuevo_tablero, profundidad - 1, False, -jugador
                )

                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_mov = movimiento

            return max_eval, mejor_mov
        else:
            min_eval = float("inf")
            mejor_mov = None

            for movimiento in movimientos:
                nuevo_tablero = self.aplicar_movimiento(tablero, movimiento)
                evaluacion, _ = self.minimax(
                    nuevo_tablero, profundidad - 1, True, -jugador
                )

                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_mov = movimiento

            return min_eval, mejor_mov

    def alfabeta(self, tablero, profundidad, alfa, beta, maximizando, jugador):
        if profundidad == 0 or self.es_terminal(tablero, jugador):
            return self.evaluar_tablero(tablero), None

        movimientos = self.obtener_movimientos(tablero, jugador)

        if maximizando:
            max_eval = float("-inf")
            mejor_mov = None

            for movimiento in movimientos:
                nuevo_tablero = self.aplicar_movimiento(tablero, movimiento)
                evaluacion, _ = self.alfabeta(
                    nuevo_tablero, profundidad - 1, alfa, beta, False, -jugador
                )

                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_mov = movimiento

                alfa = max(alfa, evaluacion)
                if beta <= alfa:
                    break

            return max_eval, mejor_mov
        else:
            min_eval = float("inf")
            mejor_mov = None

            for movimiento in movimientos:
                nuevo_tablero = self.aplicar_movimiento(tablero, movimiento)
                evaluacion, _ = self.alfabeta(
                    nuevo_tablero, profundidad - 1, alfa, beta, True, -jugador
                )

                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_mov = movimiento

                beta = min(beta, evaluacion)
                if beta <= alfa:
                    break

            return min_eval, mejor_mov


# ===========================
# FUNCIONES DE VISUALIZACIÓN
# ===========================
def visualizar_laberinto(laberinto, camino=None):
    """Visualiza el laberinto con el camino si existe"""
    html = "<div style='font-family: monospace; font-size: 20px; line-height: 1.2;'>"

    for i, fila in enumerate(laberinto.matriz):
        for j, celda in enumerate(fila):
            if camino and (i, j) in camino and celda not in ["R", "Q"]:
                html += "🟢 "
            elif celda == 1:
                html += "⬛ "
            elif celda == "R":
                html += "🐭 "
            elif celda == "Q":
                html += "🧀 "
            else:
                html += "⬜ "
        html += "<br>"

    html += "</div>"
    return html


def visualizar_tablero_damas(tablero):
    """Visualiza el tablero de damas"""
    html = "<div style='font-family: monospace; font-size: 24px; line-height: 1.2;'>"

    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if celda == 0:
                html += "⬜ " if (i + j) % 2 == 0 else "⬛ "
            elif celda == 1:
                html += "⚪ "
            elif celda == 2:
                html += "👑 "
            elif celda == -1:
                html += "⚫ "
            elif celda == -2:
                html += "♛ "
        html += "<br>"

    html += "</div>"
    return html


# ===========================
# INTERFAZ PRINCIPAL
# ===========================
def main():
    st.title("🤖 Laboratorio de Algoritmos de Búsqueda")
    st.markdown(
        "### Inteligencia Artificial - Implementación de BFS, A*, Minimax y Alfa-Beta"
    )

    st.sidebar.header("⚙️ Configuración")
    problema = st.sidebar.selectbox(
        "Selecciona un problema:",
        ["🐭 Ratón Hambriento en el Laberinto", "♟️ Juego de Damas"],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Desarrollado por:**")
    st.sidebar.info("Laboratorio 1 - IA\nAlgoritmos de Búsqueda")

    if problema == "🐭 Ratón Hambriento en el Laberinto":
        mostrar_problema_laberinto()
    else:
        mostrar_problema_damas()


def mostrar_problema_laberinto():
    st.header("🐭 Problema 1: Ratón Hambriento en el Laberinto")

    st.markdown("""
    **Objetivo:** El ratón debe encontrar el camino más corto hasta el queso.
    - 🐭 = Ratón (inicio)
    - 🧀 = Queso (objetivo)
    - ⬛ = Pared
    - ⬜ = Camino libre
    - 🟢 = Camino encontrado
    """)

    # Laberinto predefinido
    laberinto_matriz = [
        ["R", 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, "Q"],
    ]

    laberinto = Laberinto(laberinto_matriz)

    st.subheader("📋 Laberinto Inicial")
    st.markdown(visualizar_laberinto(laberinto), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 Búsqueda en Anchura (BFS)")
        if st.button("▶️ Ejecutar BFS", key="bfs"):
            with st.spinner("Explorando con BFS..."):
                camino, nodos, tiempo = laberinto.busqueda_anchura()

                if camino:
                    st.success("¡Queso encontrado! 🧀")
                    st.metric("Nodos explorados", nodos)
                    st.metric("Longitud del camino", len(camino))
                    st.metric("Tiempo", f"{tiempo:.6f} seg")

                    st.markdown("**Camino encontrado:**")
                    st.markdown(
                        visualizar_laberinto(laberinto, camino), unsafe_allow_html=True
                    )
                else:
                    st.error("No se encontró camino al queso 😢")

    with col2:
        st.subheader("🟢 Búsqueda A* (A-Star)")
        if st.button("▶️ Ejecutar A*", key="astar"):
            with st.spinner("Explorando con A*..."):
                camino, nodos, tiempo = laberinto.busqueda_a_estrella()

                if camino:
                    st.success("¡Queso encontrado! 🧀")
                    st.metric("Nodos explorados", nodos)
                    st.metric("Longitud del camino", len(camino))
                    st.metric("Tiempo", f"{tiempo:.6f} seg")

                    st.markdown("**Camino encontrado:**")
                    st.markdown(
                        visualizar_laberinto(laberinto, camino), unsafe_allow_html=True
                    )
                else:
                    st.error("No se encontró camino al queso 😢")


def mostrar_problema_damas():
    st.header("♟️ Problema 2: Juego de Damas")

    st.markdown("""
    **Objetivo:** Encontrar la mejor jugada usando algoritmos adversariales.
    - ⚪ = Ficha blanca
    - 👑 = Dama blanca
    - ⚫ = Ficha negra
    - ♛ = Dama negra
    """)

    profundidad = st.slider("Profundidad de búsqueda", 1, 6, 4)

    juego = Damas()

    st.subheader("📋 Tablero Inicial")
    st.markdown(visualizar_tablero_damas(juego.tablero), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 Minimax")
        if st.button("▶️ Ejecutar Minimax", key="minimax"):
            with st.spinner("Calculando con Minimax..."):
                inicio = time.time()
                eval_minimax, mov_minimax = juego.minimax(
                    juego.tablero, profundidad, True, 1
                )
                tiempo_minimax = time.time() - inicio

                st.success("¡Mejor jugada calculada!")
                st.metric("Tiempo de ejecución", f"{tiempo_minimax:.4f} seg")
                st.metric("Evaluación del tablero", eval_minimax)

                if mov_minimax:
                    st.info(
                        f"**Mejor movimiento:**\nDesde: {mov_minimax['desde']}\nHasta: {mov_minimax['hasta']}"
                    )

                    tablero_nuevo = juego.aplicar_movimiento(juego.tablero, mov_minimax)
                    st.markdown("**Tablero después del movimiento:**")
                    st.markdown(
                        visualizar_tablero_damas(tablero_nuevo), unsafe_allow_html=True
                    )

    with col2:
        st.subheader("🟢 Poda Alfa-Beta")
        if st.button("▶️ Ejecutar Alfa-Beta", key="alfabeta"):
            with st.spinner("Calculando con Alfa-Beta..."):
                inicio = time.time()
                eval_alfabeta, mov_alfabeta = juego.alfabeta(
                    juego.tablero, profundidad, float("-inf"), float("inf"), True, 1
                )
                tiempo_alfabeta = time.time() - inicio

                st.success("¡Mejor jugada calculada!")
                st.metric("Tiempo de ejecución", f"{tiempo_alfabeta:.4f} seg")
                st.metric("Evaluación del tablero", eval_alfabeta)

                if mov_alfabeta:
                    st.info(
                        f"**Mejor movimiento:**\nDesde: {mov_alfabeta['desde']}\nHasta: {mov_alfabeta['hasta']}"
                    )

                    tablero_nuevo = juego.aplicar_movimiento(
                        juego.tablero, mov_alfabeta
                    )
                    st.markdown("**Tablero después del movimiento:**")
                    st.markdown(
                        visualizar_tablero_damas(tablero_nuevo), unsafe_allow_html=True
                    )


if __name__ == "__main__":
    main()
