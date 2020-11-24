import pandas as pd
import numpy as np

# Nota: para crear celdas utilziar "#%%"
estados = ['e', 'h', 's', 'v', 'g', 'c', 'b', 'x']


class sistema():

    def __init__(self,fA, fB):
        self.fA = fA
        self.fB = fB

    def crearMatricesProbabilidadTransición(self):
        # Mariz de Probabilidad de Transición de usuarios tipo A
        p_A = pd.DataFrame(index=estados, columns=estados, dtype=float)
        p_A.loc['e'] = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        p_A.loc['h'] = [0.0, 0.0, 0.7, 0.0, 0.1, 0.0, 0.0, 0.2]
        p_A.loc['s'] = [0.0, 0.0, 0.4, 0.2, 0.15, 0.0, 0.0, 0.25]
        p_A.loc['v'] = [0.0, 0.0, 0.0, 0.0, 0.65, 0.0, 0.0, 0.35]
        p_A.loc['g'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.6, 0.1]
        p_A.loc['c'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        p_A.loc['b'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        p_A.loc['x'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.p_A = p_A

        # Mariz de Probabilidad de Transición de usuarios tipo B
        p_B = pd.DataFrame(index=estados, columns=estados, dtype=float)
        p_B.loc['e'] = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        p_B.loc['h'] = [0.0, 0.0, 0.7, 0.0, 0.1, 0.0, 0.0, 0.2]
        p_B.loc['s'] = [0.0, 0.0, 0.45, 0.15, 0.1, 0.0, 0.0, 0.3]
        p_B.loc['v'] = [0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.6]
        p_B.loc['g'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.55, 0.15]
        p_B.loc['c'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        p_B.loc['b'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        p_B.loc['x'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.p_B = p_B

        return

    def calcularFrecuenciaOperaciones(self):
        #Calculo frecuencia de operaciones para usuario tipo A
        A = self.p_A.to_numpy().transpose()
        diagonal_A = np.diag(self.p_A) - 1
        np.fill_diagonal(A, diagonal_A)
        A[0,0] = 1
        B = np.zeros([len(estados)])
        B[0] = 1
        self.v_A = np.linalg.solve(A,B)[:-1]

        #Calculo frecuencia de operaciones para usuario tipo B
        A = self.p_B.to_numpy().transpose()
        diagonal_A = np.diag(self.p_B) - 1
        np.fill_diagonal(A, diagonal_A)
        A[0,0] = 1
        B = np.zeros([len(estados)])
        B[0] = 1
        self.v_B = np.linalg.solve(A,B)[:-1]
        return

    def calcularCargaOperaciones(self):
        carga_media = self.v_A*self.fA + self.v_B*self.fB
        self.carga_media = pd.DataFrame(data= carga_media, index=estados[:-1], columns=['carga'], dtype=float)
        print(self.carga_media)
        return



sist = sistema(0.25, 0.75)
sist.crearMatricesProbabilidadTransición()
sist.calcularFrecuenciaOperaciones()
sist.calcularCargaOperaciones()
