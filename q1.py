def string_rotation(s: str, angle: int) -> str:
    if angle == 0:
        return s
    elif angle == 90:
        return "\n".join(reversed(s))
    elif angle == 180:
        return "".join(reversed(s))
    elif angle == 270:
        return "\n".join(s)
    else:
        raise Exception("Invalid angle")


if __name__ == "__main__":
    print(string_rotation("allo", 0))
    print(string_rotation("allo", 90))
    print(string_rotation("allo", 180))
    print(string_rotation("allo", 270))
