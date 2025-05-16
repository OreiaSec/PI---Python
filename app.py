from flask import Flask, render_template_string, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Para usar sessões e flash

# Simulação de banco de dados temporário na memória
usuarios = {}

# HTML base, simplificado para manter a estrutura funcional (pode ser melhorado)
html_template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Interatividade com Usuário</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <style>
    /* Estilos simplificados para o exemplo */
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0c2a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .container { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 15px; width: 350px; }
    .input-group { margin-bottom: 15px; position: relative; }
    .input-group i { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: #888; }
    input, select { width: 100%; padding: 10px 10px 10px 35px; border-radius: 8px; border: none; }
    button { width: 100%; padding: 10px; background: #007BFF; border: none; border-radius: 8px; color: white; font-size: 16px; cursor: pointer; }
    button:hover { background: #0056b3; }
    .message { color: yellow; margin-bottom: 10px; }
  </style>
</head>
<body>

<div class="container">
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
    <p>Já tem uma conta? <a href="{{ url_for('login') }}" style="color:#add8e6;">Login aqui</a></p>

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
    <p>Não tem conta? <a href="{{ url_for('register') }}" style="color:#add8e6;">Cadastre-se aqui</a></p>

  {% elif page == 'welcome' %}
    <h2>Bem-vindo, {{ usuario }}!</h2>
    <p>Login realizado com sucesso.</p>
    <a href="{{ url_for('logout') }}" style="color:#add8e6;">Sair</a>
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

        # Salvar usuário
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
