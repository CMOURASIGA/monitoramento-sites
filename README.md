# **Monitoramento de Sites - Status e Performance**


## **Descrição**
Este projeto realiza o monitoramento da estabilidade e desempenho de sites críticos. Ele verifica se os sites estão online ou offline, mede o tempo de resposta e classifica a latência em "Baixo", "Médio" ou "Alto". Os dados coletados são registrados em uma planilha do Google Sheets e logs detalhados são gerados diariamente.

---

## **Funcionalidades**
- Monitorar status de sites (Online/Offline).
- Medir tempo de resposta (latência).
- Classificar o tempo de resposta em três categorias:
  - **Baixo**: ≤ 1 segundo.
  - **Médio**: > 1 e ≤ 3 segundos.
  - **Alto**: > 3 segundos.
- Atualizar automaticamente uma planilha do Google Sheets:
  - Inclui timestamp, URL, status, tempo de resposta, classificação, marca e check-in.
- Gerar logs diários em arquivos separados.

---

## **Pré-requisitos**
1. **Python 3.x** instalado.
2. Instalar as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
