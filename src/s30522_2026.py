import random


NUCLEOTIDES = "ACGT"
LINE_WIDTH = 80


def generate_sequence(length: int) -> str:
    return "".join(random.choice(NUCLEOTIDES) for _ in range(length))


def calculate_stats(sequence: str) -> dict:
    sequence_length = len(sequence)

    stats = {}
    for nucleotide in NUCLEOTIDES:
        count = sequence.count(nucleotide)
        stats[nucleotide] = count / sequence_length * 100

    gc_count = sequence.count("G") + sequence.count("C")
    stats["gc_ratio_A"] = gc_count / sequence_length * 100

    return stats


def insert_name(sequence: str, name: str) -> str:
    while not name.isalpha():
        print("Błąd: imię może zawierać tylko litery.")
        name = input("Podaj imię: ").strip()

    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]


def format_fasta(
    seq_id: str,
    description: str,
    sequence: str,
    line_width: int = 80
) -> str:
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"

    sequence_lines = []
    for start in range(0, len(sequence), line_width):
        sequence_lines.append(sequence[start:start + line_width])

    fasta_record = header + "\n" + "\n".join(sequence_lines)
    fasta_record += "\n"

    return fasta_record


def validate_positive_int(
    prompt: str,
    min_val: int = 1,
    max_val: int = 100_000
) -> int:
    while True:
        user_value = input(prompt).strip()

        try:
            number = int(user_value)
        except ValueError:
            print(
                f"Błąd: wartość musi być liczbą całkowitą "
                f"z zakresu [{min_val}, {max_val}]."
            )
            continue

        if min_val <= number <= max_val:
            return number

        print(
            f"Błąd: wartość musi być liczbą całkowitą "
            f"z zakresu [{min_val}, {max_val}]."
        )


def validate_sequence_id(prompt: str) -> str:
    while True:
        seq_id = input(prompt).strip()

        if not seq_id:
            print("Błąd: ID sekwencji nie może być puste.")
            continue

        has_whitespace = any(char.isspace() for char in seq_id)

        if has_whitespace:
            print("Błąd: ID sekwencji nie może zawierać białych znaków.")
            continue

        return seq_id


def save_to_file(filename: str, content: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def print_stats(stats: dict, sequence_length: int) -> None:
    print()
    print(f"Statystyki sekwencji (n={sequence_length}):")

    for nucleotide in NUCLEOTIDES:
        print(f"  {nucleotide}: {stats[nucleotide]:.2f}%")

    print(f"  GC-content: {stats['gc_ratio_A']:.2f}%")


def batch_mode() -> None:
    print("[BATCH MODE]")
    sequences_qty = validate_positive_int("Podaj ilość sekwencji do wygenerowania: ")
    length = validate_positive_int("Podaj długość każdej sekwencji: ")
    seq_id = validate_sequence_id("Podaj bazowe ID sekwencji: ")
    description = input("Podaj bazowy opis sekwencji: ")

    file_content = ""

    for i in range(0, sequences_qty):
        curr_seq_id = f"{seq_id}_{i+1}"
        biological_sequence = generate_sequence(length)
        curr_fasta_content = format_fasta(
            seq_id=curr_seq_id,
            description=description,
            sequence=biological_sequence,
            line_width=LINE_WIDTH
        )

        file_content += curr_fasta_content
        file_content += "\n"

    filename = f"{seq_id}.fasta"
    save_to_file(filename, file_content)

def main():
    # length = validate_positive_int("Podaj długość sekwencji: ")
    # seq_id = validate_sequence_id("Podaj ID sekwencji: ")
    # description = input("Podaj opis sekwencji: ")
    # name = input("Podaj imię: ")

    # biological_sequence = generate_sequence(length)
    # stats = calculate_stats(biological_sequence)

    # sequence_for_file = insert_name(biological_sequence, name)
    # fasta_content = format_fasta(
    #     seq_id=seq_id,
    #     description=description,
    #     sequence=sequence_for_file,
    #     line_width=LINE_WIDTH
    # )

    # filename = f"{seq_id}.fasta"
    # save_to_file(filename, fasta_content)

    # print()
    # print(f"Sekwencja zapisana do pliku: {filename}")

    # print_stats(stats, length)

    batch_mode()


if __name__ == "__main__":
    main()