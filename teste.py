from certidao_hash import CertidaoHash


hashes = {

    "SHA256":
    "123456789abcdef",

    "MD5":
    "abcdef123456"

}


arquivo = "Cadeia_Custodia_LEONARDO_FILIPE_GROCHEVESKI.pdf"


resultado = CertidaoHash.gerar(
    arquivo,
    hashes
)


print(resultado)