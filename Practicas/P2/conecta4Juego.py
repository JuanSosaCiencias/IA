# Autor: Juan Mario Sosa Romo
#
# Descripcion: Aqui se gestiona la sesion del juego Conecta 4
# Referencias para pygame: https://youtu.be/SDz3P_Ctm7U?si=MoUaMRJYM5wcHAx3

from conecta4Logica import Conecta4
import pygame
import sys

if len(sys.argv) > 1:
    dificultad = sys.argv[1]
else:
    dificultad = "facil"

# Cosas de pygame
pygame.init()
size = (7 * 100, 7 * 100)
screen = pygame.display.set_mode(size)

juego = Conecta4(screen)
juego.dibujar()
pygame.display.update()


while not juego.juegoTerminado:
    if juego.jugador==1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego.juegoTerminado = True
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                juego.dibujarHover(event.pos[0])
            if event.type == pygame.MOUSEBUTTONDOWN:
                juego.jugar(event.pos[0] // 100)
    else:
        juego.jugarIA(dificultad)
    