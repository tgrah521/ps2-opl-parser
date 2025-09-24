import os
import struct
import argparse

CHUNK_SIZE = 1024 * 1024 * 1024  


def read_system_cnf(iso_path):
    with open(iso_path, "rb") as f:
        data = f.read(64 * 1024) 
        text = data.decode(errors="ignore")
        for line in text.splitlines():
            if "BOOT2" in line:
                boot = line.split("\\")[-1]
                game_id = boot.split(";")[0].replace(".", "").strip()
                return game_id
    return "UNKNOWN"


def split_iso(iso_path, out_dir, game_id):
    os.makedirs(out_dir, exist_ok=True)

    with open(iso_path, "rb") as f:
        i = 0
        while chunk := f.read(CHUNK_SIZE):
            filename = f"ul.{game_id}xx{str(i).zfill(2)}"
            with open(os.path.join(out_dir, filename), "wb") as out:
                out.write(chunk)
            print(f"[OK] Geschrieben: {filename}")
            i += 1
    return i


def write_ulcfg(cfg_path, game_id, name, parts, size_bytes, media=0x12):

    entry_size = 0x70
    with open(cfg_path, "ab") as f:
        name_bytes = name.encode("ascii", "ignore")[:64]
        name_bytes = name_bytes.ljust(64, b"\x00")

        id_bytes = game_id.encode("ascii", "ignore")[:16]
        id_bytes = id_bytes.ljust(16, b"\x00")

        entry = struct.pack(
            "<64s16sIIB",
            name_bytes,
            id_bytes,
            parts,
            size_bytes,
            media
        )
        f.write(entry)
    print(f"[OK] ul.cfg erweitert: {name}")


def add_game(iso_path, out_dir, game_name=None):
    game_id = read_system_cnf(iso_path)
    if game_id == "UNKNOWN":
        print("[WARNUNG] Konnte SYSTEM.CNF nicht auslesen – ID manuell setzen!")
        game_id = os.path.splitext(os.path.basename(iso_path))[0][:8]

    if not game_name:
        game_name = game_id

    parts = split_iso(iso_path, out_dir, game_id)
    size_bytes = os.path.getsize(iso_path) // (1024 * 1024)

    cfg_path = os.path.join(out_dir, "ul.cfg")
    write_ulcfg(cfg_path, game_id, game_name, parts, size_bytes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="USBUtil cli")
    parser.add_argument("iso", help="Pfad zur ISO-Datei")
    parser.add_argument("out", help="Ausgabeverzeichnis (USB-Stick)")
    parser.add_argument("--name", help="Spielname (optional)")

    args = parser.parse_args()
    add_game(args.iso, args.out, args.name)
