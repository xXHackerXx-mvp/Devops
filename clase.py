"""
Módulo de ejemplo: gestión de una cuenta bancaria simple.

Este módulo ilustra buenas prácticas de diseño de clases en Python:
- Type hints
- Docstrings (estilo Google)
- Validación de datos con excepciones propias
- Encapsulamiento mediante propiedades (@property)
- Métodos especiales (__repr__, __eq__, __str__)
- Registro de historial de transacciones
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


class SaldoInsuficienteError(Exception):
    """Se lanza cuando se intenta retirar más dinero del disponible."""


class MontoInvalidoError(Exception):
    """Se lanza cuando se intenta operar con un monto no positivo."""


@dataclass
class Transaccion:
    """Representa un movimiento realizado sobre la cuenta."""
    tipo: str          # "deposito" o "retiro"
    monto: float
    fecha: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        signo = "+" if self.tipo == "deposito" else "-"
        return f"[{self.fecha:%Y-%m-%d %H:%M:%S}] {signo}${self.monto:,.2f} ({self.tipo})"


class CuentaBancaria:
    """
    Representa una cuenta bancaria con operaciones básicas de depósito,
    retiro y consulta de saldo, incluyendo historial de transacciones.

    Attributes:
        titular: Nombre del propietario de la cuenta.
        numero_cuenta: Identificador único de la cuenta.
    """

    def __init__(self, titular: str, numero_cuenta: str, saldo_inicial: float = 0.0) -> None:
        if saldo_inicial < 0:
            raise MontoInvalidoError("El saldo inicial no puede ser negativo.")

        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self._saldo: float = saldo_inicial
        self._historial: List[Transaccion] = []

    @property
    def saldo(self) -> float:
        """Saldo actual de la cuenta (solo lectura desde fuera de la clase)."""
        return self._saldo

    @property
    def historial(self) -> List[Transaccion]:
        """Copia del historial de transacciones (evita mutación externa)."""
        return list(self._historial)

    def depositar(self, monto: float) -> None:
        """
        Agrega dinero a la cuenta.

        Args:
            monto: Cantidad a depositar. Debe ser mayor que cero.

        Raises:
            MontoInvalidoError: Si el monto es cero o negativo.
        """
        self._validar_monto(monto)
        self._saldo += monto
        self._historial.append(Transaccion("deposito", monto))

    def retirar(self, monto: float) -> None:
        """
        Retira dinero de la cuenta.

        Args:
            monto: Cantidad a retirar. Debe ser mayor que cero.

        Raises:
            MontoInvalidoError: Si el monto es cero o negativo.
            SaldoInsuficienteError: Si el saldo actual es menor al monto.
        """
        self._validar_monto(monto)
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: disponible ${self._saldo:,.2f}, "
                f"solicitado ${monto:,.2f}."
            )
        self._saldo -= monto
        self._historial.append(Transaccion("retiro", monto))

    def transferir(self, destino: "CuentaBancaria", monto: float) -> None:
        """Transfiere dinero desde esta cuenta hacia otra cuenta."""
        self.retirar(monto)
        destino.depositar(monto)

    @staticmethod
    def _validar_monto(monto: float) -> None:
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser mayor que cero.")

    def __str__(self) -> str:
        return f"Cuenta {self.numero_cuenta} ({self.titular}) - Saldo: ${self._saldo:,.2f}"

    def __repr__(self) -> str:
        return (
            f"CuentaBancaria(titular={self.titular!r}, "
            f"numero_cuenta={self.numero_cuenta!r}, saldo={self._saldo!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CuentaBancaria):
            return NotImplemented
        return self.numero_cuenta == other.numero_cuenta


if __name__ == "__main__":
    cuenta = CuentaBancaria("Diego Gómez", "001-234567", saldo_inicial=100_000)
    cuenta.depositar(50_000)
    cuenta.retirar(30_000)

    print(cuenta)
    print("Historial:")
    for mov in cuenta.historial:
        print(f"  {mov}")

    try:
        cuenta.retirar(1_000_000)
    except SaldoInsuficienteError as e:
        print(f"Error controlado: {e}")
