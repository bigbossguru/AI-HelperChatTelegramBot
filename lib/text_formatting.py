def text_reduce(text: str, lenght: int = 50, tolerance: int = 10) -> str:
    text_lst = text.split()
    result_index = None

    for idx in range(tolerance):
        word_pos = text_lst[lenght + idx]
        word_neg = text_lst[lenght - idx]
        if "." in word_pos:
            result_index = lenght + idx
            break
        if "." in word_neg:
            result_index = lenght - idx
            break

    result_index = result_index or lenght
    return " ".join(text_lst[: result_index + 1])


def text_validation(text: str) -> bool:
    return len(text.split("-")) >= 3
