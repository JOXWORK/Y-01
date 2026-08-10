import re

PASCAL_INTO_SNAKE = "PASCAL_INTO_SNAKE"


class case_splitters:
    @staticmethod
    def PASCAL_INTO_SNAKE(line: str):
        parsed = re.split(
            pattern=r"(?=[A-Z])",
            string=line,
        )

        lower_words = [w.lower() for w in parsed[1:]]
        return "_".join(lower_words)


## Изучить регулярные выражения для re


def transform(
    line: str,
    case_indent: str = PASCAL_INTO_SNAKE,
) -> str:
    method = getattr(
        case_splitters,
        case_indent,
    )
    return method(line)


if __name__ == "__main__":
    result = transform(
        line="Product",
    )

    print(result)
