# 142, Toma Alexandra, alexandra.toma1@s.unibuc.ro
# 142, Macovei Catalina, catalina.macovei@s.unibuc.ro

import CFG as c
import PDA

def converter_CFG_to_PDA(cfg):
    # cfg = {'Vars': [], 'Sigma': [], 'Rules': {}}

    # stabilim componentele pda ului
    # starea initiala este qs
    pda = {'States': [], 'Sigma': [], 'Theta': [], 'Actions': [], 'Start_state': 'qs', 'Final_states': []}


    # sigma este identic cu alfabetul cfg ului
    pda['Sigma'].extend(cfg['Sigma'])

    # theta contine alfabetul cfg ului si simbolul '$'
    pda['Theta'].extend(cfg['Sigma'])
    pda['Theta'].append('$')

    # adaugam starile si tranzitiile automatului

    contor = 1  # pentru denumirea starilor

    # cream scheletul pda ului
    # qs -> (*,*->$) qi -> (*,*,Vars_start) qloop -> (*,$ -> *) -> qf
    pda['States'].append('qs')
    pda['States'].append('qi')
    pda['States'].append('qloop')
    pda['States'].append('qf')

    pda['Final_states'].append('qf')

    pda['Actions'].append('qs,*,*,$,qi')
    pda['Actions'].append('qi,*,*,' + cfg['Vars'][0] + ',qloop')
    pda['Actions'].append('qloop,*,$,*,qf')

    # ne ocupam de qloop

    # intai, tranzitiile pentru intalnirea unui terminal in varful stivei
    # (q,a,a,*,q)
    for terminal in cfg['Sigma']:
        pda['Actions'].append('qloop,' + terminal + ',' + terminal + ',*,qloop')

    # apoi, adaugam starile si tranzitiile pentru intalnirea unei variabile in varful stivei
    # pentru fiecare variabila V din care pornesc reguli, adaugam o noua stare si tranzitia (qloop,*,V,*,varstate) (ii dam pop variabilei din stiva)
    for v in cfg['Rules'].keys():
        varstate = 'q' + v
        pda['States'].append(varstate)
        pda['Actions'].append('qloop,*,' + v + ',*,' + varstate)

        # pentru fiecare regula care substituie variabila v cream un loop de stari care porneste din varstate si ajunge in qloop si care adauga pe stiva membrul drept al regulii cu care s-a substituit
        for option in cfg['Rules'][v]:
            previous = varstate
            # parcurgem in sens invers regula, pe principiul LIFO
            for i in range(len(option[0]) - 1, 0, -1):
                newstate = 'q' + str(contor)
                contor += 1
                pda['States'].append(newstate)
                pda['Actions'].append(previous + ',*,*,' + option[0][i] + ',' + newstate)

                previous = newstate
            # facem legatura cu qloop
            pda['Actions'].append(previous + ',*,*,' + option[0][0] + ',qloop')

    return pda
