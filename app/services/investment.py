"""
Servicio de cálculo de inversiones (DPF — Depósito a Plazo Fijo).
Reglas ajustadas a la normativa ecuatoriana (SBS/BCE).
"""


# Tasas de retención IR según normativa ecuatoriana vigente
# < 360 días: 2%, >= 360 días: 1.75%  (referencial, configurable)
def calcular_inversion(
    capital: float,
    tasa_anual: float,   # en %
    plazo_dias: int,
) -> dict:
    """
    Calcula los rendimientos de un DPF.
    Retorna un dict con todos los valores del cálculo.
    """
    tasa_decimal = tasa_anual / 100

    # Interés bruto
    interes_bruto = round(capital * tasa_decimal * (plazo_dias / 365), 4)

    # Retención IR (Ecuador): 2% si plazo < 360, 1.75% si >= 360
    porcentaje_retencion = 2.0 if plazo_dias < 360 else 1.75
    retencion_ir = round(interes_bruto * porcentaje_retencion / 100, 4)

    # Interés neto
    interes_neto = round(interes_bruto - retencion_ir, 4)

    # Total al vencimiento
    total_vencimiento = round(capital + interes_neto, 4)

    return {
        "amount": capital,
        "term_days": plazo_dias,
        "annual_rate": tasa_anual,
        "gross_interest": interes_bruto,
        "ir_retention": retencion_ir,
        "retention_pct": porcentaje_retencion,
        "net_interest": interes_neto,
        "total_at_maturity": total_vencimiento,
    }


def calcular_tabla_comparativa(capital: float, tasa_anual: float) -> list:
    """
    Genera tabla comparativa para plazos estándar: 30, 60, 90, 180, 270, 360, 540, 720 días.
    """
    plazos = [30, 60, 90, 180, 270, 360, 540, 720]
    return [
        {**calcular_inversion(capital, tasa_anual, dias), "plazo_dias": dias}
        for dias in plazos
    ]
