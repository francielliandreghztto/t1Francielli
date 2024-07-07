"""Implementação de autômatos finitos."""


def load_automata(filename: str):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estsrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

    Um exemplo de arquivo válido é:

    ```
    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2
    ```

    Caso o arquivo seja inválido uma exceção Exception é gerada.

    """
    with open(filename, "rt", encoding="utf-8") as file:
        lines = file.readlines()
        sigma = lines[0].strip().split()
        states = lines[1].strip().split()
        final_states = lines[2].strip().split()

        for final_state in final_states:
            if final_state not in states:
                raise ValueError("Estado final não está na lista de estados.")

        initial_state = lines[3].strip()
        if initial_state not in states:
            raise ValueError("O estado inicial não está na lista de estados.")

        delta = {}
        for line in lines[4:]:
            origin, symbol, destination = line.strip().split()
            if origin not in states or destination not in states or symbol not in sigma:
                raise ValueError("Transição inválida")

            if origin not in delta:
                delta[origin] = {}
            delta[origin][symbol] = destination

    return states, sigma, delta, initial_state, final_states


def process(automaton, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """
    states, sigma, delta, initial_state, final_states = automaton
    result = {}

    for word in words:
        letters = list(word)
        invalid_state = False

        for letter in letters:
            if letter not in sigma:
                result[word] = 'INVALIDA'
                invalid_state = True
                break

        if not invalid_state:
            current_state = initial_state
            for letter in letters:
                if letter in delta.get(current_state, {}):
                    current_state = delta[current_state][letter]
                else:
                    result[word] = 'REJEITA'
                    break
            else:
                if current_state in final_states:
                    result[word] = 'ACEITA'
                else:
                    result[word] = 'REJEITA'

        if invalid_state and current_state in states:
            result[word] = 'INVALIDA'
        elif not invalid_state and current_state not in states:
            result[word] = 'REJEITA'

    return result
