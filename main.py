from analizador_lexico import Lexer
from parser import Parser

def main(codigo_fuente):  # <-- ahora recibe el código como argumento
    try:
        # Análisis léxico
        lexer = Lexer(codigo_fuente)
        tokens = lexer.analizar()
        lexer.guardar_en_archivo("tokens.txt")  # opcional

        # Análisis sintáctico
        parser = Parser(tokens)
        parser.analizar()

        print(" Compilación exitosa. El código es válido sintácticamente.")

    except Exception as e:
        print(f" Error: {e}")
