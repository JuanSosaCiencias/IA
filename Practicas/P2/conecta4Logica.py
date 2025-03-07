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
    def __init__(self):
        self.tablero = np.zeros((6,7))
        self.jugador = 1
        self.juegoTerminado = False

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

        # Verifico si hay un ganador
        if self.__ganador(fila,columna):
            print(self)
            print(f"Jugador {self.jugador} ha ganado")
            self.juegoTerminado = True
            return 
        
        # Verifico si hay empate
        if np.all(self.tablero != 0):
            print("Empate")
            self.juegoTerminado = True
            return

        # Si no hay ganador, cambiamos de jugador
        self.jugador = 1 if self.jugador == 2 else 2
        
    def dibujar(self, screen):
        for fila in range(6):
            for columna in range(7):
                pygame.draw.rect(screen, (0,0,255), (columna * 100, 100 + fila * 100, 100, 100))
                pygame.draw.circle(screen, (0,0,0), (50 + columna * 100,150+ fila * 100), 45)
                