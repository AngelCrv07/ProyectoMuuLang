from analizador_lexico import Lexer
from parser import Parser
from parser import imprimir_arbol


def main():
    try:
        # Leer el código fuente desde archivo
        with open("programa.muu", "r", encoding="utf-8") as archivo:
            codigo = archivo.read()

        # Análisis léxico
        lexer = Lexer(codigo)
        tokens = lexer.analizar()
        lexer.guardar_en_archivo("tokens.txt")  # opcional

        # Análisis sintáctico
        parser = Parser(tokens)
        arbol = parser.analizar()

        print("Compilación exitosa. El código es válido sintácticamente.")
        print("\nÁrbol sintáctico:")
        imprimir_arbol(arbol)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
