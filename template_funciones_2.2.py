import numpy as np
import scipy
import template_funciones as tp1
import numpy.linalg
# Matriz A de ejemplo
A_ejemplo = np.array([
    [0, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 1, 1, 0]
])


def calcula_L(A):
    K = calcular_K(A)
    L = K - A
    return L

def calcula_R(A):
    K = calcular_K(A)
    n = A.shape[0]
    m = A.shape[1]
    Doble_De_Conexiones = 0
    for i in range(0,n):
        for j in range(0,m):
            Doble_De_Conexiones += A[i][j]
    

    P = np.zeros((n,m))

    for i in range(0,n):
        for j in range(0,m):
            P[i][j] = (K[i][i]*K[j][j])/Doble_De_Conexiones
    
    R = A-P


    return R

def calcula_lambda(L,v): 
    s = v.copy()
    for i in range(len(s)):
        if s[i] >= 0:
            s[i] = 1
        else:
            s[i] = -1

    lambdon = (1/4 * (s.T @ L @ s))                            
    return lambdon

def calcula_Q(R,v):
    # La funcion recibe R y s y retorna la modularidad (a menos de un factor 2E)
    s = v.copy()
    for i in range(len(s)):
        if s[i] >= 0:
            s[i] = 1
        else:
            s[i] = -1
    
    Q = s.T@ R @ s
    return Q

def metpot1(A,tol=1e-8,maxrep=np.inf):
   # Recibe una matriz A y calcula su autovalor de mayor módulo, con un error relativo menor a tol y-o haciendo como mucho maxrep repeticiones
   v = np.random.uniform(-1,1,size=A.shape[0]) # Generamos un vector de partida aleatorio, entre -1 y 1
   v = v / np.linalg.norm(v,2) # Lo normalizamos
   v1 = A @ v # Aplicamos la matriz una vez
   print(f'Norma vector v1 antes de normalizar (inicio): {np.linalg.norm(v,2):.4e}')
   v1 = v1 / np.linalg.norm(v1,2)  # normalizamos
   l = (v.T @ A @ v)/(v.T @ v) # Calculamos el autovector estimado
   l1 = (v1.T @ A @ v1)/(v1.T @ v1) # Y el estimado en el siguiente paso
   nrep = 0 # Contador
   while np.abs(l1-l)/np.abs(l) > tol and nrep < maxrep: # Si estamos por debajo de la tolerancia buscada 
      v = v1 # actualizamos v y repetimos
      l = l1
      v1 = A @ v # Calculo nuevo v1
      print(f'Norma vector v1 antes de normalizar (iter {nrep}): {np.linalg.norm(v1,2):.4e}')
      v1 = v1/np.linalg.norm(v1,2) # Normalizo
      l1 = (v1.T @ A @ v1)/(v1.T @ v1) # Calculo autovector
      nrep += 1 # Un pasito mas
   if not nrep < maxrep:
      print('MaxRep alcanzado')
   l = (v1.T @ A @ v1)/(v1.T @ v1) # Calculamos el autovalor
   return v1,l,nrep<maxrep

def deflaciona(A,tol=1e-8,maxrep=np.inf):
    # Recibe la matriz A, una tolerancia para el método de la potencia, y un número máximo de repeticiones
    v1,l1,_ = metpot1(A,tol,maxrep) # Buscamos primer autovector con método de la potencia
    deflA = A - l1 * np.outer(v1,v1) # Sugerencia, usar la funcion outer de numpy
    return deflA

def metpot2(A,v1,l1,tol=1e-8,maxrep=np.inf):
   # La funcion aplica el metodo de la potencia para buscar el segundo autovalor de A, suponiendo que sus autovectores son ortogonales
   # v1 y l1 son los primeors autovectores y autovalores de A}
   # Have fun!
   deflA = A - l1 * np.outer(v1,v1)
   return metpot1(deflA,tol,maxrep)


def metpotI(A,mu,tol=1e-8,maxrep=np.inf):
    # Retorna el primer autovalor de la inversa de A + mu * I, junto a su autovector y si el método convergió.
    I = np.eye(len(A))
    Amu = A + mu * I
    L,U = tp1.calculaLU(Amu)
    Linv = scipy.linalg.solve_triangular(L,I, lower= True)
    Uinv = scipy.linalg.solve_triangular(U,I, lower= False)

    AmuINV = Uinv @ Linv
    return metpot1(AmuINV,tol=tol,maxrep=maxrep)

def metpotI2(A,mu,tol=1e-8,maxrep=np.inf):
   # Recibe la matriz A, y un valor mu y retorna el segundo autovalor y autovector de la matriz A, 
   # suponiendo que sus autovalores son positivos excepto por el menor que es igual a 0
   # Retorna el segundo autovector, su autovalor, y si el metodo llegó a converger.
   I = np.eye(len(A))
   X = A + mu * I # Calculamos la matriz A shifteada en mu
   L, U = tp1.calculaLU(X)
   Linv = scipy.linalg.solve_triangular(L,I, lower= True)
   Uinv = scipy.linalg.solve_triangular(U,I, lower= False) 
   iX = Uinv @ Linv # La invertimos
   defliX = deflaciona(iX) # La deflacionamos
   v,l,_ =  metpot1(defliX,tol=tol,maxrep=maxrep)# Buscamos su segundo autovector
   l = 1/l # Reobtenemos el autovalor correcto
   l -= mu
   return v,l,_


