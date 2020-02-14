from flask import jsonify


def schedules():
    '''
    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if (Autenticado(cookie)):

    sessao.cookies.set("JSESSIONID", cookie)

    siteHorarios = sessao.get("https://alunos.cefet-rj.br/aluno/ajax/aluno/quadrohorario/quadrohorario.action?matricula=" + matricula)
    siteHorariosBS = bs(siteHorarios.content, "html.parser")

    HorariosLinhas = siteHorariosBS.find(id = 'quadrohorario').find_all('tr')

    HorariosLinhasTratado = str(HorariosLinhas).replace("</div></td></div></td></div></td></div></td></div></td></div></td></tr>",'')

    HorariosLinhasTratadoBS = bs(HorariosLinhasTratado, "html.parser")

    print(HorariosLinhas)

    Horarios = []

    for linha in HorariosLinhas:
        HorariosCelulas = linha.find_all('td')

        horario = {}
        horario['intervalo'] = normalizacao(HorariosCelulas[0].get_text())
        print("-------------------------------------------")
        print(HorariosCelulas[0])
        print("-------------------------------------------")

        dias = {}
        dias['Dom'] = normalizacao(HorariosCelulas[1].get_text())
        dias['Seg'] = normalizacao(HorariosCelulas[2].get_text())
        dias['Ter'] = normalizacao(HorariosCelulas[3].get_text())
        dias['Qua'] = normalizacao(HorariosCelulas[4].get_text())
        dias['Qui'] = normalizacao(HorariosCelulas[5].get_text())
        dias['Sex'] = normalizacao(HorariosCelulas[6].get_text())
        dias['Sab'] = normalizacao(HorariosCelulas[7].get_text())

        horario['dias'] = dias

        Horarios.append(horario)

    return jsonify({"horarios":Horarios})

    TrLinhas = HorariosTabela.find_all('tr')

    for itemTrLinhas in TrLinhas:

        TdCelula = TrLinhas.find_all('td')

        for itemCelula in TdCelula:
            celula = itemCelula.find('a')
            print(celula.text)
    '''
    return jsonify({
        "code": 501,
        "error": "Nao Implementado"
    })
