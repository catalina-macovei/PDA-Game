# 142, Toma Alexandra, alexandra.toma1@s.unibuc.ro
# 142, Macovei Catalina, catalina.macovei@s.unibuc.ro


import random
### DATASET FOR CFG:
# Function read_cfg(filename) reads the data from the configuration file,
# stores data into a dictionary, vars, sigma, rules
# each of them has a list, excepting rules
# rules key has a dictionary value, with each var as a key and a list of simbols/words it accepts

def read_cfg(filename):
    cfg = {'Vars': [], 'Sigma': [], 'Rules': {}}        # dataset

    try:
        with open(filename, 'r') as f:
            current_section = None                          # the key of cfg dictionary
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('#'):  # just ignoring the comment lines from the file
                    continue

                if line == '':  # ignoring empty lines
                    continue

                if line.startswith('Vars'):
                    current_section = 'Vars'
                    continue

                elif line.startswith('Sigma'):
                    current_section = 'Sigma'
                    continue

                elif line.startswith('Rules'):
                    current_section = 'Rules'
                    continue

                if current_section == 'Vars':
                    var = line.split()[0]           # this adds the variable to d['Vars'] list
                    cfg['Vars'].append(var)

                elif current_section == 'Sigma':    # this adds the symbol/word to d['Sigma'] list
                    symbol = line.split()[0]
                    cfg['Sigma'].append(symbol)

                elif current_section == 'Rules':     # this adds the rule to d['Rules'] dictionary
                    lhs, rhs = line.split('->')
                    lhs = lhs.strip()
                    rhs_list = rhs.split(',')
                    rhs_list = [s.strip() for s in rhs_list]

                    if lhs not in cfg['Rules']:
                        cfg['Rules'][lhs] = []

                    cfg['Rules'][lhs].append(rhs_list)
    except:
        print("Error: Can't read the file, make sure its name is correct!")

    return cfg


def validate_vars(vars):
    check = 0  # Variable to track the validation status

    if vars == []:
        # Check if 'vars' list is empty
        print("\nError: Sorry, you have no variables!")
        return 0  # Return 0 to indicate an error

    for i in range(len(vars)):
        # Iterate over the elements of 'vars' list
        if vars[i] == '*':
            # Check if the current element is '*'
            check = 1
            vars[i:] = vars[i + 1:]  # Remove '*' and subsequent elements from 'vars'
            break  # Exit the loop

    if check == 0:
        # Check if 'check' is still 0
        print('\nError: You have no start variable! \nHint: Write \'*\' symbol on the next row after the start variable:')

    for var in vars:
        # Iterate over the remaining elements in 'vars' list
        if var.isupper() and var.isalpha():
            # Check if the variable is uppercase alphabetic
            check = 1  # Set 'check' to 1
        else:
            print(f"\nError: Your variable {var} isn't valid. "
                  f"\nHint: It should be alpha characters written in uppercase.")
            return 0  # Return 0 to indicate an error

    return check  # Return the value of 'check'



# validation sigma:
def validate_sigma(sigma):
    if sigma == []:
        print("\nError: Sorry, you have no symbols in Sigma section!")
        return 0

    for symbol in sigma:
        if symbol.isupper():
            print(f"\nError: The symbol {symbol} doesn't follow the rules. Symbols shouldn't be in uppercase."
                  f"\nHint: Write {symbol} in lowercase\n")
            return 0

    return 1


def validate_rules(rules, cfg):
    if rules == {}:
        # Check if 'rules' dictionary is empty
        print('\nError: You have no rules.'
              '\nHint: Write the rules in Rules section, each on different line.'
              '\nE.g.: [Variable]->[ValueName]\n')
        return 0

    for var, rule in rules.items():
        # Iterate over the items (variable and rule) in 'rules' dictionary
        if var not in cfg['Vars']:
            # Check if the variable is not defined in 'Vars' section of 'cfg'
            print(f"\nError: Invalid variable {var}. Make sure you've written it in Vars section\n")
            return 0

        for options in rule:
            # Iterate over the options in the rule
            for option in options:
                # Iterate over the elements in each option
                if option not in cfg['Sigma'] and option not in cfg['Vars']:
                    # Check if the option is not defined in 'Sigma' or 'Vars' section of 'cfg'
                    print(f"\nError: option {option} from rules list at variable {var} doesn't exist."
                          f"\nHint: Make sure you've written it in Vars section or in Sigma section on a NEW line each.\n")
                    return 0

    return 1  # Return 1 to indicate successful validation


# validation function:
def isvalid(cfg):
    # Check if the configuration 'cfg' is valid by validating variables, sigma, and rules
    return validate_vars(cfg['Vars']) and validate_sigma(cfg['Sigma']) and validate_rules(cfg['Rules'], cfg)


# word genrator:
def generate_word(cfg, seed=None):
    # Generate a word based on the given configuration 'cfg'
    if seed is not None:
        random.seed(seed)  # Set the random seed if provided

    start_var = cfg['Vars'][0]  # Get the first variable from 'Vars' section as the starting variable
    word = generate_word_rec(start_var, cfg)  # Generate the word recursively

    return word


def generate_word_rec(var, cfg):
    # Recursive function to generate a word for the given variable 'var' and configuration 'cfg'
    if var not in cfg['Rules']:
        # If the variable does not have any rules defined, return the variable itself as the word
        return var

    rule_list = cfg['Rules'][var]  # Get the rules for the variable
    rand_rule = random.choice(rule_list)  # Choose a random rule from the rule list
    word_list = [generate_word_rec(symbol, cfg) for symbol in rand_rule]  # Generate words for each symbol in the rule
    word = ' '.join(word_list)  # Combine the generated words into a single word

    return word


# generating 10 examples:
def show_my_words(cfg):
    words = []  # List to store the generated words, to not repeat them in the next example
    k = 0  # Counter for the number of words generated

    while(k <= 10):
        word = generate_word(cfg)  # Generate a word

        if word not in words:
            # If the generated word is not already in the list, print it, add it to the list, and increment the counter
            print(f"{k}.) {word}")
            words.append(word)
            k += 1

