# 142, Toma Alexandra, alexandra.toma1@s.unibuc.ro
# 142, Macovei Catalina, catalina.macovei@s.unibuc.ro

# sigma contine toate caracterele limbii eng, asta inseamna ca si alte mii de cuvinte sunt incluse aici dar invalide pentru joc


# cititi de la stdin/fisier linie cu linie si de afisat
# Note that each section (Sigma, States, Transition) should have written at the end the word: "End"
# For example:
# States
# q0,S
# q1
# q2
# q3,F





def reading_data_set(f):
    d = {'Sigma': [], 'Theta': [], 'States': [[], [], []], 'Transitions': []}  # data will be stored in a dictionary with this sections
    try:
        f = open(f)
        section = ''

        for l in f:
            linie = l.strip("\n")
            linie = linie.strip(" ")

            if linie == '':  # ignoring empty lines
                continue
            if linie.startswith('#'):  # just ignoring the comment lines from the file
                continue
            if linie.lower().startswith('theta'):  # if I found theta section -> the list attached to my DFA
                section = 'theta'
                continue
            if linie.lower().startswith('sigma'):  # if I found sigma section
                section = 'sigma'
                continue
            elif linie.lower().startswith('states'):  # if I found states section
                section = 'states'
                continue
            elif linie.lower().startswith('transitions'):  # if I found transitions section
                section = 'transitions'
                continue

            if section == 'sigma':
                if ',' in linie:
                    print(
                        "Please write each symbol on a new line, whithout ','! ")  # make sure each simbol is ona new line
                    return 0
                var = linie.split()
                d['Sigma'].extend(var)

            elif section == 'theta':
                if ',' in linie:
                    print(
                        "Please write each symbol on a new line, whithout ','! ")  # make sure each simbol is ona new line
                    return 0
                var = linie.split()
                d['Theta'].extend(var)

            elif section == 'states':
                state = []
                if ', ' in linie:
                    state = linie.split(', ')
                elif ',' in linie:
                    state = linie.split(',')
                else:
                    state = linie.split()

                if state != []:
                    if 'F' in state:  # adaug final states in lista de stari finale si cea cu toate starile
                        state.remove('F')
                        d['States'][2].extend(state)
                        d['States'][0].extend(state)
                    elif 'S' in state:  # adaug start state in lista de stari initiale si cea cu toate starile
                        state.remove('S')
                        d['States'][1].extend(state)
                        d['States'][0].extend(state)
                    else:
                        d['States'][0].extend(state)


            elif section == 'transitions':  # citesc tranzitiile
                transitions = []
                if ', ' in linie:
                    transitions = linie.split(', ')
                elif ',' in linie:
                    transitions = linie.split(',')
                else:
                    transitions = linie.split()

                d['Transitions'].append(tuple(transitions))  # each transition is a tuple, like ('q1', '0', 'q1')

    except:
        print("Could not load the file!")

    print(d)   # show dictionary with data for testing
    return d


# validation sigma, are the simbols/alphabet for dfa, checks if it's empty
def validation_Sigma(d):
    if d['Sigma'] != []:
        s1 = ','
        s2 = 'q'
        for simbol in d['Sigma']:
            if s1 in simbol and s2 in simbol:
                print(f'Please check the Sigma section, you are not allowed to have -> {s1 if s1 else s2} in simbols list')
        return 1
    else:
        print('You can\'t have an empty alphabet. Introduce the symbols!')
        return 0


def validation_Theta(d):        # verifica daca lista e goala
    if d['Theta'] == []:
        print('Error:Your LA list is empty, sorry!')
        return 0
    else:
        return 1


# validation states:
# states  can  be  succeeded  by  ”F”,  ”S”,  both  or  nothing
#  ”S”  symbol  can succeed only one state.  FOR EXAMPLE:
# States
# q0,S
# q1
# q2
# q3,F

def validation_states(d):
    start_state = d['States'][1]
    final_states = d['States'][2]
    len_start_state = len(start_state)

    if len_start_state > 1:
        print(f"You must have only 1 state! Found  {len_start_state} states")
        return 0
    if len_start_state == 1 and len(final_states) < 1:
        print(f"You can't have an empty list of final states while having a start state!")
        return 0
    if len_start_state < 1:
        print("It makes no sense to have no start state!")
        return 0

    return 1


# validation transitions:
def validation_transitions(d):
    transitions = d['Transitions']

    for transition in transitions:      # for each transition check if it has the necessary length, valid states and sigma
        if len(transition) > 6:
            print("Too many items in transition tuple, there can be only 6!")
            return 0

        if len(transition) < 6:
            print("Don't have enough transitions! Should have 6")
            return 0

        if transition[0] not in d['States'][0] or transition[5] not in d['States'][0]:
            print('Transitions NULL: can\'t find the transition in States')
            return 0

        if transition[1] not in d['Sigma']:
            print(f'Transitions NULL: invalid transition {transition[1]}')
            return 0

        if transition[2] not in d['Theta'] or transition[3] not in d['Theta'] and transition[4] not in d['Theta']:
            print(f'Transitions NULL: invalid transition, components not in gama')
            return 0

    return 1


# validation input function: returns a bool True - passed validation or False - didn't pass it
def validation_input(input_string, d):
    for x in input_string.split(' '):
        if x not in d['Sigma']:
            print("You have unknown simbols in input string!")
            return False
    return True


"""
1.citesc comanda a1
2.pentru s1 (item care trebuie sa il am ca sa fac tranzitia) din comanda a1 (ex: comanda -> go armory,ca sa intru in aromory imi trebuie o cheie, iar cheia e in lista)
3.daca s1 este in lista
4.sterg a2 (ex: locatia curenta: ENTRANCE HALL)
5.Adaug armory a3 in lista (pentru ca ma aflu acolo daca am intrat)
"""

def run_LA(d, plan):
    start_state = d['Transitions'][0]
    current = start_state

    level_list = d['Theta']     # lista curenta pentru regula

    # most frequent errors may occur here, that's why I use a try block
    try:
        if validation_Sigma(d) and validation_states(d) and validation_transitions(d) and validation_input(plan,d):  # if everything is valid
            for tr in d['Transitions']:
                if tr[1] == plan:
                    if tr[2] in level_list:     # daca imi trebuie un item sa intru in room
                        level_list.remove(tr[3])
                        level_list.append(tr[4])

                        current = tr
                        break
                    elif tr[2] not in level_list:   # daca nu imi trebuie nimic sa intru in room
                        level_list.remove(tr[3])  # conditie daca exista
                        level_list.append(tr[4])

                        current = tr
                        break
                    else:                           # pur si simplu trec la urmatoarea etapa
                        current = tr
                        break

            check = False

            if current[5] in d['States'][2]:  # check if final state
                check = True
            else:
                print("Automata didn't stop in final state!")

            if check:
                print('accept')
                return 1     # return 1 meaning:  accept plan, move forward

            else:
                print('reject')
                return 0    # return 0 meaning:  reject plan
        else:
            print("Automata didn't pass the validation!")
            return 0        # return 0 meaning:  reject plan

    except:
        print("Automata failed running process!")
        return 0
    return 0


# ----- Testare -----

d = reading_data_set("LA.in.txt")    # name of file goes here       !!!!!!!
plan = 'citesc_regula' # de verificat
print(run_LA(d, plan))