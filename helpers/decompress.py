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
file = hinput("\nEnter the name of the file to be decompressed (with extension): ")

if file.endswith(".zst"):
    out_name = file[:-4]
else:
    out_name = file

new_extension = hinput(f"Enter the desired file extension for the decompressed file (default: .txt): ")

if not new_extension:
    new_extension = ".txt"

if not new_extension.startswith("."):
    new_extension = "." + new_extension

out_name += new_extension

with open(file, "rb") as f:
    compressed_data = f.read()

dctx = zstd.ZstdDecompressor()
decompressed = dctx.decompress(compressed_data)

with open(out_name, "wb") as f:
    f.write(decompressed)

hprint(f"Decompressed file saved as: {out_name}")
