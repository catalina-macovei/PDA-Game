# 142, Toma Alexandra, alexandra.toma1@s.unibuc.ro
# 142, Macovei Catalina, catalina.macovei@s.unibuc.ro

def emulate_pda(pda, input_str):
    # extragem alfabetul, multimea starilor, starea initiala, multimea starilor finale ale nfa ului, si functia de tranzitie
    sigma = pda[0]
    lista_stari = pda[1]
    stare_init = pda[2]
    lista_stari_finale = pda[3]
    gama = pda[4]
    lista_actiuni = pda[5]

    # stari_crt este lista care retine starile in care se afla simultan automatul la un anumit moment dat si stiva
    # parcurgem prima data lista de actiuni pentru a aplica toate tranzitiile cu * ( care nu necesita input)
    stari_crt = []
    for t in lista_actiuni:
        parsed = t.split(',')
        # se aplica tranzitia daca starea coincide, se citeste * si dam pop la *
        if stare_init == parsed[0] and parsed[1] == '*' and parsed[2] == '*':
            stari_crt.append((parsed[4],[parsed[3]]))
    # daca nu se aplica tranzitii, in lista de stari curente se afla doar tuplul (stare_initiala, stiva_vida)
    if not stari_crt:
        stari_crt = [(stare_init, [])]

    #
    # print('stari curente',stari_crt)

    # pentru fiecare litera citita
    for s in input_str.split(' '):


        # verificam daca inputul este valid
        if s not in sigma:
            raise RuntimeError("Inputul contine simboluri necunoscute.")

        # prin tranzitii se trece la o lista de stari
        next_states = []
        # pentru fiecare stare din lista curenta de stari in care se afla automatul
        for q in stari_crt:

            # incercam sa facem match cu o tranzitie
            for act in lista_actiuni:
                t = act.split(',')
                # preluam stiva din tuplul cu starea curenta
                stack = []
                stack.append(q[1])
                if t[0] == q[0]: # daca starile coincid
                    if t[1] == '*': # daca se citeste *
                        if t[2] == '*': # daca se da pop la *
                            # se aplica tranzitia
                            if t[3] != '*': # daca avem la ce sa dam push
                                stack.append(t[3])
                            # pentru ca nu s-a consumat nicio litera din input string starea in care s-a ajuns va fi evaluata tot in aceasta runda
                            stari_crt.append((t[4], stack))
                        elif stack != [] and t[2] == stack[-1]: # daca litera careia trebuie sa-i dam pop se afla in varful stivei
                            # se aplica tranzitia
                            stack.pop()
                            if t[3] != '*':  # daca avem la ce sa dam push
                                stack.append(t[3])
                            # pentru ca nu s-a consumat nicio litera din input string starea in care s-a ajuns va fi evaluata tot in aceasta runda
                            stari_crt.append((t[4], stack))
                    elif t[1] == s:  # daca ce trebuie sa se citeasca pt aplicare tranzitiei si ceea ce s-a citit coincid
                        if t[2] == '*':  # daca nu trebuie sa dam pop la nimic
                            # se aplica tranzitia
                            if t[3] != '*':  # daca avem la ce sa dam push
                                stack.append(t[3])
                            # pentru ca s-a consumat litera de la input string, efectul tranzitiei va fi evaluat in runda urmatoare
                            next_states.append((t[4], stack))
                        elif stack != [] and t[2] == stack[-1]:  # daca ceea ce cautam pentru a da pop se afla in varful stivei
                            # se aplica regula
                            stack.pop()
                            if t[3] != '*':  # daca avem la ce sa dam push
                                stack.append(t[3])
                            # pentru ca s-a consumat litera de la input string, efectul tranzitiei va fi evaluat in runda urmatoare
                            next_states.append((t[4], stack))

        # trecem la runda urmatoare
        stari_crt = next_states

    # daca au mai ramas de executat actiuni care nu necesita input
    # pentru fiecare din starile curente, verificam ca mai sus match-urile cu tranzitiile, dar efectuam doar tranzitiile pt care nu e necesar sa citim nimic, iar rezultatul va fi evaluat inaceeasi runda
    for q in stari_crt:
        for t in lista_actiuni:
            stack = []
            stack.extend(q[1])
            if q[0] == t[0] and t[1] == '*':
                if t[2] == '*':
                    if t[3] != '*':
                        stack.append(t[3])
                elif stack != [] and t[2] == stack[-1]:
                    stack.pop()
                    if t[3] != '*':
                        stack.append(t[3])
                stari_crt.append((t[4], stack))


    # verificam daca s-a ajuns in starea finala pentru macar un branch, daca da accepted, altfel rejected
    for q in stari_crt:
        if q[0] in lista_stari_finale and q[1] == []:
            return True
    return False
