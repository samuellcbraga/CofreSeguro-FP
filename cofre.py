import seguranca

mestra = [""]
def definirSenha(senha):
    mestra[0] = senha

def senhaCorreta(tentativa):
    return tentativa == mestra[0]

