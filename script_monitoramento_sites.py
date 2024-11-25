import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import requests
import os

# Configurações de autenticação
credenciais_json = r"G:\Drives compartilhados\TI-Integra\Instabilidade Ferramentas da empresa\credenciais_monitoramento.json"
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_file(credenciais_json, scopes=scope)
client = gspread.authorize(credentials)

# Configuração da planilha
url_planilha = "https://docs.google.com/spreadsheets/d/1jNRC5jh0RsyuR8UaFNFpMZcwYSFZOTlGCzrFQFgRhsw/edit"
spreadsheet = client.open_by_url(url_planilha)
sheet = spreadsheet.sheet1

# Lista de sites a serem monitorados
sites = [
    "https://nucleode135175.rm.cloudtotvs.com.br/FrameHTML/Web/App/RH/PortalMeuRH/#/login",
    "https://fluig.redeinspiraeducadores.com.br/portal/home",
    "https://bibliotecacontemporaneo.centralaluno.com.br/",
    "https://consultacontemporaneo.centralaluno.com.br/",
    "https://bibliotecaecn.centralaluno.com.br/",
    "https://consultaecn.centralaluno.com.br/",
    "https://bibliotecamagnum.centralaluno.com.br/",
    "https://consultamagnum.centralaluno.com.br/",
    "https://bibliotecagea.centralaluno.com.br/",
    "https://consultagea.centralaluno.com.br/"
]

# Configuração do arquivo de log
data_atual = datetime.now().strftime("%Y-%m-%d")
caminho_log = r"G:\Drives compartilhados\TI-Integra\Instabilidade Ferramentas da empresa\log"
arquivo_log = os.path.join(caminho_log, f"monitoramento_log_{data_atual}.txt")

def registrar_log(mensagem):
    with open(arquivo_log, "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - {mensagem}\n")
    print(f"{datetime.now()} - {mensagem}")

# Classificação de tempos
def classificar_tempo(tempo_resposta):
    if tempo_resposta == "N/A":
        return "Offline"
    elif tempo_resposta <= 1:
        return "Baixo"
    elif 1 < tempo_resposta <= 3:
        return "Médio"
    else:
        return "Alto"

# Função para atualizar o check-in
def atualizar_check_in(sheet):
    registros = sheet.get_all_values()

    # Atualizar todos os registros para FALSE
    for i in range(1, len(registros)):
        sheet.update_cell(i + 1, 6, "FALSE")  # Coluna F para Check-in

# Função para monitorar os sites
def monitorar_sites():
    registros_atualizados = []
    for site in sites:
        try:
            inicio = time.time()
            response = requests.get(site, timeout=10)
            tempo_resposta = round(time.time() - inicio, 6)
            status = "Online" if response.status_code == 200 else "Offline"
            classificacao = classificar_tempo(tempo_resposta)
            novo_registro = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                site,
                status,
                tempo_resposta if status == "Online" else "N/A",
                classificacao if status == "Online" else "Offline",
                "TRUE"  # O novo registro será o Check-in mais recente
            ]
            registros_atualizados.append(novo_registro)
            registrar_log(f"Site monitorado: {site} | Status: {status} | Tempo de Resposta: {tempo_resposta} | Classificação: {classificacao}")
        except Exception as e:
            novo_registro = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                site,
                "Offline",
                "N/A",
                "Offline",
                "TRUE"  # Mesmo para erros, será marcado como o mais recente
            ]
            registros_atualizados.append(novo_registro)
            registrar_log(f"Erro ao monitorar site {site}: {str(e)}")

    # Atualizar a planilha
    atualizar_planilha(sheet, registros_atualizados)

# Função para atualizar a planilha
def atualizar_planilha(sheet, novos_registros):
    try:
        # Obter todos os registros existentes
        registros_existentes = sheet.get_all_values()

        # Atualizar todos os check-ins existentes para FALSE
        if len(registros_existentes) > 1:  # Verifica se há registros para atualizar
            range_check_in = f"F2:F{len(registros_existentes)}"  # Define o range da coluna Check-in
            valores_false = [["FALSE"]] * (len(registros_existentes) - 1)  # Cria a lista de FALSE
            sheet.update(range_check_in, valores_false)  # Atualiza toda a coluna de Check-in

        # Adicionar novos registros e definir Check-in como TRUE
        for registro in novos_registros:
            try:
                # Define a marca com base no site
                if "TOTVS" in registro[1].upper() or "FLUIG" in registro[1].upper():
                    marca = "TOTVS"
                else:
                    marca = "KOHA"

                # Adiciona o registro com a marca e TRUE no Check-in
                registro_completo = registro[:5] + ["TRUE", marca]  # Limita explicitamente as colunas (A-G)
                sheet.append_row(registro_completo)

                # Introduzir um delay para evitar exceder a quota
                time.sleep(1)  # Delay de 1 segundo
            except Exception as e:
                registrar_log(f"Erro ao adicionar registro: {str(e)}")

        registrar_log("Planilha atualizada com novos registros e Check-in corrigido.")

    except Exception as e:
        registrar_log(f"Erro ao atualizar a planilha: {str(e)}")



# Executar o monitoramento
if __name__ == "__main__":
    try:
        registrar_log("Iniciando monitoramento.")
        monitorar_sites()
        registrar_log("Monitoramento concluído com sucesso.")
    except Exception as e:
        registrar_log(f"Erro durante o monitoramento: {str(e)}")
