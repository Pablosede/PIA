# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:46:30 2022

@author: ilopez
"""

import numpy as np
import random
import math

class Tablero:
    """
          Responsabilidades: 
              - Almacenar la ED del tablero como una matriz numpy
              - Saber colocar nuevas fichas (echarFicha) sobre una columna (filaLibre)
              - Sabe imprimirse
              - Sabe sus columnas libres
              - Sabe si hay un movimiento ganador para un jugador determinado 
              - Sabe puntuar un movimiento para la IA (evaluarVentana+puntuarPosicion)
    """
    NUM_FILAS=6
    NUM_COLUMNAS=7
    VACIA = 0
    TAM_VENTANA = 4
    FICHA_HUMANO = 1
    FICHA_IA = 2
    tablero=[]
    
    def __init__(self,n_filas,n_columnas, fichaHumano=1,fichaIA=2):
        self.NUM_FILAS = n_filas 
        self.NUM_COLUMNAS = n_columnas
        self.FICHA_HUMANO=fichaHumano
        self.FICHA_IA=fichaIA
        self.crearTablero()
        
    def crearTablero(self):
        self.tablero= np.zeros((self.NUM_FILAS,self.NUM_COLUMNAS))
        
    def copia(self):
        copia=Tablero(self.NUM_FILAS,self.NUM_COLUMNAS,self.FICHA_HUMANO,self.FICHA_IA)
        copia.tablero=self.tablero.copy()
        return copia
    	
    def filaLibre(self, col):
        for r in range(self.NUM_FILAS):
            if self.tablero[r][col] == 0:
                return r
    def echarFicha(self, col, ficha):
        self.tablero[self.filaLibre(col)][col] = ficha        
        
    def columnaLibre(self, col):
        return self.tablero[self.NUM_FILAS-1][col] == 0

    def imprime(self):
        print(np.flip(self.tablero, 0))
        
    def columnasLibres(self):
        columnasValidas = []
        for col in range(self.NUM_COLUMNAS):
            if self.columnaLibre(col):
                columnasValidas.append(col)
        return columnasValidas
    
    def movimientoGanador(self, ficha):
        # Comprueba ubicaciones para ganar en horizontal
        for c in range(self.NUM_COLUMNAS-3):
            for r in range(self.NUM_FILAS):
                if self.tablero[r][c] == ficha and self.tablero[r][c+1] == ficha \
                  and self.tablero[r][c+2] == ficha and self.tablero[r][c+3] == ficha:
                    return True

        # Comprueba ubicaciones para ganar en vertical
        for c in range(self.NUM_COLUMNAS):
            for r in range(self.NUM_FILAS-3):
                if self.tablero[r][c] == ficha and self.tablero[r+1][c] == ficha \
                  and self.tablero[r+2][c] == ficha and self.tablero[r+3][c] == ficha:
                    return True

        # Comprueba ubicaciones para ganar en diagonales ascendentes
        for c in range(self.NUM_COLUMNAS-3):
            for r in range(self.NUM_FILAS-3):
                if self.tablero[r][c] == ficha and self.tablero[r+1][c+1] == ficha \
                  and self.tablero[r+2][c+2] == ficha and self.tablero[r+3][c+3] == ficha:
                    return True

        # Comprueba ubicaciones para ganar en diagonales descendentes
        for c in range(self.NUM_COLUMNAS-3):
            for r in range(3, self.NUM_FILAS):
                if self.tablero[r][c] == ficha and self.tablero[r-1][c+1] == ficha \
                  and self.tablero[r-2][c+2] == ficha and self.tablero[r-3][c+3] == ficha:
                    return True
                
    def evaluaVentana(self,ventana, ficha):
        score = 0
        ficha_oponente = self.FICHA_HUMANO
        if ficha == self.FICHA_HUMANO:
            ficha_oponente = self.FICHA_AI

        if ventana.count(ficha) == 4:
            score += 100
        elif ventana.count(ficha) == 3 and ventana.count(self.VACIA) == 1:
            score += 5
        elif ventana.count(ficha) == 2 and ventana.count(self.VACIA) == 2:
            score += 2

        if ventana.count(ficha_oponente) == 3 and ventana.count(self.VACIA) == 1:
            score -= 4

        return score
    
    
    def puntuarPosicion(self,ficha):
        score = 0
        ## Puntuar las fichas en la columnaa central
        columna_central = [int(i) for i in list(self.tablero[:, self.NUM_COLUMNAS//2])]
        contador_centro = columna_central.count(ficha)
        score += contador_centro * 3

        ## Puntuar las horizontales
        for r in range(self.NUM_FILAS):
            fila_array = [int(i) for i in list(self.tablero[r,:])]
            for c in range(self.NUM_COLUMNAS-3):
                ventana = fila_array[c:c+self.TAM_VENTANA]
                score += self.evaluaVentana(ventana, ficha)

        ## Puntuar las verticales
        for c in range(self.NUM_COLUMNAS):
            col_array = [int(i) for i in list(self.tablero[:,c])]
            for r in range(self.NUM_FILAS-3):
                ventana = col_array[r:r+self.TAM_VENTANA]
                score += self.evaluaVentana(ventana, ficha)

        ## puntuar las diagonales ascendentes
        for r in range(self.NUM_FILAS-3):
            for c in range(self.NUM_COLUMNAS-3):
                ventana = [self.tablero[r+i][c+i] for i in range(self.TAM_VENTANA)]
                score += self.evaluaVentana(ventana, ficha)

        ## puntuar las diagonales descendentes
        for r in range(self.NUM_FILAS-3):
            for c in range(self.NUM_COLUMNAS-3):
                ventana = [self.tablero[r+3-i][c+i] for i in range(self.TAM_VENTANA)]
                score += self.evaluaVentana(ventana, ficha)

        return score
    
    
    

class Conecta4:
    """
          Responsabilidades: 
              - detectar fin de partida
              - Implementar minimax con poda alfa-beta con un nivel de profundidad
              - Tomar la decisión del mejor camino minimax (elegirMejorMovimiento)
              - Sabe sus columnas libres
              - Comenzar y Gestionar el Juego 
    """
    game_over=False
    PROFUNDIDAD_MAX = 3
    
    FICHA_HUMANO = 1
    FICHA_IA = 2
    turno=2
    
    
    def __init__(self,profundidad):
        self.PROFUNDIDAD_MAX = profundidad
    
    def fin_partida(self,tablero):
        return tablero.movimientoGanador(self.FICHA_HUMANO) or \
            tablero.movimientoGanador(self.FICHA_IA) or len(tablero.columnasLibres()) == 0
    
    def minimax(self,tablero, profundidad, alpha, beta, maximizandoHumano):
        columnasValidas = tablero.columnasLibres()
        fin_partida = self.fin_partida(tablero)

        #caso base 1
        if fin_partida:
            if tablero.movimientoGanador(self.FICHA_IA):
                return (None, 100000000000000)  #inf
            elif tablero.movimientoGanador(self.FICHA_HUMANO):
                return (None, -10000000000000)  #-inf
            else: # Game over, no hay más movimientos válidos
                return (None, 0)
            
        #caso base 2
        if profundidad==0: # profundidad cero
                return (None, tablero.puntuarPosicion(self.FICHA_IA))
            
        if maximizandoHumano:
            valor = -math.inf
            columna = random.choice(columnasValidas)
            for col in columnasValidas:
                copiaTablero = tablero.copia()
                copiaTablero.echarFicha(col, copiaTablero.FICHA_IA)
                new_score = self.minimax(copiaTablero, profundidad-1, alpha, beta, False)[1]
                if new_score > valor:
                    valor = new_score
                    columna = col
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break
            return columna, valor

        else: # Minimizando humano
            valor = math.inf
            columna = random.choice(columnasValidas)
            for col in columnasValidas:
                copiaTablero = tablero.copia()
                copiaTablero.echarFicha(col, copiaTablero.FICHA_HUMANO)
                new_score = self.minimax(copiaTablero, profundidad-1, alpha, beta, True)[1]
                if new_score < valor:
                    valor = new_score
                    columna = col
                beta = min(beta, valor)
                if alpha >= beta:
                    break
            return columna, valor
        

    
    def cambiaTurno(self):
        if self.turno == self.FICHA_IA:
            self.turno = self.FICHA_HUMANO
        else:
            self.turno = self.FICHA_IA
            
    def jugar(self):
        tablero = Tablero(6,7,self.FICHA_HUMANO,self.FICHA_IA)
        print("NUEVA PARTIDA!")
        tablero.imprime()
        aleat= random.randint(self.FICHA_HUMANO, self.FICHA_IA)
        self.turno =aleat
        print("turno inicial",self.turno)
        self.game_over=False

        while not self.game_over:            
            if self.turno == self.FICHA_HUMANO:
                print("TURNO DEL HUMANO (ficha 1):")
                col=-1
                while col <0 or col>6:
                    col=int(input("introduce columna:"))
                
                if tablero.columnaLibre(col):
                    tablero.echarFicha(col, self.FICHA_HUMANO)

                    if tablero.movimientoGanador(self.FICHA_HUMANO):
                        print("HUMANO gana!!")
                        self.game_over = True

                    self.cambiaTurno()
                    tablero.imprime()
                else:
                    print("ubicación no válida")


            # mueve el jugador 2
            if self.turno == self.FICHA_IA and not self.game_over:				
                col, minimax_score = self.minimax(tablero, self.PROFUNDIDAD_MAX, -math.inf, math.inf, True)

                if tablero.columnaLibre(col):
                    
                    print("TURNO IA (ficha 2): [Elige {}]".format(col))
                    tablero.echarFicha(col,self.FICHA_IA)

                    if tablero.movimientoGanador(self.FICHA_IA):
                        print("I.A. gana!!")
                        self.game_over = True

                    tablero.imprime()
                    self.cambiaTurno()

juego=Conecta4(5) #un conecta 4 con profundidad 5, ficha para el humano 1, ficha para la IA 2
juego.jugar()

        
        

