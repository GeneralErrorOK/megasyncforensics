import base64

with open(
    "/home/willem/.local/share/data/Mega Limited/MEGAsync/MEGAsync.cfg", "r"
) as infile:
    with open("output.cfg", "w") as outfile:
        for inline in infile.readlines():
            if inline[0] == "[" or inline == "\n":
                outfile.write(inline)
                continue
            identifier, base64blob = inline.split("=", 1)
            stripped_base64 = base64blob.strip("\n").strip('"')
            outfile.write(
                f"{identifier}={base64.b64decode(stripped_base64).decode()}\n"
            )
