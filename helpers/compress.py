import zstandard as zstd

def hprint(text: str):
    try:
        with open("settings.txt", "r") as f:
            settings = f.read().strip()
        hackerMode = settings[1] == "1"
        print(f"\033[32m{text}\033[0m" if hackerMode else text)
    except:
        print(text)

def hinput(prompt: str):
    try:
        with open("settings.txt", "r") as f:
            settings = f.read().strip()
        hackerMode = settings[1] == "1"
        return input(f"\033[32m{prompt}\033[0m" if hackerMode else prompt)
    except:
        return input(prompt)

hprint("\nFILE MUST BE IN THE SAME DIRECTORY AS THE MAIN SCRIPT(BWRZ/)")

file = hinput("\nEnter the name of the file to be compressed (with extension): ")

out_name = file.rsplit('.', 1)[0] + ".zst"

with open(file, "rb") as f:
    data = f.read()

cctx = zstd.ZstdCompressor()
compressed = cctx.compress(data)

with open(out_name, "wb") as f:
    f.write(compressed)

hprint(f"Compressed file saved as: {out_name}")
