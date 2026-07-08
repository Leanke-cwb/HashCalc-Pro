from pathlib import Path
from datetime import datetime
import os


class ReportGenerator:

    @staticmethod
    def gerar(arquivo, hashes):

        caminho = Path(arquivo)

        nome_saida = caminho.with_name(
            caminho.stem + "_hashes.txt"
        )

        tamanho = os.path.getsize(arquivo)

        data_modificacao = datetime.fromtimestamp(
            os.path.getmtime(arquivo)
        )

        linhas = []

        linhas.append("=" * 70)
        linhas.append("HASHCALC PRO")
        linhas.append("=" * 70)
        linhas.append("")

        linhas.append(f"Arquivo : {caminho.name}")
        linhas.append(f"Caminho : {arquivo}")
        linhas.append(f"Tamanho : {tamanho:,} bytes")
        linhas.append(
            f"Última Modificação : {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}"
        )
        linhas.append(
            f"Data do Cálculo : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )

        linhas.append("")
        linhas.append("-" * 70)

        for algoritmo, valor in hashes.items():

            linhas.append("")
            linhas.append(algoritmo)
            linhas.append(valor)

        linhas.append("")
        linhas.append("=" * 70)
        linhas.append("Relatório gerado automaticamente pelo HashCalc Pro")
        linhas.append("=" * 70)

        with open(nome_saida, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))

        return str(nome_saida)