from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Função para carregar motoristas
def carregar_motoristas():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motoristas.csv')
    return pd.read_csv(csv_path, encoding='ISO-8859-1', sep=";")

# Página principal com formulário de busca por CPF
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        cpf = request.form['cpf'].strip()  # Remove espaços em branco
        return redirect(url_for('resumo', cpf=cpf))
    return render_template('index.html')

# Página de resumo do motorista
@app.route('/resumo/<cpf>')
def resumo(cpf):
    df_motorista = carregar_motoristas()

    # Garantir que a coluna 'ID_MOTORISTA' seja do tipo string e remova espaços
    df_motorista['ID_MOTORISTA'] = df_motorista['ID_MOTORISTA'].astype(str).str.strip()

    # Depuração: print as primeiras linhas do dataframe
    print(f"DataFrame carregado: {df_motorista.head()}")  # Exibe as 5 primeiras linhas para depuração

    # Usando o loc para encontrar a linha correspondente ao CPF
    motorista_data = df_motorista.loc[df_motorista['ID_MOTORISTA'] == cpf]

    # Verificando se foi encontrado algum motorista
    if not motorista_data.empty:
        motorista_data = motorista_data.iloc[0].to_dict()  # Converte a série para dicionário
    else:
        motorista_data = None

    # Depuração para verificar o resultado da busca
    print(f"Motorista encontrado: {motorista_data}")  # Depuração

    return render_template('resumo.html', motorista=motorista_data)

if __name__ == '__main__':
    app.run(debug=True)
