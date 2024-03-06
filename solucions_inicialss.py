from abia_bicing import furgonetas

def Solucio_greedy2(estaciones, numero_furgos, num_bicis_max):
    excedentes = [(est, est.num_bicicletas_next - est.demanda) for est in estaciones.lista_estaciones]
    excedentes_pos = []
    excedentes_neg = []
    
    for est, exc in excedentes:
        if exc >= 1:
            excedentes_pos.append((est, exc))
        elif exc < 0:
            excedentes_neg.append((est, exc))
            
    excedentes_pos.sort(key=lambda x: x[1], reverse=True)
    excedentes_neg.sort(key=lambda x: x[1])
    
    furgonetas_list = []
    for i in range(min(numero_furgos, len(excedentes_pos), len(excedentes_neg))):
        origen = excedentes_pos[i][0]
        dest1 = excedentes_neg[i][0]
        cant_bicis1 = min(num_bicis_max, excedentes_pos[i][1])
        
        furgoneta = furgonetas(origen, dest1, cant_bicis1)
        furgonetas_list.append(furgoneta)
        
    return furgonetas_list


import math





def distancia(estacion1, estacion2) -> float:
    return math.sqrt((estacion1.coordX - estacion2.coordX)**2 + (estacion1.coordY - estacion2.coordY)**2)


def Solucio_greedy3(estaciones, numero_furgos: int, num_bicis_max: int):
    excedentes = [(est, est.num_bicicletas_next - est.demanda) for est in estaciones.lista_estaciones]

    furgonetas_list = []
    used_origins = set()  # Keep track of stations already used as origins
    
    for _ in range(numero_furgos):
        excedentes_pos = [x for x in excedentes if x[1] > 0 and x[0] not in used_origins]  # Exclude used origins
        excedentes_neg = [x for x in excedentes if x[1] < 0]

        # Si no hay excedentes positivos o negativos, no podemos hacer mÃ¡s asignaciones.
        if not excedentes_pos or not excedentes_neg:
            break

        # Calculamos las parejas posibles ordenadas por distancia.
        parejas = [(pos, neg, distancia(pos[0], neg[0]))
                   for pos in excedentes_pos for neg in excedentes_neg if pos[0] != neg[0]]
        parejas.sort(key=lambda x: x[2])

        pos, neg, _ = parejas[0]
        cant_bicis = min(num_bicis_max, pos[1], abs(neg[1]))

        furgoneta = furgonetas(pos[0], neg[0], cant_bicis)
        furgonetas_list.append(furgoneta)

        # Add the used origin to the set
        used_origins.add(pos[0])

        # Actualizamos los excedentes y eliminamos el origen utilizado de excedentes_pos.
        excedentes = [(excedente[0], excedente[1] - cant_bicis) if excedente[0] == pos[0] 
                      else (excedente[0], excedente[1] + cant_bicis) if excedente[0] == neg[0] 
                      else excedente for excedente in excedentes]

    return furgonetas_list

