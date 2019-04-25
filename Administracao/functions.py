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