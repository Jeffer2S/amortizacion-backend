"""
Servicio de cálculo de tablas de amortización.
Soporta sistema francés (cuota fija) y sistema alemán (capital constante).
"""
from typing import List
from app.schemas.amortization import AmortizationRow


def calcular_tabla_francesa(
    monto: float,
    tasa_anual: float,
    plazo_meses: int,
    cobros_activos: list,
) -> List[dict]:
    """
    Sistema Francés: cuota de capital + interés constante.
    """
    i = tasa_anual / 100 / 12  # tasa mensual
    n = plazo_meses
    if i == 0:
        cuota_ki = monto / n
    else:
        cuota_ki = monto * i / (1 - (1 + i) ** (-n))

    tabla = []
    saldo = monto

    for periodo in range(1, n + 1):
        interes = round(saldo * i, 4)
        capital = round(cuota_ki - interes, 4)
        if periodo == n:
            capital = round(saldo, 4)

        # Calculo individual de cobros
        cobros_dict = {}
        for c in cobros_activos:
            val = 0.0
            if c.is_monthly:
                if c.is_percentage:
                    val = monto * c.value / 100 / 12
                else:
                    val = c.value
            else:
                if periodo == 1:
                    if c.is_percentage:
                        val = monto * c.value / 100
                    else:
                        val = c.value
            cobros_dict[c.name] = round(val, 4)

        total_cobros_mes = sum(cobros_dict.values())
        cuota_total = round(capital + interes + total_cobros_mes, 4)
        saldo_final = round(saldo - capital, 4)

        tabla.append({
            "period": periodo,
            "initial_balance": round(saldo, 4),
            "capital": capital,
            "interest": interes,
            "indirect_charges": cobros_dict,
            "total_payment": cuota_total,
            "final_balance": max(saldo_final, 0.0),
        })
        saldo = saldo_final

    return tabla


def calcular_tabla_alemana(
    monto: float,
    tasa_anual: float,
    plazo_meses: int,
    cobros_activos: list,
) -> List[dict]:
    """
    Sistema Alemán: capital constante en cada período.
    """
    i = tasa_anual / 100 / 12
    n = plazo_meses
    capital_constante = round(monto / n, 4)

    tabla = []
    saldo = monto

    for periodo in range(1, n + 1):
        interes = round(saldo * i, 4)
        capital = capital_constante
        if periodo == n:
            capital = round(saldo, 4)

        # Calculo individual de cobros
        cobros_dict = {}
        for c in cobros_activos:
            val = 0.0
            if c.is_monthly:
                if c.is_percentage:
                    val = monto * c.value / 100 / 12
                else:
                    val = c.value
            else:
                if periodo == 1:
                    if c.is_percentage:
                        val = monto * c.value / 100
                    else:
                        val = c.value
            cobros_dict[c.name] = round(val, 4)

        total_cobros_mes = sum(cobros_dict.values())
        cuota_total = round(capital + interes + total_cobros_mes, 4)
        saldo_final = round(saldo - capital, 4)

        tabla.append({
            "period": periodo,
            "initial_balance": round(saldo, 4),
            "capital": capital,
            "interest": interes,
            "indirect_charges": cobros_dict,
            "total_payment": cuota_total,
            "final_balance": max(saldo_final, 0.0),
        })
        saldo = saldo_final

    return tabla
