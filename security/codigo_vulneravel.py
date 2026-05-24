# security/codigo_vulneravel.py
# Arquivo de exemplo para o Agente de Segurança analisar

import subprocess

password = "admin123"
secret = "chave-super-secreta"

def buscar_usuario(nome):
    query = "SELECT * FROM users WHERE nome = '" + nome + "'"
    return query

def executar_comando(cmd):
    subprocess.run(cmd, shell=True)

def processar_entrada(entrada):
    eval(entrada)
