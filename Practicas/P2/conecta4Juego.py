# Autor: Juan Mario Sosa Romo
#
# Descripcion: Aqui se gestiona la sesion del juego Conecta 4
# Referencias para pygame: https://youtu.be/SDz3P_Ctm7U?si=MoUaMRJYM5wcHAx3

from conecta4Logica import Conecta4
import pygame
import sys

# Cosas de pygame
pygame.init()
size = (7 * 100, 7 * 100)
screen = pygame.display.set_mode(size)

juego = Conecta4()
juego.dibujar(screen)
pygame.display.update()

while not juego.juegoTerminado:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego.juegoTerminado = True
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("hola")

    # print(juego)
    # columna = int(input(f"Jugador {juego.jugador}, en que columna del 0 al 7 quieres poner tu ficha? "))
    # juego.jugar(columna)

