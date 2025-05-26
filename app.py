from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML embutido
html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Interatividade com Usuário</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
    
      <style>
        * {
          box-sizing: border-box;
        }
    
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
    
        .loading-screen, .container, .tela1, .tela2 {
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
        }
    
        button:hover {
          background-color: #0056b3;
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
            alert("Por favor, preencha todos os campos!");
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
            alert("Por favor, preencha todos os campos!");
            return;
          }
    
          if (senha !== confirmar) {
            alert("As senhas não correspondem. Por favor, tente novamente!");
            return;
          }
    
          document.querySelector(".tela1").style.display = "none";
          document.querySelector(".tela2").style.display = "flex";
        }
    
        function logar() {
          alert("Login realizado com sucesso!");
        }
    
        function irParaLogin() {
          document.querySelector(".container").style.display = "none";
          document.querySelector(".tela2").style.display = "flex";
        }
      </script>
    </head>
    <body>
    
    <!-- INÍCIO DA TELA DE CARREGAMENTO -->
    <div class="loading-screen">
      <img src="https://i.postimg.cc/26VcMNnf/Bubble-SA-PNG.png" alt="Logo Bubble SA" class="umbrella-img">
      <p>Aguarde. Estamos preparando tudo.</p>
    </div>
    
    <!-- INÍCIO DA PÁGINA A -->
    <div class="container">
      <h2>Bem-vindo!</h2>
      <p>Preencha seus dados:</p>
    
      <div class="input-group">
        <i class="fa fa-user"></i>
        <input type="text" name="nome" id="nome" placeholder="Nome completo" required>
      </div>
    
      <div class="input-group">
        <i class="fa fa-id-card"></i>
        <input type="text" name="cpf" id="cpf" placeholder="CPF" required>
      </div>
    
      <div class="input-group">
        <i class="fa fa-globe"></i>
        <select name="pais" id="pais">
          <option value="">Selecione seu país</option>
          <option value="Brasil">Brasil</option>
          <option value="Portugal">Portugal</option>
          <option value="Estados Unidos">Estados Unidos</option>
          <option value="Outro">Outro</option>
        </select>
      </div>
    
      <button onclick="irParaTela1()">Próximo</button>
      <button onclick="irParaLogin()">Já Possui cadastro? Login</button>
    </div>
    
    <!-- INÍCIO DA TELA 1 -->
    <div class="tela1">
      <h2>Informações de cadastro</h2>
    
      <div class="input-group">
        <i class="fa fa-envelope"></i>
        <input type="email" name="email" id="email" placeholder="E-mail" required>
      </div>
    
      <div class="input-group">
        <i class="fa fa-phone"></i>
        <input type="text" name="telefone" id="telefone" placeholder="Telefone" required>
      </div>
    
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="senha" id="senha" placeholder="Criar senha" required>
      </div>
    
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" name="confirmarSenha" id="confirmarSenha" placeholder="Confirmar senha" required>
      </div>
    
      <button onclick="irParaTela2()">Finalizar Cadastro</button>
    </div>
    
    <!-- INÍCIO DA TELA 2 (LOGIN) -->
    <div class="tela2">
      <h2>Login</h2>
    
      <div class="input-group">
        <i class="fa fa-envelope"></i>
        <input type="email" placeholder="E-mail">
      </div>
    
      <div class="input-group">
        <i class="fa fa-lock"></i>
        <input type="password" placeholder="Senha">
      </div>
    
      <button onclick="logar()">Entrar</button>
    </div>
    
    </body>
    </html>
