from flask import Flask, render_template, render_template_string, request, redirect, url_for, Response
import pandas as pd
import os
import requests

app = Flask(__name__, template_folder='.')  # Configura para buscar templates na pasta principal

# Função para carregar motoristas
def carregar_motoristas():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motoristas.csv')
    df = pd.read_csv(csv_path, encoding='ISO-8859-1', sep=";")
    # Remover espaços extras das colunas
    df.columns = df.columns.str.strip()
    return df


# Página principal com formulário de busca por CPF
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').strip()  # Remove espaços em branco
        return redirect(url_for('resumo', cpf=cpf))
    return render_template('index.html')

@app.route('/resumo')
def resumo():
    print("Rota /resumo foi chamada")  # Depuração para verificar se a rota foi chamada
    cpf = request.args.get('cpf')  # Obtém o CPF a partir dos parâmetros da URL
    if not cpf:
        return "CPF não informado.", 400

    df_motorista = carregar_motoristas()

    # Garantir que a coluna 'ID_MOTORISTA' seja do tipo string e remova espaços
    df_motorista['ID_MOTORISTA'] = df_motorista['ID_MOTORISTA'].astype(str).str.strip()

    # Usando o loc para encontrar a linha correspondente ao CPF
    motorista_data = df_motorista.loc[df_motorista['ID_MOTORISTA'] == cpf]

    # Verificando se foi encontrado algum motorista
    if not motorista_data.empty:
        motorista_data = motorista_data.iloc[0].to_dict()  # Converte a série para dicionário
    else:
        motorista_data = None

    # Depuração para verificar o resultado da busca
    print(f"Motorista encontrado: {motorista_data}")  # Depuração

    # URL do arquivo HTML no GitHub
    url = "https://raw.githubusercontent.com/BNOVE/appCM/main/resumo.html"

    # Fazendo a requisição do arquivo HTML
    response = requests.get(url)

    if response.status_code != 200:
        return "Erro ao carregar a página de resumo.", 404

    # Renderiza o conteúdo HTML e injeta as informações do motorista usando render_template_string
    # O `response.text` contém o conteúdo do arquivo HTML
    html_content = response.text
    return render_template_string(html_content, motorista=motorista_data, url=url_for)


if __name__ == '__main__':
    app.run(debug=True)
