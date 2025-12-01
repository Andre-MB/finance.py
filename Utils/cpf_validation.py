# validar cpf
def validar_cpf(cpf):
    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    # validação de primeiro numero verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 11 - resto if resto >= 2 else 0

    if digito1 != int(cpf[9]):
        return False

    # validação de segundo numero verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 11 - resto if resto >= 2 else 0

    if digito2 != int(cpf[10]):
        return False

    return True
