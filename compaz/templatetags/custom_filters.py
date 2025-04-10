from django import template

register = template.Library()

@register.filter
def sum_column(atendimentos_por_local, mes):
    """Soma todos os valores para um mês específico."""
    return sum(meses.get(mes, 0) for meses in atendimentos_por_local.values())

@register.filter
def sum_total(atendimentos_por_local):
    """Soma o total geral de atendimentos."""
    return sum(meses["Total"] for meses in atendimentos_por_local.values())

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

