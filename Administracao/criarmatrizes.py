def TreatStringForMatriz(location):
<<<<<<< HEAD
    f = open(location,"r",encoding="utf-8")
=======
    f = open(location,"r",encoding = 'utf-8')
>>>>>>> 0a84362e00340c89a39baa683c9cf16ccc39d583
    i = 0
    if f.mode == "r":
        f = f.readlines()
    for x in f:
        if x.isspace() or x == "":
            f.remove(x)
        i = i+1
    return f

def treatName(name):
    temp = name.replace("Curso: ","")
    temp = temp.replace("\n","")
    temp = temp.title()
    return temp

def getCursos(location):
    f = TreatStringForMatriz(location)
    em_curso = False
    index_disciplina = 1
    estado = 0
    nome = None
    numero_aulas = None
    carga_horaria = None
    curso = None
    lista = []
    for x in f:
        #print(estado)
        if not em_curso:
            if x.lower().startswith("curso"):
                em_curso = True
                index_disciplina = 1
                curso = x
        else:
            if x.lower().startswith("total"):
                em_curso = False
            else:
                if estado == 0:
                    if x.startswith(str(index_disciplina)):
                        index_disciplina = index_disciplina + 1
                        estado = 1
                elif estado == 1:
                    nome = x
                    estado = estado + 1
                elif estado == 2:
                    if(x.startswith('½')):
                        numero_aulas = 0
                    else:
                        numero_aulas = int(x)
                    estado = estado + 1
                elif estado == 3:
                    carga_horaria = int(x)
                    lista.append({"curso":treatName(curso), "disciplina":treatName(nome), "número de aulas":numero_aulas, "carga horária":carga_horaria})
                    estado = 0
    estado = 0
    for i in lista:
        print(i["curso"])
        print(i["disciplina"])
        print(i["número de aulas"])
        print("")
    temp_i = None
    for i in lista:
        if i["número de aulas"] == 0:
            if estado == 0:
                curso = i["curso"]
                nome = i["disciplina"]
                carga_horaria = i["carga horária"]
                estado = 1
                temp_i = i
            elif estado == 1:
                #if i["curso"]==curso:
                if nome[0]>i["disciplina"][0]:
                    i["disciplina"] = nome + " e " + i["disciplina"]
                if nome[0]<i["disciplina"][0]:
                    i["disciplina"] = i["disciplina"] + " e " + nome
                i["carga horária"] = i["carga horária"]+carga_horaria
                i["número de aulas"] = 1
                lista.remove(temp_i)
                estado = 0
    return lista
