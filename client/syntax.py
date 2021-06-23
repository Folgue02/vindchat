
def parse_syntax(target:str) -> list:
    foo = ""

    target += " "
    result = []
    quoteStatus = False

    for char in target:

        # Element transition
        if char == " " and not quoteStatus:
            if foo == "":
                continue

            result.append(foo)
            foo = ""
            continue

        # Quotes
        if char == "\"":
            if quoteStatus:
                quoteStatus = False
                continue

            else:
                quoteStatus = True
                continue

        else:
            foo += char
            continue

    return result    

