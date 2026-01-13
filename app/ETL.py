import pandas as pd
import re


def clean_lines(lines: list[str]) -> list[str]:
    blacklist = [
        "entrou usando o link do grupo",
        "mudou as configurações desse grupo",
        "mudou as configurações deste grupo",
        "mudou as configurações do grupo"
        "fixou uma mensagem",
        "mudou a imagem deste grupo",
        "removeu",
        "adicionou",
        "foi adicionado(a)",
        "mudou o nome do grupo",
        "mudou a descrição do grupo",
        "mudou para",
        "(arquivo anexado)",
        "<Mídia oculta>",
        "desativou as mensagens temporárias",
        "atualizou a duração das mensagens temporárias",
        "localização em tempo real compartilhada",
        "@⁨"
    ]

    phone_pattern = re.compile(
        r"""
        (\+?\d{1,3}[\s-]?)?
        (\(?\d{2,3}\)?[\s-]?)?
        \d{4,5}[\s-]?\d{4}  
        """,
        re.VERBOSE,
    )

    cleaned = []
    for line in lines:
        line_no_phone = phone_pattern.sub("", line).strip()
        if any(bad in line_no_phone for bad in blacklist):
            continue
        if line_no_phone:
            cleaned.append(line_no_phone)

    return cleaned


def lines_to_dataframe(lines: list[str]) -> pd.DataFrame:
    pattern = re.compile(
        r"""
        (?P<data>\d{2}/\d{2}/\d{4})\s+
        (?P<hora_completa>\d{2}:\d{2})\s+-\s+:\s*
        (?P<mensagem>.*)
        """,
        re.VERBOSE,
    )

    rows = []
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue

        data = match.group("data")
        hora_completa = match.group("hora_completa")

        dia, mes, ano = data.split("/")
        hora, minuto = hora_completa.split(":")

        rows.append({
            "data": data,
            "dia": int(dia),
            "mês": int(mes),
            "ano": int(ano),
            "hora_completa": hora_completa,
            "hora": int(hora),
            "minuto": int(minuto),
            "mensagem": match.group("mensagem").strip(),
        })

    return pd.DataFrame(rows)



if __name__ == "__main__":
    
    with open('../data/data.txt', 'r') as data:
        lines = data.readlines()
        data.close()

    lines = lines[3:]
    lines_clean = clean_lines(lines)
    message_history = lines_to_dataframe(lines_clean)
    message_history.to_csv('../data/message_history.csv', index=False)