import tkinter as tk
from tkinter import ttk

class CalculadoraImpuestos:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Impuestos 2025")
        
        # Constante UIT 2025
        self.UIT = 5350
        
        # Crear marco principal
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Variables para almacenar valores
        self.saldo = tk.DoubleVar(value=0)
        self.saldo_plus = tk.DoubleVar(value=0)
        self.saldo_minus = tk.DoubleVar(value=0)
        self.otros = tk.DoubleVar(value=0)
        self.total_4ta = tk.DoubleVar(value=0)
        self.quinta = tk.DoubleVar(value=0)
        self.total = tk.DoubleVar(value=0)
        self.uit7 = tk.DoubleVar(value=self.UIT * 7)
        self.uit3 = tk.DoubleVar(value=0)
        self.itf = tk.DoubleVar(value=0)
        self.impuestos = tk.DoubleVar(value=0)
        
        # Crear y colocar elementos en la interfaz
        self.crear_interfaz()
        
        # Configurar validaciones
        self.configurar_validaciones()
        
    def crear_interfaz(self):
        # Encabezados
        ttk.Label(self.frame, text="Descripción").grid(column=0, row=0, sticky=tk.W)
        ttk.Label(self.frame, text="S/.").grid(column=1, row=0, sticky=tk.W)
        
        # Campos
        campos = [
            ("Saldo", self.saldo, True),
            ("Saldo+20%", self.saldo_plus, False),
            ("Saldo-saldo20%", self.saldo_minus, False),
            ("Otros", self.otros, True),
            ("Total 4ta", self.total_4ta, False),
            ("5ta", self.quinta, True),
            ("Total", self.total, False),
            ("Deducción 7UIT max", self.uit7, False),
            ("Gastos deducibles 3UIT", self.uit3, True),
            ("ITF", self.itf, True),
            ("Impuestos a pagar", self.impuestos, False)
        ]
        
        for i, (texto, variable, editable) in enumerate(campos, 1):
            ttk.Label(self.frame, text=texto).grid(column=0, row=i, sticky=tk.W, pady=2)
            if editable:
                entry = ttk.Entry(self.frame, textvariable=variable, width=20)
            else:
                entry = ttk.Entry(self.frame, textvariable=variable, width=20, state='readonly')
            entry.grid(column=1, row=i, sticky=tk.W, pady=2)
    
    def configurar_validaciones(self):
        # Vincular eventos de cambio
        self.saldo.trace_add('write', self.calcular)
        self.otros.trace_add('write', self.calcular)
        self.quinta.trace_add('write', self.calcular)
        self.uit3.trace_add('write', self.calcular)
        self.itf.trace_add('write', self.calcular)
    
    def calcular(self, *args):
        try:
            # Obtener valores
            saldo_valor = self.saldo.get()
            otros_valor = self.otros.get()
            quinta_valor = self.quinta.get()
            uit3_valor = min(self.uit3.get(), self.UIT * 3)  # Limitar a 3 UIT
            itf_valor = self.itf.get()
            
            # Calcular Saldo+20%
            saldo_plus_valor = saldo_valor * 0.2
            self.saldo_plus.set(round(saldo_plus_valor, 2))
            
            # Calcular Saldo-saldo20%
            saldo_minus_valor = saldo_valor - saldo_plus_valor
            self.saldo_minus.set(round(saldo_minus_valor, 2))
            
            # Calcular Total 4ta
            total_4ta_valor = saldo_minus_valor + otros_valor
            self.total_4ta.set(round(total_4ta_valor, 2))
            
            # Calcular Total
            total_valor = total_4ta_valor + quinta_valor
            self.total.set(round(total_valor, 2))
            
            # Calcular Impuestos a pagar
            impuestos_valor = total_valor - self.uit7.get() - uit3_valor - itf_valor
            self.impuestos.set(round(impuestos_valor, 2))
            
             # Calcular Impuestos a pagar CORREGIDO
            base_imponible = total_valor - self.uit7.get() - uit3_valor - itf_valor
            impuestos_valor = max(base_imponible * 0.08, 0)  # Aplicar tasa del 15% y mínimo 0
            self.impuestos.set(round(impuestos_valor, 2))

        except tk.TclError:
            # Manejar errores de conversión
            pass

def main():
    root = tk.Tk()
    app = CalculadoraImpuestos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
