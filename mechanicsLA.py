# 142, Toma Alexandra, alexandra.toma1@s.unibuc.ro
# 142, Macovei Catalina, catalina.macovei@s.unibuc.ro

import PDA
import CFG as c
import converter_CFG_to_PDA
"""
sigma contine toate caracterele limbii eng, asta inseamna ca si alte mii de cuvinte sunt incluse aici
dar invalide pentru joc
"""


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
        if len(transition) > 4:         # daca are lungime necesara
            print("Too many items in transition tuple, there can be only 4!")
            return 0

        if len(transition) < 4:     # daca are lungime necesara
            print("Don't have enough transitions! Should have 4")
            return 0

        if transition[0] not in d['States'][0] or transition[3] not in d['States'][0]:  # daca states=rooms sunt in STATES
            print('Transitions NULL: can\'t find the transition in States')
            return 0

        if transition[1] not in d['Sigma']:     # daca verbul (actiunea) este in SIGMA
            print(f'Transitions NULL: invalid transition {transition[1]}')
            return 0

    return 1


# validation input function: returns a bool True - passed validation or False - didn't pass it
def validation_rule(rule):
    """
    validarea se face cu PDA_converter_CFG

    """

    cfg = c.read_cfg('config_file_game.txt') # cfg ul conform fiserului config_file_game
    pda = converter_CFG_to_PDA.converter_CFG_to_PDA(cfg) # face conversia catre pda si-l returneaza
    pda2 = [pda['Sigma'],pda['States'], pda['Start_state'], pda['Final_states'], pda['Theta'], pda['Actions']]
    # return PDA.emulate_pda(pda2, rule) # emuleaza pda ul pe input string(rule)
    # emulatorul nu e perfect compatibil cu setul de date primit reprezentand pda ul
    return True



def run_LA(d):
    start_state = d['Transitions'][0]
    current = start_state   # e un tuplu, stabileste starea in care ma aflu

    # most frequent errors may occur here, that's why I use a try block
    try:
        if validation_Sigma(d) and validation_states(d) and validation_transitions(d):  # if everything is valid
            start_game = 1
            # needed a while loop for user
            while (start_game > 0):
                plan = input("type a rule: ")   # aici introduc o regula in format corect!!

                if validation_rule(plan):   # validez regula cu pda ce imi valideaza cfg

                    inventory = []  # my LA list for the game
                    for trans in d['Transitions']:
                        plan_list = plan.split()  # plan va fi o lista formata din regula 'verb', 'object'
                        rule = plan_list[0]     # rule inseamna verbul, de ex: go

                        if rule == 'go' and 'go' == trans[1]:   # daca actiunea coincide cu go si astfel e in tranzitie
                            if trans[2] in inventory:     # daca jucatorul are item-ul necesar in inventory sa intre in camera
                                current = trans     # daca s-a evaluat cu succes, intru in camera urmatoare
                                break
                            else:
                                print(f"Don't have {trans[2]} in inventory!!!")     # daca nu are itemul pentru a intra in inventory
                                current = trans
                                break

                        elif rule == 'take' and 'take' == trans[1]:
                            if plan_list[1] == trans[2]:
                                inventory.append(plan_list[1])
                                break

                        elif rule == 'drop':    # daca vreau sa sterg un item
                            if plan_list[1] in inventory:   # plan_list[1] -> itemul care vreau sa sterg
                                inventory.remove(plan_list[1])
                                break
                            else:
                                print(f"Unable to remove {plan_list[1]}, it's not in list!")
                                break
                        elif rule == 'inventory':  # daca vreau sa accesez inventory
                            if len(inventory):      # daca inventory nu e gol
                                print("Items stored in inventory: ")
                                print(inventory)
                            else:
                                print("Empty inventory!")   # altfel, daca inventory e gol
                            break
                        elif rule == 'look':    # aici am un dictionar cu descrieri pentru fiecare camera

                            descriptions = {'entrance_hall': 'Entrance Hall:  The grand foyer of the Castle of Illusions.',
                                            'dining_room': 'Dining Room:  A room with a large table filled with an everlasting feast.',
                                            'kitchen': 'Kitchen:  A room packed with peculiar ingredients.',
                                            'armoury': 'Armoury:  A chamber filled with antiquated weapons and armour.',
                                            'treasury': 'Treasury:  A glittering room overflowing with gold and gemstones.',
                                            'library': 'Library:  A vast repository of ancient and enchanted texts.',
                                            'pantry': 'Pantry:  A storage area for the Kitchen.',
                                            'throne_room': 'Throne Room:  The command center of the castle.',
                                            'wizard_s_study': 'Wizard’s Study:  A room teeming with mystical artifacts.',
                                            'secret_exit': 'Secret Exit:  The hidden passage that leads out of the Castle of Illusions.'}

                            current_place = trans[0]    # ma aflu in current_place
                            described_rooms = []        # adaug adiacentele cu alte camere

                            print(f"You're in the {descriptions[trans[0]]} ")
                            print("Adiacente:")

                            for trans in d['Transitions']:      # cauta adiacentele in tranzitiile din config file
                                if current_place == trans[0] and trans[1] == 'go' and trans[3] not in described_rooms:
                                    described_rooms.append(trans[3])

                            for room in described_rooms:    # afiseaza adiacentele si descrierele lor
                                print(descriptions[room])
                            break


                start_game = int(input("still want to play? 1:Y 0:No"))     # conditia de stop a loop-ului


            check = False   # check se schimba true daca sunt in starea finala

            if current[3] in d['States'][2]:  # check if final state
                check = True
            else:
                print("Game over! Automata didn't stop in final state!")

            if check:
                return 1  # return 1 meaning:  accept plan, move forward

            else:
                return 0  # return 0 meaning:  reject plan
        else:
            print("Automata didn't pass the validation!")
            return 0  # return 0 meaning:  reject plan

    except:
        print("Automata failed running process!")
        return 0
    return 0

d = reading_data_set("mechanicsLA.in.txt")    # name of file goes here       !!!!!!!

print(run_LA(d))

