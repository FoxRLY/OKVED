from dataclasses import dataclass


@dataclass(frozen=True)
class OkvedData:
    """Данные ОКВЭД."""

    code: str
    """Код."""

    name: str
    """Вид деятельности."""

