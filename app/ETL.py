from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

import pandas as pd

import calendar
import locale

import re


locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


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


def dataframe_to_markdown(df: pd.DataFrame, linha_onibus: str) -> str:
    md = [f"# Linha de Ônibus ({linha_onibus})\n"]

    df = df.sort_values(
        ["ano", "mês", "dia", "hora", "minuto"]
    )

    for (ano, mes, dia), g_day in df.groupby(["ano", "mês", "dia"]):
        nome_mes = calendar.month_name[mes]
        md.append(f"## {dia} de {nome_mes} de {ano}\n")

        for hora, g_hour in g_day.groupby("hora"):
            md.append(f"### {hora:02d}h\n")
            for _, row in g_hour.iterrows():
                md.append(
                    f"- {row['hora']:02d}:{row['minuto']:02d} - {row['mensagem']}"
                )
            md.append("")

    return "\n".join(md)


def markdown_to_pdf(markdown_text: str, output_pdf: str):
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for line in markdown_text.split("\n"):
        if line.startswith("# "):
            story.append(Paragraph(f"<b>{line[2:]}</b>", styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(f"<b>{line[3:]}</b>", styles["Heading2"]))
        elif line.startswith("### "):
            story.append(Paragraph(f"<b>{line[4:]}</b>", styles["Heading3"]))
        elif line.startswith("- "):
            story.append(Paragraph(line[2:], styles["Normal"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)


if __name__ == "__main__":

    data_path = "../data/"
    
    with open(f"{data_path}data.txt", "r") as data:
        lines = data.readlines()
        data.close()

    lines = lines[3:]
    lines_clean = clean_lines(lines)
    message_history = lines_to_dataframe(lines_clean)
    message_history.to_csv('../data/message_history.csv', index=False)

    markdown_text = dataframe_to_markdown(
        message_history,
        "904 - Cidade Nova 8 - Presidente Vargas"
    )

    with open(f"{data_path}message_history.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

    markdown_to_pdf(markdown_text, f"{data_path}message_history.pdf")