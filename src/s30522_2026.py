"""
    s30522
    06.05.2026
    Funkcjonalność części pierwszej jest wygenerowana przez chat gpt
    Wybrane funkcjonalności, zaimplementowane samodzielnie: 1., 3., 4., 5.,
"""

import random


NUCLEOTIDES = "ACGT"
LINE_WIDTH = 80


def generate_sequence(length: int) -> str:
    """generowanie sekwencji dna"""
    return "".join(random.choice(NUCLEOTIDES) for _ in range(length))


def calculate_stats(sequence: str) -> dict:
    """Funkcjonalność podstawowa"""
    """obliczanie statystyk"""
    sequence_length = len(sequence)

    stats = {}
    for nucleotide in NUCLEOTIDES:
        count = sequence.count(nucleotide)
        stats[nucleotide] = count / sequence_length * 100

    gc_count = sequence.count("G") + sequence.count("C")
    stats["gc_ratio_A"] = gc_count / sequence_length * 100

    return stats


def insert_name(sequence: str, name: str) -> str:
    """Funkcjonalność podstawowa"""
    """wstawianie imienia (wyzwanie)"""
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
    """formatowanie sekwencji do formaut fasta"""
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
    """funkcja pomocnicza, na walidację zakresu, przy inpucie usera"""
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
    """funkcja pomocnicza, na walidację id (bez whitespace'ów)"""
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
    """zapisywanie do pliku"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def print_stats(stats: dict, sequence_length: int) -> None:
    """Funkcjonalność podstawowa"""
    """funkcja pomocnicza na wypisywanie statystyk"""
    print()
    print(f"Statystyki sekwencji (n={sequence_length}):")

    for nucleotide in NUCLEOTIDES:
        print(f"  {nucleotide}: {stats[nucleotide]:.2f}%")

    print(f"  GC-content: {stats['gc_ratio_A']:.2f}%")


def batch_mode() -> None:
    """Funkcjonalność 1"""
    """Generowanie sekwencji w trybie batch mode"""
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

def to_mrna(
    dna_sequence: str
) -> str:
    """Funkcjonalność 5"""
    """Translacja DNA na mRNA z walidacją poprawności wejściowej sekwencji DNA"""
    if any(nucleotide not in NUCLEOTIDES for nucleotide in dna_sequence):
        raise ValueError('Invalid DNA sequence. Cannot translate to mRNA')

    return dna_sequence.replace("T", "U")
    
def format_fasta_dna_with_corresponding_mrna(    
    seq_id: str,
    description: str,
    dna_sequence: str,
    line_width: int = LINE_WIDTH
) -> str:
    """Funkcjonalność 5"""
    """formatowanie zawartości pliku fasta dla DNA i odpowiadającego mRNA"""
    mrna_sequence = to_mrna(dna_sequence)

    fasta_dna = format_fasta(
        seq_id=seq_id,
        description=description,
        sequence=dna_sequence,
        line_width=line_width
    )

    seq_id_mrna = f"{seq_id}_mRNA"
    description_mrna = f"{description} (mRNA)"
    fasta_mrna = format_fasta(
        seq_id=seq_id_mrna,
        description=description_mrna,
        sequence=mrna_sequence,
        line_width=line_width
    )

    return fasta_dna + "\n" + fasta_mrna

def generate_dna_with_mrna() -> None:
    """Funkcjonalność 5"""
    """Generowanie pliku DNA + odpowiadające mRNA"""
    print("Generowanie pliku fasta z sekwencją DNA oraz odpowiadającą mRNA")
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = validate_sequence_id("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")

    biological_sequence = generate_sequence(length)

    fasta_content = format_fasta_dna_with_corresponding_mrna(
        seq_id=seq_id,
        description=description,
        dna_sequence=biological_sequence,
        line_width=LINE_WIDTH
    )

    filename = f"{seq_id}.fasta"
    save_to_file(filename, fasta_content)

    print()
    print(f"Sekwencja zapisana do pliku: {filename}")

def find_pattern(sequence: str, pattern: str) -> list:
    """Funkcjonalność 3"""
    """Wyszukiwanie motywu w sekwencji."""
    """Funkcja wypisuje raport i zwraca odnalezione pozycje (indeksowanie od 1)"""
    if len(pattern) > len(sequence):
        raise ValueError("Błąd. Motyw jest dłuższy od sekwencji")

    positions_found = []
    pattern_length = len(pattern)

    for i in range(len(sequence)):
        if sequence[i:i+pattern_length] == pattern:
            positions_found.append(i+1)

    print(f"Motyw: {pattern}")
    print(f"Ilość wykrytych motywów w sekwencji: {len(positions_found)}")
    print(f"Wykryte pozycje motywu w sekwencji: {positions_found}")

    return positions_found

def to_complementary(sequence: str) -> str:
    """Funkcjonalność 4"""
    """Generowanie komplementarnej sekwencji dla wejściowej, wraz z walidacją"""
    """Obsługuje zarówno DNA i MRNA"""
    if any(nucleotide not in f"{NUCLEOTIDES}T" for nucleotide in sequence):
        raise ValueError("Invalid DNA/mRNA sequence. Cannot create complementary")

    if "T" in sequence and "U" in sequence:
        raise ValueError("Invalid sequence. Both 'T' and 'U' in sequence")

    is_dna = "T" in sequence

    dna_complementary_map = {
        "A": "T", 
        "T": "A", 
        "G": "C", 
        "C": "G"
    }

    mrna_complementary_map = {
        "A": "U",
        "U": "A",
        "G": "C", 
        "C": "G"
    }

    complementary = ""

    for i in range(len(sequence)):
        if is_dna:
            complementary += dna_complementary_map[sequence[i]]
        else:
            complementary += mrna_complementary_map[sequence[i]]

    return complementary

def to_reverse_complementary(sequence: str) -> str:
    """Funkcjonalność 4"""
    """Generowanie odwrotnie komplementarnej sekwencji dla wejściowej, wraz z walidacją"""
    """Obsługuje zarówno DNA i MRNA"""
    return to_complementary(sequence)[::-1]

def format_fasta_dna_with_complementary_and_revrese_complementary(    
    seq_id: str,
    description: str,
    dna_sequence: str,
    line_width: int = LINE_WIDTH
) -> str:
    """Funkcjonalność 4"""
    """formatowanie zawartości pliku fasta dla DNA i sekwencji komplementarnej i odwrotnie komplementarnej"""
    complementary = to_complementary(dna_sequence)
    reverse_complementary = to_reverse_complementary(dna_sequence)

    fasta_dna = format_fasta(
        seq_id=seq_id,
        description=description,
        sequence=dna_sequence,
        line_width=line_width
    )

    seq_id_complementary = f"{seq_id}_Complementary"
    description_complementary = f"{description} (Complementary)"
    fasta_complementary = format_fasta(
        seq_id=seq_id_complementary,
        description=description_complementary,
        sequence=complementary,
        line_width=line_width
    )

    seq_id_reverse_complementary = f"{seq_id}_Reverse-Complementary"
    description_reverse_complementary = f"{description} (Reverse Complementary)"
    fasta_reverse_complementary = format_fasta(
        seq_id=seq_id_reverse_complementary,
        description=description_reverse_complementary,
        sequence=reverse_complementary,
        line_width=line_width
    )

    return fasta_dna + "\n" + fasta_complementary + "\n" + fasta_reverse_complementary

def generate_dna_with_complementary_and_revrese_complementary() -> None:
    """Funkcjonalność 4"""
    """Generowanie pliku DNA + sekwencji komplementarnej i odwrotnie komplementarnej"""
    print("Generowanie pliku DNA + sekwencji komplementarnej i odwrotnie komplementarnej")
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = validate_sequence_id("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")

    biological_sequence = generate_sequence(length)

    fasta_content = format_fasta_dna_with_complementary_and_revrese_complementary(
        seq_id=seq_id,
        description=description,
        dna_sequence=biological_sequence,
        line_width=LINE_WIDTH
    )

    filename = f"{seq_id}.fasta"
    save_to_file(filename, fasta_content)

    print()
    print(f"Sekwencja zapisana do pliku: {filename}")

def main():
    """Wywołanie wszystkich funkcjonalności podstawowa + wybrane"""
    print("\n===== Podstawowa funkcjonalność częsci pierwszej =====")
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = validate_sequence_id("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    biological_sequence = generate_sequence(length)
    stats = calculate_stats(biological_sequence)

    sequence_for_file = insert_name(biological_sequence, name)
    fasta_content = format_fasta(
        seq_id=seq_id,
        description=description,
        sequence=sequence_for_file,
        line_width=LINE_WIDTH
    )

    filename = f"{seq_id}.fasta"
    save_to_file(filename, fasta_content)

    print()
    print(f"Sekwencja zapisana do pliku: {filename}")

    print_stats(stats, length)


    print("\n===== Funkcjonalność 1 - batch mode =====")
    batch_mode()

    print("\n===== Funkcjonalność 5 - generowanie DNA + mRNA do jednego pliku fasta =====")
    generate_dna_with_mrna()

    print("\n===== Funkcjonalność 3 - wykrywanie motywu w sekwencji =====")
    some_sequence = generate_sequence(800)
    for i in range(0, len(some_sequence), LINE_WIDTH):
        print(some_sequence[i:i+LINE_WIDTH])
    
    find_pattern(some_sequence, "ATG")

    print("\n===== Funkcjonalność 4 - Generowanie sekwencji z nicią komplementarną i odwrotnie komplementarną =====")
    generate_dna_with_complementary_and_revrese_complementary()

if __name__ == "__main__":
    main()