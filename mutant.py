from typing import List
import numpy as np


# Constants & parameters
NITROGENOUS_BASES = ('A', 'T', 'C', 'G')
MINIMUM_MUTANT_GENES_HITS = 2


# Helper methods
def valid_dna_strain_length(dna_strain: str) -> bool:
    return True if len(dna_strain) == 6 else False


def valid_nitrogenous_bases(dna_strain: str) -> bool:
    base_check = [nitrogenous_base in NITROGENOUS_BASES for nitrogenous_base in dna_strain]
    return False not in base_check


def valid_dna_length(dna: List[str]) -> bool:
    return True if len(dna) == 6 else False


def validate_dna(dna: List[str]) -> bool:
    if not valid_dna_length(dna): return False
    for dna_strain in dna:
        if not valid_dna_strain_length(dna_strain) or not valid_nitrogenous_bases(dna_strain): return False
    return True


def dna_strains_string_to_array(dna: List[str]) -> List[List[str]]:
    return [list(strain) for strain in dna]


def mutant_genome_hits(dna_row: List[str]) -> int:
    gene_sequences = [dna_row[idx:idx+4] for idx in range(len(dna_row) - 4 + 1)]
    mutant_sequences = [seq.count(seq[0]) == len(seq) for seq in gene_sequences]
    return sum(mutant_sequences)


def dna_cols_to_list(dna_matrix: np.matrix) -> List[List[str]]:
    return [np.array(dna_matrix[:, col_idx]).ravel().tolist() for col_idx in range(dna_matrix.shape[1])]


def dna_diagonals_to_list(dna_matrix: np.matrix) -> List[List[str]]:
    return [np.array(dna_matrix.diagonal(idx)).ravel().tolist() for idx in range(-2, 2 + 1)]


# Challenge Level 1
def isMutant(dna: List[str]) -> bool:
    if not validate_dna(dna): raise ValueError("This is not Homo Sapiens DNA")
    # Rows
    dna_strains = dna_strains_string_to_array(dna)
    mutant_genes_qty = sum([mutant_genome_hits(dna_strain) for dna_strain in dna_strains])
    if mutant_genes_qty >= MINIMUM_MUTANT_GENES_HITS: return True
    # Cols
    dna_matrix = np.matrix(dna_strains)
    dna_cols = dna_cols_to_list(dna_matrix)
    mutant_genes_qty += sum([mutant_genome_hits(dna_strain) for dna_strain in dna_cols])
    if mutant_genes_qty >= MINIMUM_MUTANT_GENES_HITS: return True
    # Diagonals
    dna_diagonals = dna_diagonals_to_list(dna_matrix)
    mutant_genes_qty += sum([mutant_genome_hits(dna_strain) for dna_strain in dna_diagonals])
    return True if mutant_genes_qty >= MINIMUM_MUTANT_GENES_HITS else False
