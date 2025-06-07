#!/usr/bin/env python3

import argparse
import subprocess
import json

# ANSI formatting
BOLD = '\033[1m'
ENDC = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
__version__ = "1.0.0"


def parse_args():

    parser = argparse.ArgumentParser(description="List Docker containers")

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all containers"
    )
    parser.add_argument(
        "-s", "--slim",
        action="store_true",
        help="Show container names only (slim mode)"
    )

    args = parser.parse_args()

    return args



def get_running_docker_containers():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{json .}}"],
        capture_output=True, text=True
    )
    return [json.loads(line) for line in result.stdout.strip().splitlines()]


def get_all_docker_containers():
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{json .}}"],
        capture_output=True, text=True
    )
    return [json.loads(line) for line in result.stdout.strip().splitlines()]


def handle_state(state):
    if state == "running":
        state = f"{GREEN}[ON]{ENDC}"
    elif state == "exited":
        state = f"{RED}[OFF]{ENDC}"

    else:
        state = "Unknown"
    return state


def handle_ports(ports):
    """
    Formats a list of port mappings for clean CLI output.

    :param ports: List of port mapping strings
    :return: List of [label, value] rows suitable for row-by-row printing
    """
    ports = ports.replace(',','\n\t\t\t     ')

    return ports


def apply_colors_to_containers(containers):
    colors = [
        '\033[94m',  # blue
        GREEN,
        RED,
        '\033[96m',  # cyan
        '\033[93m',  # yellow
        '\033[95m',  # magenta
    ]
    for index, container in enumerate(containers):
        container["color"] = colors[index % len(colors)]
    return containers


def print_container_details(container):
    colored_name = f"{container['color']}{BOLD}{container['Names']}{ENDC}"
    print(colored_name)
    print_line("Container ID", container["ID"])
    print_line("Image", container["Image"])
    print_line("Command", container["Command"])
    print_line("Created", container["RunningFor"])
    print_line("Size", container["Size"])
    print_line("Status", container["Status"])
    print_line("State", handle_state(container["State"]))
    print_line("Ports", handle_ports(container["Ports"]))
    print()


def print_containers(containers, show_all=False, slim=False):    
    print()
    running_containers = 0

    print("All docker containers\n" if show_all else "Currently running docker containers\n")

    for container in containers:
        is_running = "on" in handle_state(container["State"]).lower()
        if not show_all and not is_running:
            continue

        if slim:
            colored_name = f"{container['color']}{BOLD}{container['Names']}{ENDC}"
            print(colored_name)
        else:
            print_container_details(container)

        if is_running:
            running_containers += 1

    print(f"\nTotal containers:\t{len(containers)}")
    print(f"Total running:\t\t{running_containers}")
    print()


def print_line(label, value, width=30):
    print(f"\t{BOLD}{label}:{ENDC}".ljust(width), value)


def main():
    args = parse_args()

    containers = get_all_docker_containers()

    # Apply ANSI colors to image names
    containers = apply_colors_to_containers(containers)

    # Print output
    print_containers(containers, show_all=args.all, slim=args.slim)

if __name__ == "__main__":
    main()
    
























# def parse_args():
#     parser = argparse.ArgumentParser(
#         prog="docker-pretty-images",
#         description="Minimal pretty printer for `docker images`"
#     )
#     parser.add_argument("-a", "--all", action="store_true", help="Include dangling images")
#     parser.add_argument("-s", "--slim", action="store_true", help="Slim 1-line output")
#     parser.add_argument("-v", "--version", action="store_true", help="Print version information")
#     return parser.parse_args()