from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML embutido
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro - Bubble SA</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
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
        }

        .container h2 {
            color: #fff;
            margin-bottom: 25px;
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
    </style>
</head>

<body>

    <div class="container">
        <img src="/static/Bubble SA - PNG.png" alt="Logo">

        <h2>Cadastro</h2>

        <form method="POST" action="/cadastrar">
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
                <input type="tel" name="telefone" placeholder="Telefone" required>
            </div>

            <button class="btn" type="submit">Próximo</button>
        </form>
    </div>

</body>
</html>
'''

# Página de cadastro
@app.route('/')
def cadastro():
    return render_template_string(html)

# Rota que recebe os dados
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')

    # Aqui você pode inserir no banco de dados
    print(f'Nome: {nome}, CPF: {cpf}, Telefone: {telefone}')

    return f'''
    <h1>Cadastro recebido!</h1>
    <p><b>Nome:</b> {nome}</p>
    <p><b>CPF:</b> {cpf}</p>
    <p><b>Telefone:</b> {telefone}</p>
    <a href="/">Voltar</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
