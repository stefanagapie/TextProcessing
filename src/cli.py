import typer

from visualization import EigenController

app = typer.Typer()


def word_length_interval_validation(interval: tuple[int, int]):
    lower, upper = interval
    if lower > upper:
        raise typer.BadParameter(f"The leading value {lower} cannot be greater than the trailing value {upper}.")
    return interval


def n_common_words_validation(n_common_words: int):
    if n_common_words < 1:
        raise typer.BadParameter(f"The n common words value of {n_common_words} must be greater than 0.")
    return n_common_words


def max_sentence_column_width_validation(column_width: int):
    if column_width < 40:
        raise typer.BadParameter(f"The given maximum sentence column width of {column_width} must be greater than 39.")
    return column_width


@app.command()
def main(
        word_length_interval: tuple[int, int] = typer.Option(
            (6, 8),
            help="Use to specify the smallest and largest word length.",
            show_default=False,
            callback=word_length_interval_validation),
        n_common_words: int = typer.Option(
            5,
            help="Use to specify number of common words.",
            show_default=False,
            callback=n_common_words_validation
        ),
        max_sentence_column_width: int = typer.Option(
            160,
            help="Use to specify the maximum sentence column width.",
            show_default=False,
            callback=max_sentence_column_width_validation
        )
):
    control = EigenController()
    control.run(word_length_interval, n_common_words, max_sentence_column_width)


if __name__ == "__main__":
    app()
