import pandas as pd
import numpy as np

# Nota: para crear celdas utilziar "#%%"
estados = ['e', 'h', 's', 'v', 'g', 'c', 'b', 'x']
operaciones = ['h', 's', 'v', 'g', 'c', 'b']
K = ['WS-cpu', 'WS-disk', 'AS-cpu', 'AS-disk', 'DS-cpu', 'DS-disk']

class sistema():

    def __init__(self, fA, fB, N=[1,1,1]):
        self.fA = fA
        self.fB = fB
        self.N = pd.Series(index=['WS', 'AS', 'DS'], data=N)

        self.crearMatricesProbabilidadTransición()
        self.crearMatrizDemandas()

        self.calcularFrecuenciaOperaciones()
        self.calcularFactoresCargaOperaciones()

    def configurarNServidores(self, N):
        self.N = pd.Series(index=['WS', 'AS', 'DS'], data=N)
        return

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
        # Calculo frecuencia de operaciones para usuario tipo A
        A = self.p_A.to_numpy().transpose()
        diagonal_A = np.diag(self.p_A) - 1
        np.fill_diagonal(A, diagonal_A)
        A[0, 0] = 1
        B = np.zeros([len(estados)])
        B[0] = 1
        self.v_A = np.linalg.solve(A, B)[1:-1]

        # Calculo frecuencia de operaciones para usuario tipo B
        A = self.p_B.to_numpy().transpose()
        diagonal_A = np.diag(self.p_B) - 1
        np.fill_diagonal(A, diagonal_A)
        A[0, 0] = 1
        B = np.zeros([len(estados)])
        B[0] = 1
        self.v_B = np.linalg.solve(A, B)[1:-1]
        return


    def calcularFactoresCargaOperaciones(self):
        fact_distr_carga = self.v_A*self.fA + self.v_B*self.fB
        self.fact_distr_carga = pd.Series(
            data=fact_distr_carga, index=operaciones, dtype=float)
        return

    def calculaCargaOperaciones(self):
        self.distr_carga = self.carga_global * self.fact_distr_carga
        return

    def crearMatrizDemandas(self):
        
        R = ['h', 's', 'g', 'v', 'c', 'b']
        self.D = pd.DataFrame(index=K, columns=R, dtype=float)
        self.D.loc['WS-cpu'] = [0.008, 0.009, 0.011, 0.060, 0.012, 0.015]
        self.D.loc['WS-disk'] = [0.03, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.D.loc['AS-cpu'] = [0.0, 0.03, 0.035, 0.025, 0.045, 0.04]
        self.D.loc['AS-disk'] = [0.0, 0.008, 0.08, 0.009, 0.011, 0.012]
        self.D.loc['DS-cpu'] = [0.0, 0.01, 0.009, 0.015, 0.07, 0.045]
        self.D.loc['DS-disk'] = [0.0, 0.035, 0.018, 0.05, 0.08, 0.09]
        return

    def calcularUtilizaciónRecursos(self):
        #Utilización de los recurso para todas las clases de operaciones
        self.utilizacionRec = pd.Series(index=K, dtype=float)
        self.utilizacionRec['WS-cpu'] = np.sum((self.distr_carga/self.N['WS']) * self.D.loc['WS-cpu'])
        self.utilizacionRec['WS-disk'] = np.sum((self.distr_carga/self.N['WS']) * self.D.loc['WS-disk'])
        self.utilizacionRec['AS-cpu'] = np.sum((self.distr_carga/self.N['AS']) * self.D.loc['AS-cpu'])
        self.utilizacionRec['AS-disk'] = np.sum((self.distr_carga/self.N['AS']) * self.D.loc['AS-disk'])
        self.utilizacionRec['DS-cpu'] = np.sum((self.distr_carga/self.N['DS']) * self.D.loc['DS-cpu'])
        self.utilizacionRec['DS-disk'] = np.sum((self.distr_carga/self.N['DS']) * self.D.loc['DS-disk'])
        return

    def calcularResidenciaOpxRecurso(self):
        print(self.D)
        T_ir = self.D.to_numpy() / (1 - self.utilizacionRec.to_numpy().reshape([-1,1]))
        self.T_ir = pd.DataFrame(index=K, columns=operaciones, data= T_ir, dtype=float)
        return

    def calcularTRespuestaXOperacion(self):
        self.Tres_operacion = self.T_ir.sum(axis=0)
        return

    def calcularTMedioRespuesta(self):
        self.Tres_medio = np.sum(self.Tres_operacion * (self.distr_carga / self.carga_global))
        return

    #LOS TIEMPOS DE RESPUESTA NO SALEN IGUAL QUE EN EL LIBRO
    def introducirCarga(self, carga):
        '''
        Entrada: carga global del sistema
        Salida: Tiempo medio de respuesta de operaciones, tiempo de respuesta para cada clase de operación 
        y booleano indicando si algun recurso tiene utilización > 0.9
        '''
        self.carga_global = carga

        self.calculaCargaOperaciones()
        self.calcularUtilizaciónRecursos()
        self.calcularResidenciaOpxRecurso()
        self.calcularTRespuestaXOperacion()
        self.calcularTMedioRespuesta()
        if any(self.utilizacionRec > 0.9):
            saturado = True
        else:
            saturado = False
        return self.Tres_medio, self.Tres_operacion, saturado

N = [1,1,2]
sist = sistema(0.25, 0.75, N)

carga = 11
tMedio, tOperaciones, saturado = sist.introducirCarga(carga)
print(tMedio)
print(tOperaciones)
print(saturado)
