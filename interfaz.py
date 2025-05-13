import tkinter as tk
from tkinter import messagebox
from analizador_lexico import Lexer
import threading

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Compilador MuuLang")
ventana.geometry("800x600")

# Área de texto para escribir código
entrada = tk.Text(ventana, height=20, width=80)
entrada.pack(pady=20)


# Función para mostrar los tokens generados
def mostrar_tokens():
    try:
        codigo = entrada.get("1.0", tk.END)  # Leer el código ingresado en el Text widget
        lexer = Lexer(codigo)  # Crear instancia de Lexer con el código
        tokens = lexer.analizar()  # Obtener los tokens

        # Mostrar los tokens en la ventana
        ventana_tokens = tk.Toplevel(ventana)  # Crear nueva ventana para los tokens
        ventana_tokens.title("Tokens Generados")
        texto_tokens = tk.Text(ventana_tokens, height=20, width=80)
        texto_tokens.pack(pady=20)

        # Insertar tokens en la ventana
        for token in tokens:
            texto_tokens.insert(tk.END, f"{token}\n")

        # Mostrar los tokens también en la consola
        for token in tokens:
            print(token)

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {e}")  # Si algo sale mal, mostrar un mensaje de error


# Función para ejecutar mostrar_tokens en un hilo separado
def ejecutar_mostrar_tokens():
    threading.Thread(target=mostrar_tokens).start()


# Botón para ver los tokens
mostrar_tokens_btn = tk.Button(ventana, text="Ver Tokens", command=ejecutar_mostrar_tokens)
mostrar_tokens_btn.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
