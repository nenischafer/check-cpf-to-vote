import os
from flask import Flask, jsonify, abort
import random

app = Flask(__name__)
def validar_cpf(cpf: str) -> bool:
    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False
    
    def calcular_digito(cpf_parcial):
        soma = 0
        for i, j in enumerate(range(len(cpf_parcial)+1, 1, -1)):
            soma += int(cpf_parcial[i]) * j
        resto = (soma * 10) % 11
        return resto if resto < 10 else 0

    primeiro_digito = calcular_digito(cpf[:9])
    segundo_digito = calcular_digito(cpf[:9] + str(primeiro_digito))    
    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


@app.route('api/v1/consulta-cpf/<cpf>', methods=['GET'])
def consulta_cpf(cpf):
    
    if not validar_cpf(cpf):
        return abort(400, description="CPF inválido!")
    if random.choice([True, False]):
        return abort(404, description="CPF não encontrado!")
    else:
        status = random.choice(["ABLE_TO_VOTE", "UNABLE_TO_VOTE"])
        return jsonify({"cpf": cpf, "status": status}), 200

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 10000))
#     app.run(host='0.0.0.0', port=port)
