import json

try:
    with open('Feira de ciências/perguntas.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        print("Dados carregados com sucesso:", data)
except FileNotFoundError:
    print("Arquivo perguntas.json não encontrado.")
except json.JSONDecodeError:
    print("Erro ao decodificar JSON.")
except Exception as e:
    print("Ocorreu um erro:", e)
