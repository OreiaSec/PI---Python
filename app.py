from flask import Flask, render_template_string, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

usuarios = {}

html_template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Interatividade com Usuário</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-image: url('https://i.gifer.com/se0.gif');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      background-color: rgba(11, 12, 42, 0.9);
      background-blend-mode: overlay;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

    .container, .tela1, .tela2 {
      background-color: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3);
      padding: 20px;
      border-radius: 15px;
      width: 350px;
      animation: fadeIn 1.5s ease forwards;
      text-align: center;
    }

    .umbrella-img {
      width: auto;
      height: auto;
      max-width: 90%;
      max-height: 90%;
      transform: scale(0.85);
      margin-bottom: 10px;
      opacity: 0;
      animation: fadeIn 1.5s ease forwards,
                 float 3s ease-in-out infinite,
                 pulse 1s ease-in-out infinite;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.5); }
      to { opacity: 1; transform: scale(0.85); }
    }

    @keyframes float {
      0%, 100% { transform: translateY(0) scale(0.85); }
      50% { transform: translateY(-10px) scale(0.85); }
    }

    @keyframes pulse {
      0%, 100% { transform: translateY(0) scale(0.85); }
      50% { transform: translateY(0) scale(0.95); }
    }

    h2, p, label {
      color: white;
      text-align: center;
    }

    .input-group {
      position: relative;
      width: 100%;
      margin: 10px 0;
    }

    .input-group i {
      position: absolute;
      top: 50%;
      left: 12px;
      transform: translateY(-50%);
      color: #888;
    }

    .input-group input, .input-group select {
      width: 100%;
      padding: 12px 12px 12px 36px;
      border: 1px solid #ccc;
      border-radius: 10px;
      font-size: 16px;
      transition: all 0.3s ease;
    }

    .input-group input:focus, .input-group select:focus {
      border-color: #007BFF;
      background-color: #f4faff;
      outline: none;
      box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
    }

    button {
      margin-top: 15px;
      padding: 12px 25px;
      border: none;
      background-color: #007BFF;
      color: white;
      border-radius: 10px;
      cursor: pointer;
      font-size: 16px;
      transition: background-color 0.3s ease;
      width: 100%;
    }

    button:hover {
      background-color: #0056b3;
    }

    .message {
      color: yellow;
      text-align: center;
      margin-bottom: 10px;
    }

    a {
      color: #add8e6;
    }
  </style>
</head>
<body>

<div class="container">
  <img class="umbrella-img" src="https://i.pinimg.com/originals/6a/25/79/6a25795cf9f3f1f4bfb7ae07a204b6fc.png" alt="Umbrella Logo">

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for msg in messages %}
        <div class="message">{{ msg }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  {% if page == 'register' %}
    <h2>Cadastro</h2>
    <form method="post" action="{{ url_for('register') }}">
      <div class="input-group">
        <i class="fa fa-user"></i>
        <input type="text" name="nome" placeholder="Nome completo" required>
      </div>
      <div class="input-group">
        <i class="fa fa-id-card"></i>
        <input type="text" name="cpf" placeholder="CPF" required>
      </div>
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
        <i class="fa fa-phone"></i>
        <input type="text" name="telefone" placeholder="Telefone" required>
      </div>
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="senha" placeholder="Criar senha" required>
      </div>
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="confirmar_senha" placeholder="Confirmar senha" required>
      </div>
      <button type="submit">Finalizar Cadastro</button>
    </form>
    <p>Já tem uma conta? <a href="{{ url_for('login') }}">Login aqui</a></p>

  {% elif page == 'login' %}
    <h2>Login</h2>
    <form method="post" action="{{ url_for('login') }}">
      <div class="input-group">
        <i class="fa fa-envelope"></i>
        <input type="email" name="email" placeholder="E-mail" required>
      </div>
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="senha" placeholder="Senha" required>
      </div>
      <button type="submit">Entrar</button>
    </form>
    <p>Não tem conta? <a href="{{ url_for('register') }}">Cadastre-se aqui</a></p>

  {% elif page == 'welcome' %}
    <h2>Bem-vindo, {{ usuario }}!</h2>
    <p>Login realizado com sucesso.</p>
    <a href="{{ url_for('logout') }}">Sair</a>
  {% endif %}
</div>

</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        pais = request.form['pais']
        email = request.form['email'].lower()
        telefone = request.form['telefone']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash("As senhas não correspondem.")
            return redirect(url_for('register'))

        if email in usuarios:
            flash("Usuário já cadastrado com esse e-mail.")
            return redirect(url_for('register'))

        usuarios[email] = {
            'nome': nome,
            'cpf': cpf,
            'pais': pais,
            'telefone': telefone,
            'senha': senha
        }
        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for('login'))

    return render_template_string(html_template, page='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        senha = request.form['senha']

        user = usuarios.get(email)
        if user and user['senha'] == senha:
            session['usuario'] = user['nome']
            return redirect(url_for('welcome'))
        else:
            flash("E-mail ou senha incorretos.")
            return redirect(url_for('login'))

    return render_template_string(html_template, page='login')

@app.route('/welcome')
def welcome():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login'))
    return render_template_string(html_template, page='welcome', usuario=usuario)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu com sucesso.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
