from flask import Flask, render_template_string, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'chave_super_segura'

# Dicionário para simular um banco de dados
usuarios = {}

# Página de cadastro - Etapa 1
html_template_step1 = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro - Etapa 1</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap" rel="stylesheet">
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <style>
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: url("/static/fundo.png") no-repeat center center fixed;
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        .container img {
            width: 100px;
            margin-bottom: 20px;
            animation: fadeIn 1.5s ease forwards, float 3s ease-in-out infinite, pulse 1s ease-in-out infinite;
            opacity: 0;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .input-field {
            display: flex;
            align-items: center;
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .input-field i {
            margin-right: 10px;
            color: #333;
        }
        .input-field input {
            border: none;
            outline: none;
            width: 100%;
            font-size: 16px;
            background: none;
        }
        .btn {
            background-color: #007bff;
            color: white;
            padding: 12px;
            width: 100%;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        h2 {
            color: white;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo">
        <h2>Cadastro</h2>
        <form method="POST">
            <div class="input-field">
                <i class="fa fa-user"></i>
                <input type="text" name="nome" placeholder="Nome completo" required>
            </div>
            <div class="input-field">
                <i class="fa fa-id-card"></i>
                <input type="text" name="cpf" placeholder="CPF" required>
            </div>
            <div class="input-field">
                <i class="fa fa-phone"></i>
                <input type="text" name="telefone" placeholder="Telefone" required>
            </div>
            <button class="btn" type="submit">Próximo</button>
        </form>
    </div>
</body>
</html>
'''

# Página de cadastro - Etapa 2
html_template_step2 = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro - Etapa 2</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap" rel="stylesheet">
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <style>
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background-color: #0b0c2a;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.9);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        .input-field {
            display: flex;
            align-items: center;
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .input-field i {
            margin-right: 10px;
            color: #333;
        }
        .input-field input, .input-field select {
            border: none;
            outline: none;
            width: 100%;
            font-size: 16px;
            background: none;
        }
        .btn {
            background-color: #007bff;
            color: white;
            padding: 12px;
            width: 100%;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        h2 {
            color: white;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Finalizar Cadastro</h2>
        <form method="POST">
            <div class="input-field">
                <i class="fa fa-globe"></i>
                <select name="pais" required>
                    <option value="" disabled selected>Selecione seu país</option>
                    <option value="Brasil">Brasil</option>
                    <option value="Portugal">Portugal</option>
                    <option value="Estados Unidos">Estados Unidos</option>
                    <option value="Outro">Outro</option>
                </select>
            </div>
            <div class="input-field">
                <i class="fa fa-envelope"></i>
                <input type="email" name="email" placeholder="E-mail" required>
            </div>
            <div class="input-field">
                <i class="fa fa-lock"></i>
                <input type="password" name="senha" placeholder="Senha" required>
            </div>
            <div class="input-field">
                <i class="fa fa-lock"></i>
                <input type="password" name="confirmar_senha" placeholder="Confirmar senha" required>
            </div>
            <button class="btn" type="submit">Cadastrar</button>
        </form>
    </div>
</body>
</html>
'''

# Rota da etapa 1
@app.route('/', methods=['GET', 'POST'])
def register_step1():
    if request.method == 'POST':
        session['nome'] = request.form['nome']
        session['cpf'] = request.form['cpf']
        session['telefone'] = request.form['telefone']
        return redirect(url_for('register_step2'))
    return render_template_string(html_template_step1)

# Rota da etapa 2
@app.route('/register2', methods=['GET', 'POST'])
def register_step2():
    if request.method == 'POST':
        pais = request.form['pais']
        email = request.form['email'].lower()
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            return "<script>alert('As senhas não coincidem.'); window.history.back();</script>"

        if email in usuarios:
            return "<script>alert('E-mail já cadastrado.'); window.history.back();</script>"

        usuarios[email] = {
            'nome': session.get('nome'),
            'cpf': session.get('cpf'),
            'telefone': session.get('telefone'),
            'pais': pais,
            'senha': senha
        }
        session.clear()
        return "<h2 style='color:white; text-align:center; margin-top:20%;'>Cadastro concluído com sucesso!</h2>"
    return render_template_string(html_template_step2)

if __name__ == '__main__':
    app.run(debug=True)
