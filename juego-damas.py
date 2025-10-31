import copy
import time


class Damas:
    def __init__(self):
        """
        Inicializa el tablero de damas 8x8
        0 = casilla vacía
        1 = ficha blanca
        2 = dama blanca
        -1 = ficha negra
        -2 = dama negra
        """
        self.tablero = self.crear_tablero_inicial()
        self.turno = 1  # 1 = blancas, -1 = negras

    def crear_tablero_inicial(self):
        """Crea el tablero inicial de damas"""
        tablero = [[0 for _ in range(8)] for _ in range(8)]

        # Colocar fichas negras (arriba)
        for fila in range(3):
            for col in range(8):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = -1

        # Colocar fichas blancas (abajo)
        for fila in range(5, 8):
            for col in range(8):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = 1

        return tablero

    def imprimir_tablero(self):
        """Visualiza el tablero"""
        print("\n  ", end="")
        for i in range(8):
            print(f" {i} ", end="")
        print()

        for i, fila in enumerate(self.tablero):
            print(f"{i} ", end="")
            for celda in fila:
                if celda == 0:
                    print(" · ", end="")
                elif celda == 1:
                    print(" ○ ", end="")  # Ficha blanca
                elif celda == 2:
                    print(" ⊙ ", end="")  # Dama blanca
                elif celda == -1:
                    print(" ● ", end="")  # Ficha negra
                elif celda == -2:
                    print(" ⊗ ", end="")  # Dama negra
            print(f" {i}")

        print("  ", end="")
        for i in range(8):
            print(f" {i} ", end="")
        print("\n")

    def obtener_movimientos(self, tablero, jugador):
        """Obtiene todos los movimientos posibles para un jugador"""
        movimientos = []

        # Primero verificar si hay capturas obligatorias
        capturas = self.obtener_capturas(tablero, jugador)
        if capturas:
            return capturas

        # Si no hay capturas, movimientos normales
        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]

                # Verificar si es ficha del jugador
                if (jugador > 0 and pieza > 0) or (jugador < 0 and pieza < 0):
                    movs = self.obtener_movimientos_pieza(tablero, fila, col, pieza)
                    movimientos.extend(movs)

        return movimientos

    def obtener_movimientos_pieza(self, tablero, fila, col, pieza):
        """Obtiene movimientos de una pieza específica"""
        movimientos = []
        es_dama = abs(pieza) == 2

        if pieza > 0:  # Blancas (mueven hacia arriba)
            direcciones = [(-1, -1), (-1, 1)]
            if es_dama:
                direcciones.extend([(1, -1), (1, 1)])
        else:  # Negras (mueven hacia abajo)
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
        """Obtiene todas las capturas posibles"""
        capturas = []

        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]

                if (jugador > 0 and pieza > 0) or (jugador < 0 and pieza < 0):
                    caps = self.obtener_capturas_pieza(tablero, fila, col, pieza)
                    capturas.extend(caps)

        return capturas

    def obtener_capturas_pieza(self, tablero, fila, col, pieza):
        """Obtiene capturas de una pieza específica"""
        capturas = []
        es_dama = abs(pieza) == 2

        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for df, dc in direcciones:
            # Posición de la pieza enemiga
            enemigo_fila = fila + df
            enemigo_col = col + dc

            # Posición de destino (después de saltar)
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

                # Verificar que haya enemigo y destino vacío
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
        """Aplica un movimiento al tablero"""
        nuevo_tablero = copy.deepcopy(tablero)
        desde_fila, desde_col = movimiento["desde"]
        hasta_fila, hasta_col = movimiento["hasta"]

        pieza = nuevo_tablero[desde_fila][desde_col]
        nuevo_tablero[desde_fila][desde_col] = 0
        nuevo_tablero[hasta_fila][hasta_col] = pieza

        # Si hay captura, eliminar pieza capturada
        if movimiento["captura"]:
            cap_fila, cap_col = movimiento["captura"]
            nuevo_tablero[cap_fila][cap_col] = 0

        # Coronar si llega al final
        if pieza == 1 and hasta_fila == 0:
            nuevo_tablero[hasta_fila][hasta_col] = 2
        elif pieza == -1 and hasta_fila == 7:
            nuevo_tablero[hasta_fila][hasta_col] = -2

        return nuevo_tablero

    def evaluar_tablero(self, tablero):
        """
        Función de evaluación del tablero
        Positivo = ventaja blancas
        Negativo = ventaja negras
        """
        puntuacion = 0

        for fila in range(8):
            for col in range(8):
                pieza = tablero[fila][col]

                if pieza == 1:  # Ficha blanca
                    puntuacion += 10
                    puntuacion += fila  # Bonificación por avance
                elif pieza == 2:  # Dama blanca
                    puntuacion += 30
                elif pieza == -1:  # Ficha negra
                    puntuacion -= 10
                    puntuacion -= 7 - fila  # Bonificación por avance
                elif pieza == -2:  # Dama negra
                    puntuacion -= 30

        return puntuacion

    def es_terminal(self, tablero, jugador):
        """Verifica si el juego terminó"""
        movimientos = self.obtener_movimientos(tablero, jugador)
        return len(movimientos) == 0

    def minimax(self, tablero, profundidad, maximizando, jugador):
        """
        ALGORITMO MINIMAX
        - Explora todos los movimientos posibles
        - No usa optimizaciones
        - Más lento pero didáctico
        """
        # Caso base
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
        """
        ALGORITMO ALFABETA (Poda Alfa-Beta)
        - Optimización de Minimax
        - Poda ramas que no afectan la decisión
        - Mucho más eficiente
        """
        # Caso base
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

                # PODA: Si beta <= alfa, no explorar más
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

                # PODA: Si beta <= alfa, no explorar más
                if beta <= alfa:
                    break

            return min_eval, mejor_mov


