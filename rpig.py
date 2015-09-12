"""
Random private IP generator
"""

from argparse import ArgumentParser
from random import randint


# https://en.wikipedia.org/wiki/Private_network#Private_IPv4_address_spaces
RANGES = {
    "24": {
        "from": "10.0.0.0",
        "to": "10.255.255.255"
    },
    "20": {
        "from": "172.16.0.0",
        "to": "172.31.255.255"
    },
    "16": {
        "from": "192.168.0.0",
        "to": "192.168.255.255"
    }
}


def generate_ip(bits):
    ip_from = RANGES[bits]["from"].split(".")
    ip_to = RANGES[bits]["to"].split(".")

    generated = []
    for index, from_part in enumerate(ip_from):
        from_part = int(from_part)
        to_part = int(ip_to[index])

        # Last segment of the IP cannot be 0 or 255
        if index == 3:
            from_part = max(from_part, 1)
            to_part = min(to_part, 254)

        generated.append(randint(from_part, to_part))

    return ".".join([
        str(i) for i in generated
    ])


if __name__ == "__main__":
    ap = ArgumentParser(description="""
    Generates private IP addresses for use in e.g. Vagrant boxes.
    """)

    choices = RANGES.keys()
    help_text = ", ".join([
        "{key}-bits: {data[from]} - {data[to]}".format(
            key=key,
            data=RANGES[key]
        )
        for key in choices
    ])

    ap.add_argument("--bits", choices=choices, default="20",
                    help=help_text)

    options = ap.parse_args()

    print(generate_ip(options.bits))
