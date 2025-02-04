punctuation_dict = {
    "，": ",",
    "。": ".",
}
translation_table = str.maketrans(punctuation_dict)
stop_str = "<|im_end|>"


def svg_to_html(svg_content, output_filename):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Embedded in HTML</title>
    </head>
    <body>
        <svg width="2100" height="15000" xmlns="http://www.w3.org/2000/svg">
            {svg_content}
        </svg>
    </body>
    </html>
    """

    with open(output_filename, "w") as file:
        file.write(html_content)


def render_ocr_text(text, result_path, format_text=False):
    if text.endswith(stop_str):
        text = text[: -len(stop_str)]
    text = text.strip()

    if "**kern" in text:
        import verovio

        tk = verovio.toolkit()
        tk.loadData(text)
        tk.setOptions(
            {
                "pageWidth": 2100,
                "footer": "none",
                "barLineWidth": 0.5,
                "beamMaxSlope": 15,
                "staffLineWidth": 0.2,
                "spacingStaff": 6,
            }
        )
        tk.getPageCount()
        svg = tk.renderToSVG()
        svg = svg.replace('overflow="inherit"', 'overflow="visible"')

        svg_to_html(svg, result_path)

    if format_text and "**kern" not in text:
        if "\\begin{tikzpicture}" not in text:
            html_path = "./render_tools/" + "/content-mmd-to-html.html"
            right_num = text.count("\\right")
            left_num = text.count("\left")

            if right_num != left_num:
                text = (
                    text.replace("\left(", "(")
                    .replace("\\right)", ")")
                    .replace("\left[", "[")
                    .replace("\\right]", "]")
                    .replace("\left{", "{")
                    .replace("\\right}", "}")
                    .replace("\left|", "|")
                    .replace("\\right|", "|")
                    .replace("\left.", ".")
                    .replace("\\right.", ".")
                )

            text = text.replace('"', "``").replace("$", "")

            outputs_list = text.split("\n")
            gt = ""
            for out in outputs_list:
                gt += '"' + out.replace("\\", "\\\\") + r"\n" + '"' + "+" + "\n"

            gt = gt[:-2]

            with open(html_path, "r") as web_f:
                lines = web_f.read()
                lines = lines.split("const text =")
                new_web = lines[0] + "const text =" + gt + lines[1]
        else:
            html_path = "./render_tools/" + "/tikz.html"
            text = text.translate(translation_table)
            outputs_list = text.split("\n")
            gt = ""
            for out in outputs_list:
                if out:
                    if (
                        "\\begin{tikzpicture}" not in out
                        and "\\end{tikzpicture}" not in out
                    ):
                        while out[-1] == " ":
                            out = out[:-1]
                            if out is None:
                                break

                        if out:
                            if out[-1] != ";":
                                gt += out[:-1] + ";\n"
                            else:
                                gt += out + "\n"
                    else:
                        gt += out + "\n"

            with open(html_path, "r") as web_f:
                lines = web_f.read()
                lines = lines.split("const text =")
                new_web = lines[0] + gt + lines[1]

        with open(result_path, "w") as web_f_new:
            web_f_new.write(new_web)