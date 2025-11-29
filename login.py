import re
import firebase_admin
from firebase_admin import credentials, firestore
import webview

# ===== Conexão com Firebase =====
cred = credentials.Certificate("register-c4290-firebase-adminsdk-fbsvc-86ac68d5a4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ===== Validações =====
def validar_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email)) and len(email) <= 50

def validar_senha(senha):
    return senha.strip() != "" and 4 <= len(senha) <= 10

# ===== Classe acessível pelo HTML =====
class API:
    def login(self, email, senha):
        if not validar_email(email):
            return "❌ E-mail inválido!"
        if not validar_senha(senha):
            return "❌ Senha inválida!"

        # === Procurar usuário no Firebase ===
        usuarios = db.collection("usuarios").where("email", "==", email).stream()

        usuario_encontrado = None
        for user in usuarios:
            usuario_encontrado = user.to_dict()
            break

        if usuario_encontrado is None:
            return "❌ Usuário não encontrado!"

        if usuario_encontrado["senha"] != senha:
            return "❌ Senha incorreta!"

        return f"✅ Login realizado! Bem-vindo(a), {usuario_encontrado['nome']}!"

# ===== Abrir janela com HTML =====
if __name__ == "__main__":
    api = API()
    webview.create_window("Login - Hábitos+", "login.html", js_api=api)
    webview.start()
