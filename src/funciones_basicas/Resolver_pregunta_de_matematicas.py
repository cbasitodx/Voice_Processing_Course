import re

# Función para resolver operaciones matemáticas básicas
def resolver_operacion(pregunta):

    numeros = re.findall(r'\d+', pregunta)
    # Asegurarse de que hay al menos dos números
    if len(numeros) < 2:
        return "No entendí la operación. Proporcione al menos dos números."
    num1 = int(numeros[0])  # Tomamos los dos primeros números
    num2 = int(numeros[1])

    # Detectar la operación
    palabras = pregunta.lower().split()
    if "+" in palabras or "más" in palabras or "suma" in palabras or "sumo" in palabras or "agrega" in palabras or "agrego" in palabras:
        return f"El resultado de {num1} más {num2} es {num1 + num2}."
    elif "-" in palabras or "menos" in palabras or "resta" in palabras or "resto" in palabras or "quita" in palabras or "quito" in palabras:
        return f"El resultado de {num1} menos {num2} es {num1 - num2}."
    elif "*" in palabras or "por" in palabras or "multiplica" in palabras or "multiplico" in palabras:
        return f"El resultado de {num1} por {num2} es {num1 * num2}."
    elif "/" in palabras or "entre" in palabras or "divide" in palabras or "divido" in palabras:
        if num2 == 0:
            return "No se puede dividir entre cero."
        return f"El resultado de {num1} entre {num2} es {num1 / num2}."
    else:
        return "No entendí la operación. Por favor, pregunta sobre sumas, restas, multiplicaciones o divisiones."



pregunta = "¿Cuanto vale 18 más 14?"
respuesta = resolver_operacion(pregunta)

print("pregunta:", pregunta)
print("respuesta:", respuesta)
