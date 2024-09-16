import pefile
import argparse
import os


def get_exported_function(pe):
    export_directory = pe.DIRECTORY_ENTRY_EXPORT
    for symbol in export_directory.symbols:
        if "PyInit" in symbol.name.decode():
            return (True, symbol.name.decode())
    return (False, "")


def rename_exported_function(pe, og_exported, custom_exported):
    export_directory = pe.DIRECTORY_ENTRY_EXPORT
    for symbol in export_directory.symbols:
        if symbol.name.decode() == og_exported:
            symbol.name = custom_exported.encode()
            return (True, pe)
    return (False, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Re-name exported function of target .pyd file."
    )
    parser.add_argument("filepath", help="target .pyd filepath")
    args = parser.parse_args()

    if args.filepath:

        target_pyd = args.filepath
        print(f"target: {target_pyd}")

        pe = pefile.PE(target_pyd)

        success, og_exported = get_exported_function(pe)

        if not success:
            raise ValueError("failed: not found exported name start with PyInit.")

        max_name_length = len(og_exported.replace("PyInit_", ""))
        print(f"found original exported name: {og_exported}")

        custom_exported = input(
            f"change {og_exported} to PyInit_$name$\nenter the $name$ you want (max length: {max_name_length}): "
        )

        if len(custom_exported) > max_name_length or custom_exported == "":
            raise ValueError(
                f"failed: name empty or name length exceed {max_name_length} characters"
            )

        full_custom_exported = f"PyInit_{custom_exported}"
        success, renamed_pe = rename_exported_function(
            pe, og_exported, full_custom_exported
        )
        if success:
            bak_path = target_pyd + ".bak"
            os.rename(target_pyd, bak_path)
            pe.write(
                os.path.join(os.path.dirname(target_pyd), f"{custom_exported}.pyd")
            )
            print(
                f"re-name exported name to {full_custom_exported} success.\nnow you can import it with 'import {custom_exported}'"
            )
        else:
            print("failed: can't re-name exported name!")

    else:
        print(f"failed: target .pyd filepath is need!")
