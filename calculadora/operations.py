def add(valA, valB):
    return valA + valB


def sub(valA, valB):
    return valA - valB


def mult(valA, valB):
    return valA * valB


def div(valA, valB):
    return valA / valB


operations = {
    "+": add,
    "-": sub,
    "x": mult,
    "÷": div,
}
