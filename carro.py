class Carro:
    def __init__(self, marca, modelo, año, color):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.color = color
        self.velocidad = 0

    def acelerar(self, incremento):
        self.velocidad += incremento
        print(f"El carro acelera a {self.velocidad} km/h")

    def frenar(self, decremento):
        self.velocidad = max(0, self.velocidad - decremento)
        print(f"El carro frena a {self.velocidad} km/h")

    def mostrar_info(self):
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Año: {self.año}")
        print(f"Color: {self.color}")
        print(f"Velocidad actual: {self.velocidad} km/h")


if __name__ == "__main__":
    mi_carro = Carro("Toyota", "Corolla", 2023, "Rojo")
    mi_carro.mostrar_info()
    mi_carro.acelerar(50)
    mi_carro.frenar(20)