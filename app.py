from flask import Flask, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para exibir mensagens flash

# Código HTML com tooltips centralizados
html_code = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Interatividade com Usuário</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>

  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      background-image: url('https://i.gifer.com/se0.gif');
      background-size: cover;
      background-position: center;
      background-repeat: repeat;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }
    .loading-screen {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(11, 12, 42, 0.9);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      transition: opacity 1s ease-in-out;
      z-index: 10;
    }
    .container, .tela1, .tela2 {
      background-color: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3);
      width: 90%;
      max-width: 450px;
      border-radius: 20px;
      padding: 30px 20px;
      display: none;
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      height: auto;
      max-height: 90vh;
      overflow-y: auto;
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
    h2, p, label { color: white; }
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
      z-index: 2;
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
    .input-group input:invalid, .input-group select:invalid {
      border-color: #dc3545;
    }
    
    /* Tooltip centralizado */
    .tooltip {
      position: absolute;
      top: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background-color: #333;
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      white-space: nowrap;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.3s, visibility 0.3s;
      z-index: 1000;
      pointer-events: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Seta do tooltip */
    .tooltip::before {
      content: '';
      position: absolute;
      bottom: 100%;
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: transparent transparent #333 transparent;
    }
    
    /* Mostrar tooltip quando input está inválido ou vazio e focado */
    .input-group input:focus:invalid + .tooltip,
    .input-group select:focus:invalid + .tooltip,
    .input-group input:focus:placeholder-shown + .tooltip {
      opacity: 1;
      visibility: visible;
    }
    
    /* Tooltip para erro de confirmação de senha */
    .password-error {
      position: absolute;
      top: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background-color: #dc3545;
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.3s, visibility 0.3s;
      z-index: 1000;
      text-align: center;
      white-space: nowrap;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .password-error::before {
      content: '';
      position: absolute;
      bottom: 100%;
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: transparent transparent #dc3545 transparent;
    }
    
    .password-error.show {
      opacity: 1;
      visibility: visible;
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
    }
    button:hover { background-color: #0056b3; }
    .flash-message {
      color: #007BFF;
      font-weight: bold;
      margin-bottom: 10px;
    }
  </style>

  <script>
    window.onload = function () {
      setTimeout(() => {
        document.querySelector(".loading-screen").style.opacity = 0;
        setTimeout(() => {
          document.querySelector(".loading-screen").style.display = "none";
          document.querySelector(".container").style.display = "flex";
        }, 1000);
      }, 3000);
    };

    function irParaTela1() {
      let nome = document.getElementById("nome").value;
      let cpf = document.getElementById("cpf").value;
      let pais = document.getElementById("pais").value;
      if (nome === "" || cpf === "" || pais === "") {
        // Mostrar tooltips para campos vazios
        showEmptyFieldTooltips(['nome', 'cpf', 'pais']);
        return;
      }
      document.querySelector(".container").style.display = "none";
      document.querySelector(".tela1").style.display = "flex";
    }

    function irParaTela2() {
      let email = document.getElementById("email").value;
      let telefone = document.getElementById("telefone").value;
      let senha = document.getElementById("senha").value;
      let confirmar = document.getElementById("confirmarSenha").value;
      
      if (email === "" || telefone === "" || senha === "" || confirmar === "") {
        showEmptyFieldTooltips(['email', 'telefone', 'senha', 'confirmarSenha']);
        return;
      }
      if (senha !== confirmar) {
        showPasswordError();
        return;
      }
      document.getElementById("formCadastro").submit();
    }
    
    function showEmptyFieldTooltips(fieldIds) {
      fieldIds.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const tooltip = field.parentNode.querySelector('.tooltip');
        if (field.value === "" && tooltip) {
          tooltip.style.opacity = '1';
          tooltip.style.visibility = 'visible';
          setTimeout(() => {
            tooltip.style.opacity = '0';
            tooltip.style.visibility = 'hidden';
          }, 3000);
        }
      });
    }
    
    function showPasswordError() {
      const errorDiv = document.querySelector('.password-error');
      errorDiv.classList.add('show');
      setTimeout(() => {
        errorDiv.classList.remove('show');
      }, 3000);
    }

    function logar() {
      alert("Login realizado com sucesso!");
    }

    function irParaLogin() {
      document.querySelector(".container").style.display = "none";
      document.querySelector(".tela2").style.display = "flex";
    }
    
    // Remover tooltips quando o usuário digitar
    document.addEventListener('DOMContentLoaded', function() {
      const inputs = document.querySelectorAll('input, select');
      inputs.forEach(input => {
        input.addEventListener('input', function() {
          const tooltip = this.parentNode.querySelector('.tooltip');
          if (tooltip && this.value !== '') {
            tooltip.style.opacity = '0';
            tooltip.style.visibility = 'hidden';
          }
        });
      });
    });
  </script>
</head>
<body>

<form id="formCadastro" method="POST" action="/cadastrar">

<div class="loading-screen">
  <img src="https://i.postimg.cc/26VcMNnf/Bubble-SA-PNG.png" alt="Logo Bubble SA" class="umbrella-img">
  <p>Aguarde. Estamos preparando tudo.</p>
</div>

<div class="container">
  <h2>Bem-vindo!</h2>
  <p>Preencha seus dados:</p>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="flash-message">{{ messages[0] }}</div>
    {% endif %}
  {% endwith %}

  <div class="input-group">
    <i class="fa fa-user"></i>
    <input type="text" name="nome" id="nome" placeholder="Nome completo" required>
    <div class="tooltip">Por favor, preencha seu nome completo</div>
  </div>

  <div class="input-group">
    <i class="fa fa-id-card"></i>
    <input type="text" name="cpf" id="cpf" placeholder="CPF" required pattern="[0-9]{11}">
    <div class="tooltip">Digite um CPF válido (11 dígitos)</div>
  </div>

  <div class="input-group">
    <i class="fa fa-globe"></i>
    <select name="pais" id="pais" required>
      <option value="">Selecione seu país</option>
      <option value="Brasil">Brasil</option>
      <option value="Portugal">Portugal</option>
      <option value="Estados Unidos">Estados Unidos</option>
      <option value="Outro">Outro</option>
    </select>
    <div class="tooltip">Selecione seu país</div>
  </div>

  <button type="button" onclick="irParaTela1()">Próximo</button>
  <button type="button" onclick="irParaLogin()">Já possui cadastro? Login</button>
</div>

<div class="tela1">
  <h2>Informações de cadastro</h2>

  <div class="input-group">
    <i class="fa fa-envelope"></i>
    <input type="email" name="email" id="email" placeholder="E-mail" required>
    <div class="tooltip">Digite um e-mail válido</div>
  </div>

  <div class="input-group">
    <i class="fa fa-phone"></i>
    <input type="text" name="telefone" id="telefone" placeholder="Telefone" required>
    <div class="tooltip">Digite seu telefone</div>
  </div>

  <div class="input-group">
    <i class="fa fa-lock"></i>
    <input type="password" name="senha" id="senha" placeholder="Criar senha" required minlength="6">
    <div class="tooltip">A senha deve ter pelo menos 6 caracteres</div>
  </div>

  <div class="input-group">
    <i class="fa fa-lock"></i>
    <input type="password" id="confirmarSenha" placeholder="Confirmar senha" required>
    <div class="tooltip">Confirme sua senha</div>
    <div class="password-error">As senhas não correspondem!</div>
  </div>

  <button type="button" onclick="irParaTela2()">Finalizar Cadastro</button>
</div>

<div class="tela2">
  <h2>Login</h2>

  <div class="input-group">
    <i class="fa fa-envelope"></i>
    <input type="email" placeholder="E-mail" required>
    <div class="tooltip">Digite seu e-mail</div>
  </div>

  <div class="input-group">
    <i class="fa fa-lock"></i>
    <input type="password" placeholder="Senha" required>
    <div class="tooltip">Digite sua senha</div>
  </div>

  <button onclick="logar()">Entrar</button>
</div>

</form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    pais = request.form.get('pais')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')

    print(f"Dados cadastrados: {nome}, {cpf}, {pais}, {email}, {telefone}")

    flash('Cadastro realizado com sucesso! Faça o login.')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
