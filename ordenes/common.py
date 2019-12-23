from enum import Enum

class OrdenEstado(Enum):
    CREADO = 'CREADA'
    PAGADO = 'PAGADA'
    COMPLETADA = 'COMPLETADA'
    CANCELADA = 'CANCELADA'

choices = [(tag, tag.value) for tag in OrdenEstado]