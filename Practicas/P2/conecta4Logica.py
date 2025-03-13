# Asignatura: Inteligencia Artificial
# Practica 2
# Alumnos:  Juan Mario Sosa Romo
# 
# Descripcion: Implementacion del juego Conecta 4
#
# Este codigo esta extremadamente inspirado en los videos de @keithgalli
# https://youtu.be/MMLtza3CZFM?si=JQm8JRdoTkouGAvO y su serie de videos de la base

import numpy as np
import pygame

class Conecta4:
    """
    Clase que representa el juego Conecta 4

    Atributos:
    tablero: matriz de 6x7 que representa el tablero del juego
    jugador: jugador actual
    juegoTerminado: indica si el juego ha terminado
    font: fuente para mostrar mensajes
    screen: pantalla de pygame

    Metodos:
    __init__: constructor de la clase
    __str__: metodo para imprimir el tablero
    __ganador: verifica si hay un ganador
    __ganadorHorizontal: verifica si hay un ganador en horizontal
    __ganadorVertical: verifica si hay un ganador en vertical
    __ganadorDiagonal: verifica si hay un ganador en diagonal
    jugar: metodo para jugar una ficha
    dibujarHover: dibuja la ficha que se va a poner
    dibujar: dibuja el tablero
    juzgaPosicion: evalua una posicion en el tablero
    __eligeMejorJugada: elige la mejor jugada
    __obtenerJugadaValida: obtiene las jugadas validas
    __esValida: verifica si una jugada es valida
    __verificarGanador: verifica si hay un ganador en un tablero dado
    obtenerFilaDisponible: obtiene la fila disponible en una columna
    minimax: algoritmo minimax
    minimaxAlfaBeta: algoritmo minimax con poda alfa-beta
    jugarIA: juega la IA
    """

    def __init__(self, screen):
        self.tablero = np.zeros((6,7))
        self.jugador = np.random.randint(1,3)
        self.juegoTerminado = False
        self.font = pygame.font.SysFont("monospace",60)
        self.screen = screen

    def __str__(self):
        return str(self.tablero)
    
    def __ganador(self,fila,columna):
        """
        Verifica si hay un ganador en el tablero del objeto

        Parametros:
        fila: fila de la ultima jugada
        columna: columna de la ultima jugada
        """
        return self.__ganadorHorizontal(fila) or self.__ganadorVertical(columna) or self.__ganadorDiagonal(fila,columna)

    def __ganadorHorizontal(self,fila):
        """
        Verifica si hay un ganador en horizontal

        Parametros:
        fila: fila de la ultima jugada
        """
        seguidos= 0
        for columna in range(7):
            if self.tablero[fila][columna] == self.jugador:
                seguidos += 1
                if seguidos == 4:
                    return True
            else:
                seguidos = 0
        return False
    
    def __ganadorVertical(self,columna):
        """
        Verifica si hay un ganador en vertical
        
        Parametros:
        columna: columna de la ultima jugada
        """
        seguidos= 0
        for fila in range(6):
            if self.tablero[fila][columna] == self.jugador:
                seguidos += 1
                if seguidos == 4:
                    return True
            else:
                seguidos = 0
        return False

    def __ganadorDiagonal(self,fila,columna):
        """
        Verifica si hay un ganador en diagonal

        Parametros:
        fila: fila de la ultima jugada
        columna: columna de la ultima
        """
        # Diagonal hacia arriba
        seguidos = 0
        for i in range(-3,4):
            if fila + i >= 0 and fila + i < 6 and columna + i >= 0 and columna + i < 7:
                if self.tablero[fila + i][columna + i] == self.jugador:
                    seguidos += 1
                    if seguidos == 4:
                        return True
                else:
                    seguidos = 0

        # Diagonal hacia abajo
        seguidos = 0
        for i in range(-3,4):
            if fila + i >= 0 and fila + i < 6 and columna - i >= 0 and columna - i < 7:
                if self.tablero[fila + i][columna - i] == self.jugador:
                    seguidos += 1
                    if seguidos == 4:
                        return True
                else:
                    seguidos = 0
        return False
        

    def jugar(self,columna):
        """
        Metodo para jugar una ficha

        Parametros:
        columna: columna donde se va a poner la ficha
        """
        # Verificamos que la columna sea valida
        if columna < 0 or columna > 6:
            print("Columna invalida")
            return
        if self.tablero[0][columna] != 0:
            print("Columna llena")
            return
        
        # Poner ficha en la columna
        fila = 5    
        while self.tablero[fila][columna] != 0:
            fila -= 1
        self.tablero[fila][columna] = self.jugador

        self.dibujar()

        # Verifico si hay un ganador
        if self.__ganador(fila,columna):
            self.screen.blit(self.font.render("Ganador : jugador " + str(self.jugador), True, (255,255,255)), (0,0))
            pygame.display.update()
            pygame.time.wait(3000)
            self.juegoTerminado = True
            return 
        
        # Verifico si hay empate
        if np.all(self.tablero != 0):
            self.screen.blit(self.font.render("Empate", True, (255,255,255)), (0,0))
            pygame.display.update()
            pygame.time.wait(3000)
            self.juegoTerminado = True
            return

        # Si no hay ganador, cambiamos de jugador
        self.jugador = 1 if self.jugador == 2 else 2
        
    
    def dibujarHover(self, pos):
        """
        Dibuja la ficha que se va a poner

        Parametros:
        pos: posicion del mouse
        """
        pygame.draw.rect(self.screen, (0,0,0), (0,0,7*100,100))
        if self.jugador == 1:
            pygame.draw.circle(self.screen, (255,0,0), (pos, 50), 45)
        else:
            pygame.draw.circle(self.screen, (255,255,0), (pos, 50), 45)
        pygame.display.update()
        
    def dibujar(self):
        """
        Dibuja el tablero
        """
        for fila in range(6):
            for columna in range(7):
                pygame.draw.rect(self.screen, (0,0,255), (columna * 100, 100 + fila * 100, 100, 100))
                if self.tablero[fila][columna] == 0:
                    pygame.draw.circle(self.screen, (0,0,0), (50 + columna * 100,150+ fila * 100), 45)
                elif self.tablero[fila][columna] == 1:
                    pygame.draw.circle(self.screen, (255,0,0), (50 + columna * 100,150+ fila * 100), 45)
                else:
                    pygame.draw.circle(self.screen, (255,255,0), (50 + columna * 100,150+ fila * 100), 45)
        pygame.display.update()
    
    def juzgaPosicion(self, tablero, jugador):
        """
        Evalua una posicion en el tablero, asignando un puntaje
        Gran parte de este pensamiento viene en el video de @
        pero la idea es que cree un tablero virtual, juege y 
        vea si su posicion esta mejorando o empeorando.

        Los valroes de retorno son arbitrarios, pero se pueden
        ajustar para mejorar el rendimiento de la IA, idealmente
        se deberia de hacer un entrenamiento para ajustar estos
        valores.

        Parametros:
        tablero: tablero a evaluar
        jugador: jugador actual (1 o 2)
        """
        posicion = 0
        oponente = 1 if jugador == 2 else 2 
        
        def evaluar_ventana(ventana, posiciones_reales, jugador_actual):
            """
            Evalua una ventana de 4 fichas

            Parametros:
            ventana: ventana de 4 fichas
            posiciones_reales: posiciones reales de la ventana
            jugador_actual: jugador actual
            """
            puntos = 0
            if ventana.count(jugador_actual) == 4:
                puntos += 100000
            elif ventana.count(jugador_actual) == 3 and ventana.count(0) == 1:
                espacio_vacio_indice = ventana.index(0)
                fila_real, col_real = posiciones_reales[espacio_vacio_indice]
                
                if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                    if jugador_actual == jugador:
                        puntos += 50000
                    else:
                        puntos += 40000
            
            elif ventana.count(jugador_actual) == 2 and ventana.count(0) == 2:
                espacios_jugables = 0
                for i in range(4):
                    if ventana[i] == 0:
                        fila_real, col_real = posiciones_reales[i]
                        
                        if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                            espacios_jugables += 1
                            if jugador_actual == jugador:
                                puntos += 1000
                            else:
                                puntos += 800
                
                # mas flexible
                if espacios_jugables > 1 and jugador_actual == jugador:
                    puntos += 500
            
            return puntos
        
        for fila in range(6):
            for columna in range(4):
                ventana = [tablero[fila][columna+i] for i in range(4)]
                posiciones = [(fila, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones, jugador)
                posicion -= evaluar_ventana(ventana, posiciones, oponente)
        
        # Evaluación vertical
        for columna in range(7):
            for fila in range(3):
                ventana = [tablero[fila+i][columna] for i in range(4)]
                posiciones = [(fila+i, columna) for i in range(4)]
                
                
                ventana_puntos_ia = 0
                
                if ventana.count(jugador) == 4:
                    ventana_puntos_ia += 100000
                
                elif ventana.count(jugador) == 3 and ventana.count(0) == 1:
                    espacio_vacio_indice = ventana.index(0)
                    fila_real = fila + espacio_vacio_indice
                    
                    es_jugable = True
                    for i in range(fila_real + 1, 6):
                        if tablero[i][columna] == 0:
                            es_jugable = False
                            break
                    
                    if es_jugable:
                        ventana_puntos_ia += 50000
                
                elif ventana.count(jugador) == 2 and ventana.count(0) == 2:
                    for i in range(4):
                        if ventana[i] == 0:
                            fila_real = fila + i
                            
                            es_jugable = True
                            for j in range(fila_real + 1, 6):
                                if tablero[j][columna] == 0:
                                    es_jugable = False
                                    break
                            
                            if es_jugable:
                                ventana_puntos_ia += 1000
                
                posicion += ventana_puntos_ia
                
                # Evaluar defensa
                ventana_puntos_oponente = 0
                
                if ventana.count(oponente) == 4:
                    ventana_puntos_oponente += 100000
                
                elif ventana.count(oponente) == 3 and ventana.count(0) == 1:
                    espacio_vacio_indice = ventana.index(0)
                    fila_real = fila + espacio_vacio_indice
                    
                    # Un espacio es jugable en vertical si está en la parte más baja disponible
                    es_jugable = True
                    for i in range(fila_real + 1, 6):
                        if tablero[i][columna] == 0:
                            es_jugable = False
                            break
                    
                    if es_jugable:
                        ventana_puntos_oponente += 100000  
                
                elif ventana.count(oponente) == 2 and ventana.count(0) == 2:
                    for i in range(4):
                        if ventana[i] == 0:
                            fila_real = fila + i
                            
                            es_jugable = True
                            for j in range(fila_real + 1, 6):
                                if tablero[j][columna] == 0:
                                    es_jugable = False
                                    break
                            
                            if es_jugable:
                                ventana_puntos_oponente += 800 
                
                posicion -= ventana_puntos_oponente
        
        # (/)
        for fila in range(3):
            for columna in range(4):
                ventana = [tablero[fila+i][columna+i] for i in range(4)]
                posiciones = [(fila+i, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones, jugador)
                posicion -= evaluar_ventana(ventana, posiciones, oponente)
        
        # (\)
        for fila in range(3):
            for columna in range(4):
                ventana = [tablero[fila+3-i][columna+i] for i in range(4)]
                posiciones = [(fila+3-i, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones, jugador)
                posicion -= evaluar_ventana(ventana, posiciones, oponente)
        
        # Preferencia para jugar en el centro
        centro_columna = 3
        for i in range(6):
            if tablero[i][centro_columna] == 0:
                if i == 5 or tablero[i+1][centro_columna] != 0:
                    posicion += 500
                break
        
        return posicion
    
    def __eligeMejorJugada(self, tablero, jugador):
        """
        Elige la mejor jugada en el tablero

        Parametros:
        tablero: tablero a evaluar (puede no ser el del objeto)
        jugador: jugador actual (1 o 2)
        """
        jugadasValidas = self.__obtenerJugadaValida(tablero)
        
        if not jugadasValidas:
            return np.random.randint(0, 7)
        
        mejorPuntaje = -float('inf')
        mejoresColumnas = []
        
        for columna in jugadasValidas:
            fila = None
            for r in range(5, -1, -1):
                if tablero[r][columna] == 0:
                    fila = r
                    break
            
            if fila is not None:
                tableroTemp = tablero.copy()
                tableroTemp[fila][columna] = jugador
                
                puntaje = self.juzgaPosicion(tableroTemp, jugador)
                
                if puntaje > mejorPuntaje:
                    mejorPuntaje = puntaje
                    mejoresColumnas = [columna]
                elif puntaje == mejorPuntaje:
                    mejoresColumnas.append(columna)
        
        return np.random.choice(mejoresColumnas)
        
    def __obtenerJugadaValida(self, tablero):       
        """
        Obtiene las jugadas validas en el tablero

        Parametros:
        tablero: tablero a evaluar
        """
        jugadas = []     
        for columna in range(7):
            if self.__esValida(columna,tablero):
                jugadas.append(columna)
        return jugadas
    
    def __esValida(self, columna, tablero):
        """
        Verifica si una jugada es valida

        Parametros:
        columna: columna a evaluar
        tablero: tablero a evaluar
        """
        return tablero[0][columna] == 0
    
    def __verificarGanador(self, tablero, jugador):
        """
        Verifica si hay un ganador en un tablero dado

        Parametros:
        tablero: tablero a evaluar
        jugador: jugador a verificar
        """
        # Verificar horizontal
        for fila in range(6):
            for columna in range(4):
                if all(tablero[fila][columna+i] == jugador for i in range(4)):
                    return True
                    
        # Verificar vertical
        for fila in range(3):
            for columna in range(7):
                if all(tablero[fila+i][columna] == jugador for i in range(4)):
                    return True
                    
        # Verificar diagonal (/)
        for fila in range(3):
            for columna in range(4):
                if all(tablero[fila+i][columna+i] == jugador for i in range(4)):
                    return True
                    
        # Verificar diagonal (\)
        for fila in range(3, 6):
            for columna in range(4):
                if all(tablero[fila-i][columna+i] == jugador for i in range(4)):
                    return True
                    
        return False
    
    def __esTerminal(self, tablero):
        """
        Verifica si el tablero es terminal

        Parametros:
        tablero: tablero a evaluar
        """
        return self.__verificarGanador(tablero, 1) or self.__verificarGanador(tablero, 2) or np.all(tablero != 0)

    def obtenerFilaDisponible(self, tablero, columna):
        """
        Obtiene la fila disponible en una columna

        Parametros:
        tablero: tablero a evaluar
        columna: columna a evaluar  
        """
        for fila in range(5, -1, -1):
            if tablero[fila][columna] == 0:
                return fila
        return -1

    def minimax(self, tablero, profundidad, maximizando):
        """
        Algoritmo minimax para la IA sin poda alfa-beta
        Gran parte del codigo otra vez es del video

        Parametros:
        tablero: tablero a evaluar
        profundidad: profundidad de la busqueda
        maximizando: indica si es el turno de la IA
        """
        # Casos base
        if profundidad == 0 or self.__esTerminal(tablero):
            if self.__esTerminal(tablero):
                if self.__verificarGanador(tablero, 2):  # IA gana
                    return (None, 1000000)
                elif self.__verificarGanador(tablero, 1):  # Jugador gana
                    return (None, -1000000)
                else:  # Empate
                    return (None, 0)
            else:
                # Evaluación heurística
                return (None, self.juzgaPosicion(tablero, 2))
        
        # Si no hay validas podemos acabar
        jugadas_validas = self.__obtenerJugadaValida(tablero)
        if not jugadas_validas:
            return (None, 0)
            
        if maximizando:  # Turno de la IA (jugador 2)
            valor = -float('inf')

            # Empezamos por una aleatoria
            columna_elegida = np.random.choice(jugadas_validas)
            
            for columna in jugadas_validas:
                fila = self.obtenerFilaDisponible(tablero, columna)
                if fila == -1:  # Columna llena
                    continue
                    
                tablero_temp = tablero.copy()
                tablero_temp[fila][columna] = 2  # IA juega
                
                # Llamada recursiva
                nuevo_valor = self.minimax(tablero_temp, profundidad-1, False)[1]
                
                # Si obtenemos un valor mejor, lo guardamos
                if nuevo_valor > valor:
                    valor = nuevo_valor
                    columna_elegida = columna
                    
            return columna_elegida, valor
            
        else:  # Turno del jugador (jugador 1)
            valor = float('inf')
            columna_elegida = np.random.choice(jugadas_validas)
            
            for columna in jugadas_validas:
                fila = self.obtenerFilaDisponible(tablero, columna)
                if fila == -1:  # Columna llena
                    continue
                    
                tablero_temp = tablero.copy()
                tablero_temp[fila][columna] = 1  # Jugador juega
                
                # Llamada recursiva
                nuevo_valor = self.minimax(tablero_temp, profundidad-1, True)[1]
                
                # Si obtenemos un valor menor lo guarda porque el jugador es el minimizador
                if nuevo_valor < valor:
                    valor = nuevo_valor
                    columna_elegida = columna
                    
            return columna_elegida, valor

    def minimaxAlfaBeta(self, tablero, profundidad, alpha, beta, maximizando):
        """
        Algoritmo minimax para la IA con poda alfa-beta, este es muy parecido al anterior
        solo que elimina las ramas que no son racionales para la IA

        Parametros:
        tablero: tablero a evaluar
        profundidad: profundidad de la busqueda
        alpha: valor de alpha
        beta: valor de beta 
        maximizando: indica si es el turno de la IA
        """
        # Casos base
        if profundidad == 0 or self.__esTerminal(tablero):
            if self.__esTerminal(tablero):
                if self.__verificarGanador(tablero, 2):  # IA gana
                    return (None, 1000000)
                elif self.__verificarGanador(tablero, 1):  # Jugador gana
                    return (None, -1000000)
                else:  # Empate
                    return (None, 0)
            else:
                # Evaluación heurística
                return (None, self.juzgaPosicion(tablero, 2))
        
        jugadas_validas = self.__obtenerJugadaValida(tablero)
        if not jugadas_validas:
            return (None, 0)
            
        if maximizando:  # Turno de la IA (jugador 2)
            valor = -float('inf')
            columna_elegida = np.random.choice(jugadas_validas)
            
            for columna in jugadas_validas:
                fila = self.obtenerFilaDisponible(tablero, columna)
                if fila == -1:  # Columna llena
                    continue
                    
                tablero_temp = tablero.copy()
                tablero_temp[fila][columna] = 2  # IA juega
                
                # Llamada recursiva
                nuevo_valor = self.minimaxAlfaBeta(tablero_temp, profundidad-1, alpha, beta, False)[1]
                
                if nuevo_valor > valor:
                    valor = nuevo_valor
                    columna_elegida = columna
                
                # Poda alfa-beta, hasta antes de esto es igualito
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break
                    
            return columna_elegida, valor
            
        else:  # Turno del jugador (jugador 1)
            valor = float('inf')
            columna_elegida = np.random.choice(jugadas_validas)
            
            for columna in jugadas_validas:
                fila = self.obtenerFilaDisponible(tablero, columna)
                if fila == -1:  # Columna llena
                    continue
                    
                tablero_temp = tablero.copy()
                tablero_temp[fila][columna] = 1  # Jugador juega
                
                # Llamada recursiva
                nuevo_valor = self.minimaxAlfaBeta(tablero_temp, profundidad-1, alpha, beta, True)[1]
                
                if nuevo_valor < valor:
                    valor = nuevo_valor
                    columna_elegida = columna
                
                # Poda alfa-beta
                beta = min(beta, valor) # como vemos aca usamos el min por lo mismo
                if alpha >= beta:
                    break
                    
            return columna_elegida, valor

    def jugarIA(self, dificultad):
        """
        Maneja la logica de como juega la ia

        Parametros:
        dificultad: dificultad de la IA
        """

        # Mis dificultades
        if dificultad == "null": 
            self.jugar(np.random.randint(0, 7))

        # De aqui en adelante, esta demasiado fuerte    
        elif dificultad == "de compas":
            self.jugar(self.__eligeMejorJugada(self.tablero, self.jugador))
        elif dificultad == "trivial":
            columna = self.minimaxAlfaBeta(self.tablero, 8, -float('inf'), float('inf'), True)[0]
            self.jugar(columna)
        
        # Dificultades oficiales
        elif dificultad == "facil":
            columna = self.minimax(self.tablero, 3, True)[0]
            self.jugar(columna)
        elif dificultad == "medio":
            columna = self.minimaxAlfaBeta(self.tablero, 5, -float('inf'), float('inf'), True)[0]
            self.jugar(columna)
        elif dificultad == "dificil":
            columna = self.minimaxAlfaBeta(self.tablero, 7, -float('inf'), float('inf'), True)[0]
            self.jugar(columna)
        else:
            print("Dificultad invalida")
            return