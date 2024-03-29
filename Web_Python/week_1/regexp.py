def calculate(data, findall):
    matches = findall(r"([a-c])([+-]?)=([a-c]?)([+-]?\d*)")  # Если придумать хорошую регулярку, будет просто
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        if not s:
            data[v1] = data.get(v2, 0) + int(n or 0)
        if s == '-':
            data[v1] = data[v1] - (data.get(v2, 0) + int(n or 0))
        if s == '+':
            data[v1] = data[v1] + (data.get(v2, 0) + int(n or 0))
    return data