def jugar_demo():
    """Demostración del juego con ambos algoritmos"""
    print("=" * 70)
    print("🎮 JUEGO DE DAMAS - COMPARACIÓN DE ALGORITMOS 🎮")
    print("=" * 70)

    juego = Damas()

    print("\n📋 TABLERO INICIAL:")
    juego.imprimir_tablero()

    profundidad = 4  # Profundidad de búsqueda

    print(f"\n🔍 PROFUNDIDAD DE BÚSQUEDA: {profundidad}")
    print("🤍 Blancas (jugador maximizante)")
    print("🖤 Negras (jugador minimizante)")

    # MÉTODO 1: MINIMAX
    print("\n" + "=" * 70)
    print("🔵 MÉTODO 1: MINIMAX (Sin optimización)")
    print("=" * 70)

    inicio = time.time()
    eval_minimax, mov_minimax = juego.minimax(juego.tablero, profundidad, True, 1)
    tiempo_minimax = time.time() - inicio

    print(f"\n⏱️  Tiempo de ejecución: {tiempo_minimax:.4f} segundos")
    print(f"📊 Evaluación del tablero: {eval_minimax}")

    if mov_minimax:
        print(f"🎯 Mejor movimiento encontrado:")
        print(f"   Desde: {mov_minimax['desde']}")
        print(f"   Hasta: {mov_minimax['hasta']}")
        if mov_minimax["captura"]:
            print(f"   ¡Captura en: {mov_minimax['captura']}!")

        # Aplicar movimiento
        tablero_minimax = juego.aplicar_movimiento(juego.tablero, mov_minimax)
        print("\n📋 TABLERO DESPUÉS DEL MOVIMIENTO (Minimax):")
        juego_temp = Damas()
        juego_temp.tablero = tablero_minimax
        juego_temp.imprimir_tablero()

    # MÉTODO 2: ALFABETA
    print("\n" + "=" * 70)
    print("🟢 MÉTODO 2: ALFABETA (Con poda)")
    print("=" * 70)

    inicio = time.time()
    eval_alfabeta, mov_alfabeta = juego.alfabeta(
        juego.tablero, profundidad, float("-inf"), float("inf"), True, 1
    )
    tiempo_alfabeta = time.time() - inicio

    print(f"\n⏱️  Tiempo de ejecución: {tiempo_alfabeta:.4f} segundos")
    print(f"📊 Evaluación del tablero: {eval_alfabeta}")

    if mov_alfabeta:
        print(f"🎯 Mejor movimiento encontrado:")
        print(f"   Desde: {mov_alfabeta['desde']}")
        print(f"   Hasta: {mov_alfabeta['hasta']}")
        if mov_alfabeta["captura"]:
            print(f"   ¡Captura en: {mov_alfabeta['captura']}!")

        # Aplicar movimiento
        tablero_alfabeta = juego.aplicar_movimiento(juego.tablero, mov_alfabeta)
        print("\n📋 TABLERO DESPUÉS DEL MOVIMIENTO (Alfabeta):")
        juego_temp = Damas()
        juego_temp.tablero = tablero_alfabeta
        juego_temp.imprimir_tablero()

    # COMPARACIÓN
    print("\n" + "=" * 70)
    print("📈 COMPARACIÓN DE RENDIMIENTO")
    print("=" * 70)

    print(f"\n⏱️  Minimax:  {tiempo_minimax:.4f} segundos")
    print(f"⏱️  Alfabeta: {tiempo_alfabeta:.4f} segundos")

    if tiempo_minimax > tiempo_alfabeta:
        aceleracion = tiempo_minimax / tiempo_alfabeta
        mejora = ((tiempo_minimax - tiempo_alfabeta) / tiempo_minimax) * 100
        print(f"\n🚀 Alfabeta es {aceleracion:.2f}x más rápido")
        print(f"💡 Mejora de eficiencia: {mejora:.1f}%")

    print(
        f"\n✅ Ambos algoritmos encontraron la misma evaluación: {eval_minimax == eval_alfabeta}"
    )

    print("\n" + "=" * 70)
    print("🎓 CONCLUSIONES")
    print("=" * 70)
    print("• Minimax explora TODOS los nodos del árbol de juego")
    print("• Alfabeta PODA ramas que no afectan la decisión final")
    print("• Ambos encuentran el mismo mejor movimiento")
    print("• Alfabeta es mucho más eficiente en tiempo")
    print("=" * 70)


if __name__ == "__main__":
    jugar_demo()
