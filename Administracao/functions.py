import datetime
from cevest.models import Feriado

def get_proper_casing(name):
    temp_name = name
    temp_name = temp_name.lower()
    temp_name = temp_name.title()
    return temp_name

#Python usa dias da semana como 0(segunda) até 6 (domingo)
#essa função vê se um dia da semana começando com domingo como 0 é o mesmo dia em python
def compare_brazilian_to_python_weekday(br_day,py_day):
    converted_py_day = (py_day+1) % 7
    if br_day-1 == converted_py_day:
        return True
    return False

def convert_date_to_tuple(data):
    tuple_return = []
    for tuple_data in data:
        tuple_return.append((tuple_data.year,tuple_data.month, tuple_data.day))
    return tuple_return

def convert_tuple_to_data(tuple_data):
    data_return = []
    for data_tuple in tuple_data:
        data_return.append(datetime.date(data_tuple[0],data_tuple[1],data_tuple[2]))
    return data_return

def calculate_easter_date(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return datetime.date(year, month, day)

def create_not_fixed_holidays_in_db(year):
    pascoa = calculate_easter_date(year)
    terca_carnaval = pascoa - datetime.timedelta(days = 47)
    quarta_cinzas = terca_carnaval + datetime.timedelta(days = 1)
    sexta_feira_santa = pascoa - datetime.timedelta(days = 2)
    corpus_christi = pascoa + datetime.timedelta(days = 60)

    pascoa_object, created_pascoa = Feriado.objects.get_or_create(nome = "Páscoa", data = pascoa, fixo = False)
    terca_carnaval_object, created_terca_carnaval = Feriado.objects.get_or_create(nome = "Carnaval", data = terca_carnaval, fixo = False)
    quarta_cinzas_object, created_quarta_cinzas = Feriado.objects.get_or_create(nome = "Quarta-feira de Cinzas", data = quarta_cinzas, fixo = False)
    sexta_feira_santa_object, created_sexta_feira_santa = Feriado.objects.get_or_create(nome = "Sexta-feira Santa", data = sexta_feira_santa, fixo = False)
    corpus_christi_object, created_corpus_christi = Feriado.objects.get_or_create(nome = "Corpus Christi", data = corpus_christi, fixo = False) 

def is_date_holiday(data):
    feriados = Feriado.objects.all()
    for feriado in feriados:
        if feriado.fixo:
            #se o feriado for fixo, compara só o dia e o mês
            if data.month == feriado.data.month and data.day == feriado.data.day:
                return True
        else:
            #se o feriado não for fixo, compara o dia, mês e ano
            if data == feriado.data:
                return True
    return False

def create_select_choices(datas):
    choices = []
    i = 0
    for dia in datas:
        choices.append((i,dia.strftime("%d/%m")))
        i+=1
    return choices
