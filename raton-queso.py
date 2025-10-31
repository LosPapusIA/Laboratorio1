import heapq
from collections import deque
import time

class Laberinto:
    def __init__(self, matriz):
        """
        Inicializa el laberinto
        0 = camino libre
        1 = pared
        R = ratón (inicio)
        Q = queso (objetivo)
        """
        self.matriz = matriz
        self.filas = len(matriz)
        self.columnas = len(matriz[0])
        self.inicio = None
        self.objetivo = None

        # Encontrar posiciones del ratón y queso
        for i in range(self.filas):
            for j in range(self.columnas):
                if matriz[i][j] == 'R':
                    self.inicio = (i, j)
                elif matriz[i][j] == 'Q':
                    self.objetivo = (i, j)

    def es_valido(self, pos):
        """Verifica si una posición es válida"""
        fila, col = pos
        return (0 <= fila < self.filas and
                0 <= col < self.columnas and
                self.matriz[fila][col] != 1)

    def obtener_vecinos(self, pos):
        """Obtiene los vecinos válidos de una posición"""
        fila, col = pos
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
        vecinos = []

        for mov_fila, mov_col in movimientos:
            nueva_pos = (fila + mov_fila, col + mov_col)
            if self.es_valido(nueva_pos):
                vecinos.append(nueva_pos)

        return vecinos

    def reconstruir_camino(self, padres, inicio, objetivo):
        """Reconstruye el camino desde el inicio hasta el objetivo"""
        camino = []
        actual = objetivo

        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual)

        camino.reverse()
        return camino

    def busqueda_anchura(self):
        """
        BÚSQUEDA EN ANCHURA (BFS)
        - Estrategia no informada
        - Explora nivel por nivel
        - Garantiza encontrar el camino más corto
        """
        print("\n" + "="*60)
        print("BÚSQUEDA EN ANCHURA (BFS)")
        print("="*60)

        inicio_tiempo = time.time()

        cola = deque([self.inicio])
        visitados = {self.inicio}
        padres = {self.inicio: None}
        nodos_explorados = 0

        while cola:
            actual = cola.popleft()
            nodos_explorados += 1

            print(f"Explorando: {actual}")

            # ¿Llegamos al queso?
            if actual == self.objetivo:
                tiempo_total = time.time() - inicio_tiempo
                camino = self.reconstruir_camino(padres, self.inicio, self.objetivo)

                print(f"\n¡QUESO ENCONTRADO! 🧀")
                print(f"Nodos explorados: {nodos_explorados}")
                print(f"Longitud del camino: {len(camino)}")
                print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
                print(f"Camino: {' -> '.join(map(str, camino))}")

                return camino, nodos_explorados

            # Explorar vecinos
            for vecino in self.obtener_vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.append(vecino)

        print("No se encontró camino al queso 😢")
        return None, nodos_explorados

    def heuristica_manhattan(self, pos):
        """Calcula la distancia Manhattan hasta el objetivo"""
        return abs(pos[0] - self.objetivo[0]) + abs(pos[1] - self.objetivo[1])

    def busqueda_a_estrella(self):
        """
        BÚSQUEDA A* (A-Star)
        - Estrategia informada
        - Usa heurística (distancia Manhattan)
        - f(n) = g(n) + h(n)
        - Muy eficiente para encontrar caminos óptimos
        """
        print("\n" + "="*60)
        print("BÚSQUEDA A* (A-STAR)")
        print("="*60)

        inicio_tiempo = time.time()

        # Cola de prioridad: (f, contador, posición)
        contador = 0
        cola_prioridad = [(0, contador, self.inicio)]
        heapq.heapify(cola_prioridad)

        visitados = set()
        padres = {self.inicio: None}
        g_score = {self.inicio: 0}  # Costo desde el inicio
        nodos_explorados = 0

        while cola_prioridad:
            _, _, actual = heapq.heappop(cola_prioridad)

            if actual in visitados:
                continue

            visitados.add(actual)
            nodos_explorados += 1

            g_actual = g_score[actual]
            h_actual = self.heuristica_manhattan(actual)
            f_actual = g_actual + h_actual

            print(f"Explorando: {actual} | g={g_actual}, h={h_actual}, f={f_actual}")

            # ¿Llegamos al queso?
            if actual == self.objetivo:
                tiempo_total = time.time() - inicio_tiempo
                camino = self.reconstruir_camino(padres, self.inicio, self.objetivo)

                print(f"\n¡QUESO ENCONTRADO! 🧀")
                print(f"Nodos explorados: {nodos_explorados}")
                print(f"Longitud del camino: {len(camino)}")
                print(f"Costo total: {g_actual}")
                print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
                print(f"Camino: {' -> '.join(map(str, camino))}")

                return camino, nodos_explorados

            # Explorar vecinos
            for vecino in self.obtener_vecinos(actual):
                nuevo_g = g_actual + 1

                if vecino not in g_score or nuevo_g < g_score[vecino]:
                    g_score[vecino] = nuevo_g
                    h = self.heuristica_manhattan(vecino)
                    f = nuevo_g + h

                    contador += 1
                    heapq.heappush(cola_prioridad, (f, contador, vecino))
                    padres[vecino] = actual

        print("No se encontró camino al queso 😢")
        return None, nodos_explorados

    def visualizar_camino(self, camino, nombre_metodo):
        """Visualiza el laberinto con el camino encontrado"""
        print(f"\n{'='*60}")
        print(f"VISUALIZACIÓN DEL CAMINO - {nombre_metodo}")
        print(f"{'='*60}")

        # Crear copia del laberinto
        laberinto_visual = []
        for fila in self.matriz:
            laberinto_visual.append(list(fila))

        # Marcar el camino
        if camino:
            for i, pos in enumerate(camino):
                fila, col = pos
                if laberinto_visual[fila][col] not in ['R', 'Q']:
                    laberinto_visual[fila][col] = '·'

        # Imprimir
        for fila in laberinto_visual:
            fila_str = ''
            for celda in fila:
                if celda == 1:
                    fila_str += '█ '
                elif celda == 'R':
                    fila_str += 'R '
                elif celda == 'Q':
                    fila_str += 'Q '
                elif celda == '·':
                    fila_str += '· '
                else:
                    fila_str += '  '
            print(fila_str)
        print()


