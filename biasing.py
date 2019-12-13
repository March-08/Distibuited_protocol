from random import randint
'''
assumendo che randint generi u.a.r un bit
'''

'''
Algoritmo che dato un numero p in (0,1) restituisce 1 con probabilità p e 0 con
probabilità 1-p
'''

'''
IDEA: preso p in (0,1) possiamo considerarlo come p = X0.X1 X2 X3 X4.....Xinf..
      quindi generiamo continuamente un nuovo bit di p e lo restituiamo con probabilità 1/2
'''

'''
IMPLEMENTAZIONE: biasing(p):
                 funzione principale che cicla sulla chiamata di compute_next_bit
                 e restituisce il bit calcolato con probabilità 1/2

                 compute_next_bit(a,b,p):
                 sfruttiamo la funzione compute_next_bit per calcolare il bit successivo di p
                 tale funzione sfrutta l'idea che partendo con a=0 e b = 1 per capire
                 se il bit successivo è 1 ci basta verificare se p è >= di a+b/2 e aggiornare a e b

'''

def biasing1(p):
    a = 0
    b = 1
    r = x = 0
    while x == r:
        a,b,x = compute_next_bit(a,b,p)
        r = randint(0,1)
    return x

def compute_next_bit(a,b,p):
    m = (a+b)/2
    if p >= m:
        return m,b,1
    return a,m,0


#p = probabilita' di vincita' al lotto
#i = 0
#for _ in range(1,10000):
#    i = i+biasing1(1/10000000)
#print(i)
