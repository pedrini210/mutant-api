import unittest
import mutant
import numpy as np


class MutantTestCase(unittest.TestCase):
    def setUp(self):
        self.bad_strain_1 = "ATCG"  # Good nitrogenous bases, bad length
        self.bad_strain_2 = "ATCGAX"  # Bad nitrogenous bases, good length
        self.human_strain = "ATCGAG"
        self.mutant_strain_1 = "AAAACG"  # 1 mutant hit
        self.mutant_strain_2 = "AAAAAG"  # 2 mutant hits
        self.mutant_strain_3 = "AAAAAA"  # 3 mutant hits

        self.bad_dna_1 = ["CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]
        self.bad_dna_2 = ["ATGCG", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]
        self.bad_dna_3 = ["ATGCGX", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]
        self.human_dna = ["ATGCGA", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]
        self.small_human_dna = ["AAA", "AAA", "AAA"]
        self.mutant_dna_1 = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]   # 3 mutant genes
        self.mutant_dna_2 = ["AAAAAG", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]  # 2 mutant genes
        self.mutant_dna_3 = ["AAAAAA", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]  # 3 mutant genes

    def test_valid_nitrogenous_bases(self):
        self.assertFalse(mutant.valid_nitrogenous_bases(self.bad_strain_2))
        self.assertTrue(mutant.valid_nitrogenous_bases(self.bad_strain_1))
        self.assertTrue(mutant.valid_nitrogenous_bases(self.human_strain))
        self.assertTrue(mutant.valid_nitrogenous_bases(self.mutant_strain_1))
        self.assertTrue(mutant.valid_nitrogenous_bases(self.mutant_strain_2))
        self.assertTrue(mutant.valid_nitrogenous_bases(self.mutant_strain_3))

    def test_dna_strains_string_to_array(self):
        dna_control = [list("ATGCGA"), list("CCGTGC"), list("TTATCT"), list("AGAACG"), list("CGCCTA"), list("TCACTG")]
        dna_in_study = mutant.dna_strains_string_to_array(self.human_dna)
        self.assertEqual(dna_control, dna_in_study)

    def test_validate_homo_sapiens_dna(self):
        self.assertFalse(mutant.validate_homo_sapiens_dna(self.bad_dna_1))
        self.assertFalse(mutant.validate_homo_sapiens_dna(self.bad_dna_2))
        self.assertFalse(mutant.validate_homo_sapiens_dna(self.bad_dna_3))
        self.assertTrue(mutant.validate_homo_sapiens_dna(self.human_dna))
        self.assertTrue(mutant.validate_homo_sapiens_dna(self.mutant_dna_1))
        self.assertTrue(mutant.validate_homo_sapiens_dna(self.mutant_dna_2))
        self.assertTrue(mutant.validate_homo_sapiens_dna(self.mutant_dna_3))

    def test_impossible_to_be_mutant(self):
        self.assertTrue(mutant.impossible_to_be_mutant(np.matrix(mutant.dna_strains_string_to_array(self.small_human_dna))))
        self.assertFalse(mutant.impossible_to_be_mutant(np.matrix(mutant.dna_strains_string_to_array(self.human_dna))))
        self.assertFalse(mutant.impossible_to_be_mutant(np.matrix(mutant.dna_strains_string_to_array(self.mutant_dna_1))))

    def test_mutant_genome_hits(self):
        self.assertEqual(mutant.mutant_genome_hits(list(self.human_strain)), 0)
        self.assertEqual(mutant.mutant_genome_hits(list(self.small_human_dna[0])), 0)
        self.assertEqual(mutant.mutant_genome_hits(list(self.mutant_strain_1)), 1)
        self.assertEqual(mutant.mutant_genome_hits(list(self.mutant_strain_2)), 2)
        self.assertEqual(mutant.mutant_genome_hits(list(self.mutant_strain_3)), 3)

    def test_dna_cols_to_list(self):
        control_cols = [['A', 'C', 'T', 'A', 'C', 'T'], ['T', 'C', 'T', 'G', 'G', 'C'], ['G', 'G', 'A', 'A', 'C', 'A'],
                        ['C', 'T', 'T', 'A', 'C', 'C'], ['G', 'G', 'C', 'C', 'T', 'T'], ['A', 'C', 'T', 'G', 'A', 'G']]
        dna_in_study = np.matrix(mutant.dna_strains_string_to_array(self.human_dna))
        self.assertEqual(control_cols, mutant.dna_cols_to_list(dna_in_study))

    def test_dna_diagonals_to_list(self):
        control_diagonals = [['T', 'G', 'C', 'C'], ['C', 'T', 'A', 'C', 'T'], ['A', 'C', 'A', 'A', 'T', 'G'],
                             ['T', 'G', 'T', 'C', 'A'], ['G', 'T', 'C', 'G']]
        dna_in_study = np.matrix(mutant.dna_strains_string_to_array(self.human_dna))
        self.assertEqual(control_diagonals, mutant.dna_diagonals_to_list(dna_in_study))

    def test_isMutant(self):
        with self.assertRaisesRegex(ValueError, "This is not Homo Sapiens DNA"): mutant.isMutant(self.bad_dna_1)
        with self.assertRaisesRegex(ValueError, "This is not Homo Sapiens DNA"): mutant.isMutant(self.bad_dna_2)
        with self.assertRaisesRegex(ValueError, "This is not Homo Sapiens DNA"): mutant.isMutant(self.bad_dna_3)
        self.assertFalse(mutant.isMutant(self.human_dna))
        self.assertFalse(mutant.isMutant(self.small_human_dna))
        self.assertTrue(mutant.isMutant(self.mutant_dna_1))
        self.assertTrue(mutant.isMutant(self.mutant_dna_2))
        self.assertTrue(mutant.isMutant(self.mutant_dna_3))
