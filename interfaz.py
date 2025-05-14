import tkinter as tk
from tkinter import scrolledtext
from analizador_lexico import Lexer
from parser import Parser

class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Compilador MuuLang")
        self.ventana.geometry("600x400")

        # Botones para interactuar con la interfaz
        self.boton_mostrar_tokens = tk.Button(self.ventana, text="Mostrar Tokens", command=self.mostrar_tokens)
        self.boton_mostrar_tokens.pack(pady=10)

        self.boton_mostrar_arbol = tk.Button(self.ventana, text="Mostrar Árbol Sintáctico", command=self.mostrar_arbol)
        self.boton_mostrar_arbol.pack(pady=10)

        # Área de texto para mostrar los tokens o el árbol sintáctico
        self.texto = scrolledtext.ScrolledText(self.ventana, width=70, height=15)
        self.texto.pack(pady=20)

    def mostrar_tokens(self):
        try:
            with open("tokens.txt", "r") as archivo:
                tokens = archivo.read()
                self.texto.delete(1.0, tk.END)  # Limpiar el área de texto
                self.texto.insert(tk.END, tokens)  # Insertar los tokens
        except Exception as e:
            self.texto.delete(1.0, tk.END)
            self.texto.insert(tk.END, f"Error al leer los tokens: {e}")

    def mostrar_arbol(self):
        try:
            # Leer el código fuente desde archivo
            with open("programa.muu", "r", encoding="utf-8") as archivo:
                codigo = archivo.read()

            # Análisis léxico
            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            # Análisis sintáctico
            parser = Parser(tokens)
            arbol = parser.analizar()

            # Mostrar el árbol sintáctico en la interfaz
            self.texto.delete(1.0, tk.END)  # Limpiar el área de texto
            self.texto.insert(tk.END, "Árbol Sintáctico:\n")
            self.imprimir_arbol(arbol)  # Llamar a la función para mostrar el árbol
        except Exception as e:
            self.texto.delete(1.0, tk.END)
            self.texto.insert(tk.END, f"Error: {e}")

    def imprimir_arbol(self, nodo, nivel=0):
        indentacion = "  " * nivel
        self.texto.insert(tk.END, f"{indentacion}{nodo.tipo}: {nodo.valor}\n")
        for hijo in nodo.hijos:
            self.imprimir_arbol(hijo, nivel + 1)

def main():
    ventana = tk.Tk()
    app = Interfaz(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
