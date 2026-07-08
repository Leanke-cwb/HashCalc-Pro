import os
import subprocess
import platform

from datetime import datetime

from certidao_hash import CertidaoHash
from hash_utils import HashCalculator


from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QCheckBox,
    QProgressBar,
    QFileDialog,
    QGroupBox,
    QLineEdit,
)


from PySide6.QtCore import (
    Qt,
    QThread,
    Signal
)



class HashWorker(QThread):

    progresso = Signal(int)
    finalizado = Signal(dict)
    erro = Signal(str)


    def __init__(self, arquivo, algoritmos):

        super().__init__()

        self.arquivo = arquivo
        self.algoritmos = algoritmos



    def run(self):

        try:

            calc = HashCalculator(
                self.arquivo
            )


            resultado = calc.calcular(
                self.algoritmos,
                self.progresso.emit
            )


            self.finalizado.emit(
                resultado
            )


        except Exception as e:

            self.erro.emit(
                str(e)
            )




class MainWindow(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "HashCalc Pro"
        )


        self.resize(
            900,
            700
        )


        self.arquivo = ""

        self.hashes = {}


        self.criar_interface()



    def gerarCertidao(self):


        if not self.hashes:

            self.status.setText(
                "Calcule o hash antes de gerar a certidão."
            )

            return



        arquivo = CertidaoHash.gerar(

            self.arquivo,

            self.hashes

        )


        self.status.setText(

            f"Certidão criada: {arquivo}"

        )
    def criar_interface(self):


        layout = QVBoxLayout()


        titulo = QLabel(
            "HASHCALC PRO"
        )


        titulo.setAlignment(
            Qt.AlignCenter
        )


        titulo.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#00C853;
            padding:10px;
        """)


        layout.addWidget(
            titulo
        )


        linha = QHBoxLayout()


        self.txtArquivo = QLineEdit()

        self.txtArquivo.setReadOnly(
            True
        )


        self.btnAbrir = QPushButton(
            "Selecionar Arquivo"
        )


        linha.addWidget(
            self.txtArquivo
        )


        linha.addWidget(
            self.btnAbrir
        )


        layout.addLayout(
            linha
        )



        info = QGroupBox(
            "Informações do Arquivo"
        )


        infoLayout = QVBoxLayout()



        self.lblNome = QLabel(
            "Nome:"
        )


        self.lblTamanho = QLabel(
            "Tamanho:"
        )


        self.lblData = QLabel(
            "Data:"
        )


        self.lblCaminho = QLabel(
            "Caminho:"
        )



        infoLayout.addWidget(
            self.lblNome
        )


        infoLayout.addWidget(
            self.lblTamanho
        )


        infoLayout.addWidget(
            self.lblData
        )


        infoLayout.addWidget(
            self.lblCaminho
        )


        info.setLayout(
            infoLayout
        )


        layout.addWidget(
            info
        )



        grupo = QGroupBox(
            "Algoritmos"
        )


        alg = QHBoxLayout()



        self.md5 = QCheckBox(
            "MD5"
        )


        self.sha1 = QCheckBox(
            "SHA-1"
        )


        self.sha256 = QCheckBox(
            "SHA-256"
        )


        self.sha512 = QCheckBox(
            "SHA-512"
        )



        self.sha256.setChecked(
            True
        )



        alg.addWidget(
            self.md5
        )


        alg.addWidget(
            self.sha1
        )


        alg.addWidget(
            self.sha256
        )


        alg.addWidget(
            self.sha512
        )



        grupo.setLayout(
            alg
        )


        layout.addWidget(
            grupo
        )



        self.btnCalcular = QPushButton(
            "CALCULAR HASH"
        )


        self.btnCalcular.setMinimumHeight(
            45
        )


        layout.addWidget(
            self.btnCalcular
        )



        self.progress = QProgressBar()


        self.progress.setValue(
            0
        )


        layout.addWidget(
            self.progress
        )



        self.resultado = QTextEdit()


        self.resultado.setReadOnly(
            True
        )


        layout.addWidget(
            self.resultado
        )



        botoes = QHBoxLayout()



        self.btnCopiar = QPushButton(
            "Copiar Tudo"
        )


        self.btnSalvar = QPushButton(
            "Gerar Certidão"
        )


        self.btnAbrirPasta = QPushButton(
            "Abrir Pasta"
        )



        botoes.addWidget(
            self.btnCopiar
        )


        botoes.addWidget(
            self.btnSalvar
        )


        botoes.addWidget(
            self.btnAbrirPasta
        )



        layout.addLayout(
            botoes
        )



        self.status = QLabel(
            "Pronto."
        )


        layout.addWidget(
            self.status
        )



        self.setLayout(
            layout
        )



        self.btnAbrir.clicked.connect(
            self.abrirArquivo
        )


        self.btnCalcular.clicked.connect(
            self.calcular
        )


        self.btnCopiar.clicked.connect(
            self.copiarTudo
        )


        self.btnSalvar.clicked.connect(
            self.gerarCertidao
        )


        self.btnAbrirPasta.clicked.connect(
            self.abrirPasta
        )
    def abrirArquivo(self):


        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo"
        )


        if not arquivo:

            return



        self.arquivo = arquivo


        self.txtArquivo.setText(
            arquivo
        )


        tamanho = os.path.getsize(
            arquivo
        )


        data = datetime.fromtimestamp(
            os.path.getmtime(
                arquivo
            )
        )


        self.lblNome.setText(
            f"Nome: {os.path.basename(arquivo)}"
        )


        self.lblTamanho.setText(
            f"Tamanho: {tamanho:,} bytes"
        )


        self.lblData.setText(
            f"Data: {data.strftime('%d/%m/%Y %H:%M:%S')}"
        )


        self.lblCaminho.setText(
            f"Caminho: {arquivo}"
        )


        self.status.setText(
            "Arquivo selecionado."
        )



    def algoritmosSelecionados(self):


        lista = []


        if self.md5.isChecked():

            lista.append(
                "md5"
            )


        if self.sha1.isChecked():

            lista.append(
                "sha1"
            )


        if self.sha256.isChecked():

            lista.append(
                "sha256"
            )


        if self.sha512.isChecked():

            lista.append(
                "sha512"
            )


        return lista




    def calcular(self):


        if not self.arquivo:


            self.status.setText(
                "Selecione um arquivo."
            )


            return



        algoritmos = self.algoritmosSelecionados()



        if not algoritmos:


            self.status.setText(
                "Selecione pelo menos um algoritmo."
            )


            return



        self.resultado.clear()


        self.progress.setValue(
            0
        )


        self.btnCalcular.setEnabled(
            False
        )


        self.status.setText(
            "Calculando hash..."
        )



        self.worker = HashWorker(

            self.arquivo,

            algoritmos

        )



        self.worker.progresso.connect(

            self.progress.setValue

        )



        self.worker.finalizado.connect(

            self.hashFinalizado

        )



        self.worker.erro.connect(

            self.erroCalculo

        )



        self.worker.start()




    def hashFinalizado(self, hashes):


        self.hashes = hashes


        texto = ""



        for algoritmo, valor in hashes.items():


            texto += algoritmo.upper()

            texto += ":\n"

            texto += valor

            texto += "\n\n"



        self.resultado.setPlainText(

            texto

        )


        self.progress.setValue(
            100
        )


        self.btnCalcular.setEnabled(
            True
        )


        self.status.setText(
            "Hash calculado com sucesso."
        )




    def erroCalculo(self, mensagem):


        self.btnCalcular.setEnabled(
            True
        )


        self.status.setText(
            mensagem
        )




    def copiarTudo(self):


        texto = self.resultado.toPlainText()



        QApplication.clipboard().setText(

            texto

        )



        self.status.setText(

            "Hash copiado."

        )




    def abrirPasta(self):


        if not self.arquivo:

            return



        pasta = os.path.dirname(

            self.arquivo

        )



        sistema = platform.system()



        if sistema == "Windows":


            os.startfile(

                pasta

            )



        elif sistema == "Darwin":


            subprocess.Popen(

                [
                    "open",
                    pasta
                ]

            )



        else:


            subprocess.Popen(

                [
                    "xdg-open",
                    pasta
                ]

            )