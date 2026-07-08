import hashlib
import os


class HashCalculator:

    def __init__(self, arquivo):

        self.arquivo = arquivo

    def calcular(self, algoritmos, callback=None):

        hashes = {}

        if "md5" in algoritmos:
            hashes["MD5"] = hashlib.md5()

        if "sha1" in algoritmos:
            hashes["SHA1"] = hashlib.sha1()

        if "sha256" in algoritmos:
            hashes["SHA256"] = hashlib.sha256()

        if "sha512" in algoritmos:
            hashes["SHA512"] = hashlib.sha512()

        tamanho = os.path.getsize(self.arquivo)

        lido = 0

        with open(self.arquivo, "rb") as f:

            while True:

                bloco = f.read(1024 * 1024)

                if not bloco:
                    break

                lido += len(bloco)

                for h in hashes.values():
                    h.update(bloco)

                if callback:
                    callback(int(lido * 100 / tamanho))

        resultado = {}

        for nome, h in hashes.items():
            resultado[nome] = h.hexdigest().upper()

        return resultado    