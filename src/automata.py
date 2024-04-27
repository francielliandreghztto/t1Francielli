from collections import defaultdict

def load_automata(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        Sigma = set(lines[0].split())
        Q = lines[1].split()
        F = lines[2].split()
        q0 = lines[3].strip()
        transitions = lines[4:]

        delta = defaultdict(dict)
        for transition in transitions:
            state_from, symbol, state_to = transition.split()
            if symbol in delta[state_from]:
                raise Exception("Transição não determinística encontrada")
            delta[state_from][symbol] = state_to

        return Q, Sigma, delta, q0, set(F)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {filename} Não foi encontrado")
    except Exception as e:
        raise Exception(f"Erro ao converte arquivo: {str(e)}")

def process(automata, words):
    Q, Sigma, delta, q0, F = automata
    results = {}

    for word in words:
        current_state = q0
        for char in word:
            if char not in Sigma:
                results[word] = "INVÁLIDA"
                break
            try:
                current_state = delta[current_state][char]
            except KeyError:
                results[word] = "REJEITA"
                break
        else:
            results[word] = "ACEITA" if current_state in F else "REJEITA"
    
    return results