# EJEMPLO DE USO
if __name__ == "__main__":
    # Definir el laberinto
    # R = Ratón (inicio), Q = Queso (objetivo)
    # 0 = Camino libre, 1 = Pared
    laberinto_matriz = [
        ['R', 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 'Q']
    ]

    # Crear laberinto
    laberinto = Laberinto(laberinto_matriz)

    print("🐭 PROBLEMA DEL RATÓN HAMBRIENTO 🧀")
    print("El ratón debe encontrar el camino al queso...")

    # Método 1: Búsqueda en Anchura
    camino_bfs, nodos_bfs = laberinto.busqueda_anchura()
    if camino_bfs:
        laberinto.visualizar_camino(camino_bfs, "BFS")

    # Método 2: Búsqueda A*
    camino_a_star, nodos_a_star = laberinto.busqueda_a_estrella()
    if camino_a_star:
        laberinto.visualizar_camino(camino_a_star, "A*")

    # Comparación
    print("="*60)
    print("COMPARACIÓN DE MÉTODOS")
    print("="*60)
    print(f"BFS - Nodos explorados: {nodos_bfs}")
    print(f"A*  - Nodos explorados: {nodos_a_star}")
    print(f"\nA* exploró {nodos_bfs - nodos_a_star} nodos menos que BFS")
    print(f"Eficiencia de A*: {(1 - nodos_a_star/nodos_bfs)*100:.1f}% más eficiente")
