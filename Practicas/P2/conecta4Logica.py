# Asignatura: Inteligencia Artificial
# Practica 2
# Alumnos:  Juan Mario Sosa Romo
# 
# Descripcion: Implementacion del juego Conecta 4
#
# Referencias:
# https://youtu.be/UYgyRArKDEs?si=oFdGIPmDG5r3HyRs 

import numpy as np
import pygame

class Conecta4:
    def __init__(self, screen):
        self.tablero = np.zeros((6,7))
        self.jugador = np.random.randint(1,3)
        self.juegoTerminado = False
        self.font = pygame.font.SysFont("monospace",60)
        self.screen = screen

    def __str__(self):
        return str(self.tablero)
    
    def __ganador(self,fila,columna):
        return self.__ganadorHorizontal(fila) or self.__ganadorVertical(columna) or self.__ganadorDiagonal(fila,columna)

    def __ganadorHorizontal(self,fila):
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

        pygame.time.wait(200)
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
            print("Empate")
            self.juegoTerminado = True
            return

        # Si no hay ganador, cambiamos de jugador
        self.jugador = 1 if self.jugador == 2 else 2
        
    
    def dibujarHover(self, pos):
        pygame.draw.rect(self.screen, (0,0,0), (0,0,7*100,100))
        if self.jugador == 1:
            pygame.draw.circle(self.screen, (255,0,0), (pos, 50), 45)
        else:
            pygame.draw.circle(self.screen, (255,255,0), (pos, 50), 45)
        pygame.display.update()
        
    def dibujar(self):
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
        posicion = 0
        
        # Función auxiliar para evaluar una ventana y verificar si los espacios son jugables
        def evaluar_ventana(ventana, posiciones_reales):
            puntos = 0
            # Ganar inmediatamente (4 en línea)
            if ventana.count(jugador) == 4:
                puntos += 100000
            
            # Alta prioridad para 3 en línea con espacio para ganar
            elif ventana.count(jugador) == 3 and ventana.count(0) == 1:
                # Identificar la posición del espacio vacío
                espacio_vacio_indice = ventana.index(0)
                fila_real, col_real = posiciones_reales[espacio_vacio_indice]
                
                # Verificar si el espacio vacío es jugable
                if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                    puntos += 50000
            
            # Prioridad media para 2 en línea
            elif ventana.count(jugador) == 2 and ventana.count(0) == 2:
                for i in range(4):
                    if ventana[i] == 0:
                        fila_real, col_real = posiciones_reales[i]
                        
                        if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                            puntos += 1000
            
            return puntos
        
        # Evaluación horizontal
        for fila in range(6):
            for columna in range(4):
                ventana = [tablero[fila][columna+i] for i in range(4)]
                posiciones = [(fila, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones)
        
        # Evaluación vertical
        for columna in range(7):
            for fila in range(3):
                ventana = [tablero[fila+i][columna] for i in range(4)]
                # Para vertical, necesitamos verificación especial de jugabilidad
                # Un espacio es jugable solo si todos los espacios debajo están ocupados
                ventana_puntos = 0
                
                # Verificar victoria inmediata
                if ventana.count(jugador) == 4:
                    ventana_puntos += 100000
                
                # Verificar 3 en línea
                elif ventana.count(jugador) == 3 and ventana.count(0) == 1:
                    espacio_vacio_indice = ventana.index(0)
                    fila_real = fila + espacio_vacio_indice
                    
                    # Un espacio es jugable en vertical si está en la parte más baja disponible
                    es_jugable = True
                    for i in range(fila_real + 1, 6):
                        if tablero[i][columna] == 0:
                            es_jugable = False
                            break
                    
                    if es_jugable:
                        ventana_puntos += 50000
                
                # Verificar 2 en línea
                elif ventana.count(jugador) == 2 and ventana.count(0) == 2:
                    for i in range(4):
                        if ventana[i] == 0:
                            fila_real = fila + i
                            
                            # Verificar jugabilidad
                            es_jugable = True
                            for j in range(fila_real + 1, 6):
                                if tablero[j][columna] == 0:
                                    es_jugable = False
                                    break
                            
                            if es_jugable:
                                ventana_puntos += 1000
                
                posicion += ventana_puntos
        
        # Evaluación diagonal descendente (\)
        for fila in range(3):
            for columna in range(4):
                ventana = [tablero[fila+i][columna+i] for i in range(4)]
                posiciones = [(fila+i, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones)
        
        # Evaluación diagonal ascendente (/)
        for fila in range(3):
            for columna in range(4):
                ventana = [tablero[fila+3-i][columna+i] for i in range(4)]
                posiciones = [(fila+3-i, columna+i) for i in range(4)]
                posicion += evaluar_ventana(ventana, posiciones)
        
        # Preferencia para jugar en el centro
        centro_columna = 3
        if self.__esValida(centro_columna, tablero):
            posicion += 500
        
        return posicion
    
    def evaluar_ventana(self, ventana, posiciones_reales, tablero, jugador):
        puntos = 0
        
        if ventana.count(jugador) == 4:
            puntos += 100000
        
        elif ventana.count(jugador) == 3 and ventana.count(0) == 1:
            espacio_vacio_indice = ventana.index(0)
            fila_real, col_real = posiciones_reales[espacio_vacio_indice]
            
            if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                puntos += 50000
        
        elif ventana.count(jugador) == 2 and ventana.count(0) == 2:
            for i in range(4):
                if ventana[i] == 0:
                    fila_real, col_real = posiciones_reales[i]
                    
                    if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                        puntos += 1000
        
        elif ventana.count(jugador) == 1 and ventana.count(0) == 3:
            for i in range(4):
                if ventana[i] == 0:
                    fila_real, col_real = posiciones_reales[i]
                    
                    if fila_real == 5 or (fila_real < 5 and tablero[fila_real+1][col_real] != 0):
                        puntos += 100
        
        return puntos
    
    def __eligeMejorJugada(self, tablero, jugador):
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
        jugadas = []     
        for columna in range(7):
            if self.__esValida(columna,tablero):
                jugadas.append(columna)
        return jugadas
    
    def __esValida(self, columna, tablero):
        return tablero[0][columna] == 0
        

    def jugarIA(self, dificultad):
        if dificultad == "null": 
            self.jugar(np.random.randint(0,7)) 
        elif dificultad == "facil":
            self.jugar(self.__eligeMejorJugada(self.tablero,self.jugador))
        elif dificultad == "medio":
            pass
        elif dificultad == "dificil":
            pass
        else:
            print("Dificultad invalida")
            return