def laplaciano_iterativo(A,niveles,nombres_s=None):
    # Recibe una matriz A, una cantidad de niveles sobre los que hacer cortes, y los nombres de los nodos
    # Retorna una lista con conjuntos de nodos representando las comunidades.
    # La función debe, recursivamente, ir realizando cortes y reduciendo en 1 el número de niveles hasta llegar a 0 y retornar.
    if nombres_s is None: # Si no se proveyeron nombres, los asignamos poniendo del 0 al N-1
        nombres_s = range(A.shape[0])
    if A.shape[0] == 1 or niveles == 0: # Si llegamos al último paso, retornamos los nombres en una lista
        return([nombres_s])
    else: # Sino:
        L = calcula_L(A) # Recalculamos el L
        v,l,_ = metpotI2(L, 1) # Encontramos el segundo autovector de L
        # Recortamos A en dos partes, la que está asociada a el signo positivo de v y la que está asociada al negativo
        Ap = np.zeros(A.shape) # Asociado al signo positivo
        Am = np.zeros(A.shape) # Asociado al signo negativo
        #(g) Separamos A en Ap y Am:
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if A[i][j] == 1:
                    if (v[i] > 0) and (v[j] > 0):
                        Ap[i][j] = A[i][j]
                        Ap[j][i] = A[j][i]
                        
                    elif (v[i] < 0) and (v[j] < 0):
                        Am[i][j] = A[i][j]
                        Am[j][i] = A[j][i]
                        
        
        return(
                laplaciano_iterativo(Ap,niveles-1,
                                     nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi>0]) +
                laplaciano_iterativo(Am,niveles-1,
                                     nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi<0])
                )        


def modularidad_iterativo(A=None,R=None,nombres_s=None):
    # Recibe una matriz A, una matriz R de modularidad, y los nombres de los nodos
    # Retorna una lista con conjuntos de nodos representando las comunidades.

    if A is None and R is None:
        print('Dame una matriz')
        return(np.nan)
    if R is None:
        R = calcula_R(A)
    if nombres_s is None:
        nombres_s = range(R.shape[0])
    print(f'Norma matriz R: {np.linalg.norm(R,2):.4e}')
    # Acá empieza lo bueno
    if R.shape[0] == 1: # Si llegamos al último nivel
        return [nombres_s]
    else:
        v,l,_ = metpot1(R) # Primer autovector y autovalor de R
        print(f'metpot1 con R, autovalor: {l:.4e}')
        # Modularidad Actual:
        Q0 = np.sum(R[v>0,:][:,v>0]) + np.sum(R[v<0,:][:,v<0])
        if Q0<=0 or all(v>0) or all(v<0): # Si la modularidad actual es menor a cero, o no se propone una partición, terminamos
            return [nombres_s]
        else:
            ## Hacemos como con L, pero usando directamente R para poder mantener siempre la misma matriz de modularidad
            Rp = np.zeros(R.shape) # Asociado al signo positivo
            Rm = np.zeros(R.shape)
            idx_pos = [i for i, val in enumerate(v) if val > 0]
            idx_neg = [i for i, val in enumerate(v) if val < 0]
            Rp = R[np.ix_(idx_pos, idx_pos)]
            Rm = R[np.ix_(idx_neg, idx_neg)]
            # Asociado al signo negativo
            #for i in range(R.shape[0]):
                #for j in range(R.shape[1]):
                    #if (v[i] > 0) and (v[j] > 0):
                        #Rp[i][j] = 1
                        #Rp[j][i] = 1
                    #elif (v[i] < 0) and (v[j] < 0):
                        #Rm[i][j] = 1
                        #Rm[j][i] = 1
        
            #Rp = calcula_R(Ap) # Parte de R asociada a los valores positivos de v                 
            #Rm = calcula_R(Am) # Parte asociada a los valores negativos de v
            print(f'Norma matriz Rp: {np.linalg.norm(Rp, 2):.4e}')
            print(f'Norma matriz Rm: {np.linalg.norm(Rm, 2):.4e}')                      
            vp,lp,_ = metpot1(Rp)  # autovector principal de Rp                     
            vm,lm,_ = metpot1(Rm) # autovector principal de Rm                      
        
            # Calculamos el cambio en Q que se produciría al hacer esta partición
            Q1 = 0
            if not all(vp>0) or all(vp<0):
               Q1 = np.sum(Rp[vp>0,:][:,vp>0]) + np.sum(Rp[vp<0,:][:,vp<0])
            if not all(vm>0) or all(vm<0):
                Q1 += np.sum(Rm[vm>0,:][:,vm>0]) + np.sum(Rm[vm<0,:][:,vm<0])
            if Q0 >= Q1: # Si al partir obtuvimos un Q menor, devolvemos la última partición que hicimos
                return([[ni for ni,vi in zip(nombres_s,v) if vi>0],[ni for ni,vi in zip(nombres_s,v) if vi<0]])
            else:
                # Sino, repetimos para los subniveles
                return(
                        modularidad_iterativo(A, Rp, nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi>0]) +
                        modularidad_iterativo(A, Rm, nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi<0])
                        )




def calcular_K(A):
    m = A.shape[0]
    K = np.zeros((m, m))
    n = A.shape[1]
    for i in range(0, n):
        grado = 0
        for elem in A[i]:
            if elem != 0:
                grado += 1
        K[i,i] = grado
    return K


print(modularidad_iterativo(A_ejemplo))