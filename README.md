# PHP-in-JPG Payload Generator

I've developed this script while completing the skills assessment of the [Upload File Attacks](https://academy.hackthebox.com/module/details/136) module from the HackTheBox Academy (which I've completed successfully by getting the flag: `HTB{m********_******_***********n}` :D).
<br />
Although the script depends on the [Pillow](https://pypi.org/project/Pillow/) package, it is self-contained and does not require cloning or downloading the entire repository.

---

### ⚠️ Disclaimer
This script must be used for educational purposes **only**.
<br/>
**DO NOT** use it against systems you do not own.

---

## 🛠️ Features

- Embed a PHP payload inline or in the EXIF `Comment` tag.
- Supports custom templates for command/output embedding.
- Command-line interface with flexible options.

---

## 🔧 Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/) (`pip install Pillow`)
- [`exiftool`](https://exiftool.org/) for embedding within metadata (*optional*)

---

## 🚀 Usage

Simply:

```bash
python imagine.py -o output.jpg
```

Don't forget to check all the available options using `--help`:

```bash
username@hostname -> python3 ./imagine.py --help
usage: imagine.py [-h] [-t TEMPLATE] [-c COMMAND] [-s WIDTH HEIGHT] -o OUTPUT [-x]

Generate a JPG image with embedded PHP payload.

options:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Path to custom template file.
  -c COMMAND, --command COMMAND
                        Linux command to embed within the template.
  -p PLACEHOLDER, --placeholder PLACEHOLDER
                        Custom command placeholder within the template (default: {COMMAND})
  -s WIDTH HEIGHT, --size WIDTH HEIGHT
                        Image size as width height (default: (100, 100))
  -o OUTPUT, --output OUTPUT
                        Path to the output file
  -x, --use-exiftools   If specified, exiftools will be used for payload embedding.
```
