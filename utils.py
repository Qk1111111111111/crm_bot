import re
from datetime import datetime
from dateutil import parser

def parse_date(s):
    if not s or not str(s).strip():
        return None
    s = str(s).strip().lower()
    months = {
        "января": "01", "январь": "01", "янв": "01",
        "февраля": "02", "февраль": "02", "фев": "02",
        "марта": "03", "март": "03", "мар": "03",
        "апреля": "04", "апрель": "04", "апр": "04",
        "мая": "05", "май": "05",
        "июня": "06", "июнь": "06", "июн": "06",
        "июля": "07", "июль": "07", "июл": "07",
        "августа": "08", "август": "08", "авг": "08",
        "сентября": "09", "сентябрь": "09", "сен": "09",
        "октября": "10", "октябрь": "10", "окт": "10",
        "ноября": "11", "ноябрь": "11", "ноя": "11",
        "декабря": "12", "декабрь": "12", "дек": "12",
    }
    for ru_month, num in months.items():
        s = re.sub(rf"\b{ru_month}\b", num, s)
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%d-%m-%y",
        "%d.%m.%y",
        "%d/%m/%y",
        "%d %m %Y",
        "%d %m %y",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt).date()
            return dt
        except ValueError:
            continue
    try:
        from dateutil import parser
        dt = parser.parse(s, dayfirst=True, fuzzy=True)
        return dt.date()
    except Exception:
        return None


def normalize_ru_phone(phone: str) -> str:
    """
    Приводит российский номер телефона к формату:
    +79991234567

    Поддерживает:
    - +7XXXXXXXXXX
    - 8XXXXXXXXXX
    - 9XXXXXXXXX
    - номера с пробелами, скобками, тире и т.д.
    """
    # Удаляем всё кроме цифр
    digits = re.sub(r"\D", "", phone)
    # Если номер начинается с 8
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    # Если номер начинается с 9 (без кода страны)
    elif len(digits) == 10 and digits.startswith("9"):
        digits = "7" + digits
    # Если уже начинается с 7
    elif len(digits) == 11 and digits.startswith("7"):
        pass
    else:
        raise ValueError(f"Некорректный номер телефона: {phone}")
    return f"+{digits}"