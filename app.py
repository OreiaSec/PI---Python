
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

usuarios = {}

html_template_step1 = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cadastro - Etapa 1</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background-image: url('https://i.gifer.com/se0.gif');
      background-size: cover;
      background-position: center;
      background-color: rgba(11, 12, 42, 0.9);
      background-blend-mode: overlay;
      margin: 0;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .container {
      background-color: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
      width: 350px;
      text-align: center;
    }
    .logo {
      max-width: 100px;
      margin-bottom: 20px;
      animation: fadeIn 1.5s ease forwards, float 3s ease-in-out infinite, pulse 1s ease-in-out infinite;
      opacity: 0;
    }
    @keyframes fadeIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .input-group { position: relative; margin-bottom: 15px; }
    .input-group i { position: absolute; top: 50%; left: 10px; transform: translateY(-50%); color: #888; }
    input { width: 100%; padding: 12px 12px 12px 35px; border-radius: 10px; border: 1px solid #ccc; }
    button { width: 100%; padding: 12px; border: none; background-color: #007BFF; color: white; border-radius: 10px; font-size: 16px; cursor: pointer; }
    button:hover { background-color: #0056b3; }
    h2, p { color: white; }
  </style>
</head>
<body>
  <div class="container">
    <img class="logo" src="{{ url_for('static', filename='logo.png') }}" alt="Logo">
    <h2>Cadastro</h2>
    <form method="post">
      <div class="input-group">
        <i class="fa fa-user"></i>
        <input type="text" name="nome" placeholder="Nome completo" required>
      </div>
      <div class="input-group">
        <i class="fa fa-id-card"></i>
        <input type="text" name="cpf" placeholder="CPF" required>
      </div>
      <div class="input-group">
        <i class="fa fa-phone"></i>
        <input type="text" name="telefone" placeholder="Telefone" required>
      </div>
      <button type="submit">Próximo</button>
    </form>
  </div>
</body>
</html>'''

html_template_step2 = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cadastro - Etapa 2</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <style>
    body { background-color: #0b0c2a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Segoe UI'; }
    .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; width: 350px; backdrop-filter: blur(10px); box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3); }
    .input-group { margin-bottom: 15px; position: relative; }
    .input-group i { position: absolute; top: 50%; left: 10px; transform: translateY(-50%); color: #888; }
    input, select { width: 100%; padding: 12px 12px 12px 36px; border-radius: 10px; border: 1px solid #ccc; }
    button { width: 100%; padding: 12px; background: #007BFF; border: none; border-radius: 10px; color: white; font-size: 16px; cursor: pointer; }
    button:hover { background: #0056b3; }
    h2 { text-align: center; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Finalizar Cadastro</h2>
    <form method="post">
      <div class="input-group">
        <i class="fa fa-globe"></i>
        <select name="pais" required>
          <option value="" disabled selected>Selecione seu país</option>
          <option value="Brasil">Brasil</option>
          <option value="Portugal">Portugal</option>
          <option value="Estados Unidos">Estados Unidos</option>
          <option value="Outro">Outro</option>
        </select>
      </div>
      <div class="input-group">
        <i class="fa fa-envelope"></i>
        <input type="email" name="email" placeholder="E-mail" required>
      </div>
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="senha" placeholder="Senha" required>
      </div>
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="confirmar_senha" placeholder="Confirmar senha" required>
      </div>
      <button type="submit">Cadastrar</button>
    </form>
  </div>
</body>
</html>'''

@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register_step1():
    if request.method == 'POST':
        session['nome'] = request.form['nome']
        session['cpf'] = request.form['cpf']
        session['telefone'] = request.form['telefone']
        session['pais'] = request.form['pais']
        return redirect(url_for('register_step2'))
    return render_template_string(html_template_step1)

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
            'pais': session.get('pais'),
            'senha': senha
        }
        session.clear()
        return "<h2 style='color:white; text-align:center; margin-top:20%;'>Cadastro concluído com sucesso!</h2>"
    return render_template_string(html_template_step2)

if __name__ == '__main__':
    app.run(debug=True)
