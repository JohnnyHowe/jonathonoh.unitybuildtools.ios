REGULAR=None
WARNING="#f1c40f"
ERROR="#e06c75"
SUCCESS="#98c379"


def pretty_print(*args, color=None, **kwargs):
    text = " ".join(str(a) for a in args)  # join everything manually
    if not color:
        print(text, **kwargs)
        return

    color = color.lstrip("#")
    r, g, b = (int(color[i:i+2], 16) for i in (0, 2, 4))
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)
