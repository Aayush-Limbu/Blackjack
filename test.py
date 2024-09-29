import unittest
from unittest.mock import patch, MagicMock
from blackjack import *

class TestBlackjack(unittest.TestCase):
    def setUp(self):
        self.print_mock = MagicMock()
        self.input_mock = MagicMock()
        self.rand_mock = MagicMock()
        self.blackjack = Blackjack(rand_func=self.rand_mock, input_func=self.input_mock, print_func=self.print_mock)

    def test_case_1_randomint_min_value(self):
        self.rand_mock.return_value = 1
        self.assertEqual(self.blackjack.randomint(), 1)

    def test_case_2_randomint_max_value(self):
        self.rand_mock.return_value = 13
        self.assertEqual(self.blackjack.randomint(), 13)

    def test_case_3_randomint_returns_integer(self):
        self.rand_mock.return_value = 5
        self.assertIsInstance(self.blackjack.randomint(), int)
        self.assertEqual(self.blackjack.randomint(), 5)

    
    def test_case_4_randomint_uniform_distribution(self):
        self.rand_mock.side_effect = [2, 4, 6, 8, 10]
        results = [self.blackjack.randomint() for _ in range(5)]
        self.assertEqual(results, [2, 4, 6, 8, 10])

    
    def test_case_5_randomint_mocked_randint(self):
        self.rand_mock.side_effect = [3, 7]
        self.assertEqual(self.blackjack.randomint(), 3)
        self.assertEqual(self.blackjack.randomint(), 7)

    
    def test_case_6_name_ace(self):
        self.blackjack.name(1)
        self.print_mock.assert_called_with('Drew an Ace')

    
    def test_case_7_name_king(self):
        self.blackjack.name(13)
        self.print_mock.assert_called_with('Drew a King')

    
    def test_case_8_name_number_card(self):
        self.blackjack.name(7)
        self.print_mock.assert_called_with('Drew a 7')

    
    def test_case_9_name_queen(self):
        self.blackjack.name(12)
        self.print_mock.assert_called_with('Drew a Queen')

    
    def test_case_10_name_jack(self):
        self.blackjack.name(11)
        self.print_mock.assert_called_with('Drew a Jack')

    
    def test_case_11_name_eight_with_an_prefix(self):
        self.blackjack.name(8)
        self.print_mock.assert_called_with('Drew an 8')

    
    def test_case_12_value_ace(self):
        self.assertEqual(self.blackjack.value(1), 11)

    
    def test_case_13_value_king(self):
        self.assertEqual(self.blackjack.value(13), 10)

    
    def test_case_14_value_number_card(self):
        self.assertEqual(self.blackjack.value(5), 5)

    
    def test_case_15_value_jack(self):
        self.assertEqual(self.blackjack.value(11), 10)

    
    def test_case_16_value_invalid_card(self):
        with self.assertRaises(Exception):
            self.blackjack.value(14)

    
    def test_case_17_add_two_number_cards(self):
        self.rand_mock.side_effect = [5, 7]
        total = self.blackjack.add()
        expected_calls = [unittest.mock.call('Drew a 5'), unittest.mock.call('Drew a 7')]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(total, 12)

    
    def test_case_18_add_face_and_number_card(self):
        self.rand_mock.side_effect = [11, 9]  
        total = self.blackjack.add()
        expected_calls = [unittest.mock.call('Drew a Jack'), unittest.mock.call('Drew a 9')]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(total, 19)

    
    def test_case_19_add_two_aces(self):
        self.rand_mock.side_effect = [1, 1]
        total = self.blackjack.add()
        expected_calls = [unittest.mock.call('Drew an Ace'), unittest.mock.call('Drew an Ace')]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(total, 22)  

    
    def test_case_20_add_maximum_card_values(self):
        self.rand_mock.side_effect = [13, 13]  
        total = self.blackjack.add()
        expected_calls = [unittest.mock.call('Drew a King'), unittest.mock.call('Drew a King')]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(total, 20)

    
    def test_case_21_add_minimum_card_values(self):
        self.rand_mock.side_effect = [1, 1]  
        total = self.blackjack.add()
        expected_calls = [unittest.mock.call('Drew an Ace'), unittest.mock.call('Drew an Ace')]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(total, 22)

    
    def test_case_22_check_valid_y(self):
        result = self.blackjack.check('y', 10)
        self.assertEqual(result, 'y')

    
    def test_case_23_check_valid_n(self):
        result = self.blackjack.check('n', 10)
        self.assertEqual(result, 'n')

    
    def test_case_24_check_invalid_then_y(self):
        self.input_mock.side_effect = ['invalid', 'y']
        result = self.blackjack.check('invalid', 10)
        self.assertEqual(result, 'y')
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_25_check_invalid_then_n(self):
        self.input_mock.side_effect = ['?', 'n']
        result = self.blackjack.check('?', 10)
        self.assertEqual(result, 'n')
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_26_check_multiple_invalid_then_y(self):
        self.input_mock.side_effect = ['?', 'maybe', 'y']
        result = self.blackjack.check('?', 10)
        self.assertEqual(result, 'y')
        self.assertEqual(self.print_mock.call_count, 2)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_27_usersum_blackjack(self):
        self.blackjack.uservalue = 21
        self.blackjack.usersum(21)
        self.print_mock.assert_any_call('Final hand: 21.')
        self.print_mock.assert_any_call('BLACKJACK!')

    
    def test_case_28_usersum_bust(self):
        self.blackjack.uservalue = 22
        self.blackjack.usersum(22)
        self.print_mock.assert_any_call('Final hand: 22.')
        self.print_mock.assert_any_call('BUST.')

    
    def test_case_29_usersum_hit_reach_21(self):
        self.blackjack.uservalue = 10
        self.input_mock.return_value = 'y'
        with patch.object(self.blackjack, 'randomint', return_value=11):
            with patch.object(self.blackjack, 'value', return_value=11):
                self.blackjack.usersum(10)
                self.assertEqual(self.blackjack.uservalue, 21)
                self.print_mock.assert_any_call('Final hand: 21.')
                self.print_mock.assert_any_call('BLACKJACK!')

    
    def test_case_30_usersum_hit_bust(self):
        self.blackjack.uservalue = 20
        self.input_mock.return_value = 'y'
        with patch.object(self.blackjack, 'randomint', return_value=2):
            with patch.object(self.blackjack, 'value', return_value=2):
                self.blackjack.usersum(20)
                self.assertEqual(self.blackjack.uservalue, 22)
                self.print_mock.assert_any_call('Final hand: 22.')
                self.print_mock.assert_any_call('BUST.')

    
    def test_case_31_usersum_stand(self):
        self.blackjack.uservalue = 18
        self.input_mock.return_value = 'n'
        self.blackjack.usersum(18)
        self.print_mock.assert_any_call('Final hand: 18.')
        self.assertEqual(self.blackjack.uservalue, 18)

    
    def test_case_32_dealersum_blackjack(self):
        self.blackjack.dealersum(21)
        self.print_mock.assert_any_call('Final hand: 21.')
        self.print_mock.assert_any_call('BLACKJACK!')
        self.assertEqual(self.blackjack.dealervalue, 21)

    
    def test_case_33_dealersum_bust(self):
        self.blackjack.dealersum(22)
        self.print_mock.assert_any_call('Final hand: 22.')
        self.print_mock.assert_any_call('BUST.')
        self.assertEqual(self.blackjack.dealervalue, 22)

    
    def test_case_34_dealersum_stand_at_17(self):
        self.blackjack.dealersum(17)
        self.print_mock.assert_any_call('Final hand: 17.')
        self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_35_dealersum_hit_to_17(self):
        self.blackjack.dealersum(10)
        self.rand_mock.return_value = 7  
        self.blackjack.dealersum(10)
        expected_calls = [
            unittest.mock.call('Final hand: 17.')
        ]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_36_dealersum_hit_and_bust(self):
        self.blackjack.dealersum(15)
        self.rand_mock.return_value = 10  
        self.blackjack.dealersum(15)
        expected_calls = [
            unittest.mock.call('Final hand: 25.'),
            unittest.mock.call('BUST.')
        ]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(self.blackjack.dealervalue, 25)

    
    def test_case_37_game_user_wins_dealer_bust(self):
        self.blackjack.uservalue = 20
        self.blackjack.dealervalue = 22
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("You win!")

    
    def test_case_38_game_user_wins_higher_than_dealer(self):
        self.blackjack.uservalue = 19
        self.blackjack.dealervalue = 17
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("You win!")

    
    def test_case_39_game_push(self):
        self.blackjack.uservalue = 18
        self.blackjack.dealervalue = 18
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Push.")

    
    def test_case_40_game_dealer_wins_higher(self):
        self.blackjack.uservalue = 16
        self.blackjack.dealervalue = 19
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Dealer wins!")

    
    def test_case_41_game_dealer_wins_user_busts(self):
        self.blackjack.uservalue = 23
        self.blackjack.dealervalue = 20
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Dealer wins!")

    
    def test_case_42_usersum_initial_two_aces_bust(self):
        self.blackjack.uservalue = 22  
        self.blackjack.usersum(22)
        self.print_mock.assert_any_call('Final hand: 22.')
        self.print_mock.assert_any_call('BUST.')

    
    def test_case_43_dealersum_all_aces_bust(self):
        self.blackjack.dealervalue = 22  
        self.blackjack.dealersum(22)
        self.print_mock.assert_any_call('Final hand: 22.')
        self.print_mock.assert_any_call('BUST.')
        self.assertEqual(self.blackjack.dealervalue, 22)

    
    def test_case_44_usersum_max_hits_without_busting(self):
        
        self.blackjack.uservalue = 10
        self.input_mock.side_effect = ['y', 'y', 'y', 'n']
        with patch.object(self.blackjack, 'randomint', side_effect=[3, 4, 2]):
            with patch.object(self.blackjack, 'value', side_effect=[3, 4, 2]):
                self.blackjack.usersum(10)
                self.assertEqual(self.blackjack.uservalue, 19)
                expected_calls = [
                    unittest.mock.call('Drew a 3'),
                    unittest.mock.call('Drew a 4'),
                    unittest.mock.call('Drew a 2'),
                    unittest.mock.call('Final hand: 19.')
                ]
                self.print_mock.assert_has_calls(expected_calls, any_order=False)

    
    def test_case_45_usersum_min_hits_to_blackjack(self):
        
        self.blackjack.uservalue = 10
        self.input_mock.return_value = 'y'
        with patch.object(self.blackjack, 'randomint', return_value=11):
            with patch.object(self.blackjack, 'value', return_value=10):
                self.blackjack.usersum(10)
                self.assertEqual(self.blackjack.uservalue, 20)
                
                
                
                self.blackjack.uservalue = 10
                self.input_mock.return_value = 'y'
                with patch.object(self.blackjack, 'randomint', return_value=1):
                    with patch.object(self.blackjack, 'value', return_value=11):
                        self.blackjack.usersum(10)
                        self.assertEqual(self.blackjack.uservalue, 21)
                        self.print_mock.assert_any_call('Final hand: 21.')
                        self.print_mock.assert_any_call('BLACKJACK!')

    
    def test_case_46_dealersum_hits_exactly_17(self):
        self.blackjack.dealervalue = 15
        self.rand_mock.return_value = 2  
        self.blackjack.dealersum(15)
        expected_calls = [
            unittest.mock.call('Dealer has 15.'),
            unittest.mock.call('Drew a 2'),
            unittest.mock.call('Final hand: 17.')
        ]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_47_usersum_hits_multiple_times_and_stands(self):
        self.blackjack.uservalue = 10
        self.input_mock.side_effect = ['y', 'y', 'n']
        with patch.object(self.blackjack, 'randomint', side_effect=[5, 5]):
            with patch.object(self.blackjack, 'value', side_effect=[5, 5]):
                self.blackjack.usersum(10)
                self.assertEqual(self.blackjack.uservalue, 20)
                expected_calls = [
                    unittest.mock.call('Drew a 5'),
                    unittest.mock.call('Drew a 5'),
                    unittest.mock.call('Final hand: 20.')
                ]
                self.print_mock.assert_has_calls(expected_calls, any_order=False)

    
    def test_case_48_dealersum_stands_at_17_with_multiple_aces(self):
        self.blackjack.dealervalue = 17  
        self.blackjack.dealersum(17)
        expected_calls = [
            unittest.mock.call('Final hand: 17.')
        ]
        self.print_mock.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_49_check_non_string_inputs(self):
        self.input_mock.side_effect = [123, 'y']
        with patch.object(self.blackjack, 'check', side_effect=['y']):
            with patch.object(self.blackjack, 'randomint', return_value=10):
                with patch.object(self.blackjack, 'value', return_value=10):
                    self.blackjack.usersum(10)
                    self.assertEqual(self.blackjack.uservalue, 20)
                    self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_50_game_simultaneous_blackjack_push(self):
        self.blackjack.uservalue = 21
        self.blackjack.dealervalue = 21
        with patch('builtins.print') as mock_print:
            self.blackjack.evaluate_game_result()
            mock_print.assert_any_call("Push.")

    

    
    def test_case_51_usersum_three_aces_bust(self):
        self.rand_mock.side_effect = [1, 1, 1]  
        with patch.object(self.blackjack, 'add', side_effect=self.blackjack.add):
            total = self.blackjack.add()
            self.assertEqual(total, 33)  
            self.blackjack.uservalue = total
            self.blackjack.usersum(total)
            self.print_mock.assert_any_call('Final hand: 33.')
            self.print_mock.assert_any_call('BUST.')

    
    def test_case_52_usersum_multiple_hits_to_21(self):
        self.blackjack.uservalue = 10
        self.input_mock.side_effect = ['y', 'y', 'n']
        self.rand_mock.side_effect = [5, 6]
        with patch.object(self.blackjack, 'value', side_effect=[5, 6]):
            self.blackjack.usersum(10)
            self.assertEqual(self.blackjack.uservalue, 21)
            self.print_mock.assert_any_call('Final hand: 21.')
            self.print_mock.assert_any_call('BLACKJACK!')

    
    def test_case_53_dealersum_dealer_hits_ace_and_busts(self):
        self.blackjack.dealervalue = 15
        self.rand_mock.return_value = 1  
        with patch.object(self.blackjack, 'value', return_value=11):
            self.blackjack.dealersum(15)
            self.assertEqual(self.blackjack.dealervalue, 26)
            expected_calls = [
                unittest.mock.call('Dealer has 15.'),
                unittest.mock.call('Drew an Ace'),
                unittest.mock.call('Final hand: 26.'),
                unittest.mock.call('BUST.')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)

    
    def test_case_54_usersum_user_stands_initially(self):
        self.blackjack.uservalue = 16
        self.input_mock.return_value = 'n'
        self.blackjack.usersum(16)
        self.print_mock.assert_called_with('Final hand: 16.')
        self.assertEqual(self.blackjack.uservalue, 16)

    
    def test_case_55_dealersum_dealer_hits_to_17_exactly(self):
        self.blackjack.dealervalue = 10
        self.rand_mock.return_value = 7  
        with patch.object(self.blackjack, 'value', return_value=7):
            self.blackjack.dealersum(10)
            expected_calls = [
                unittest.mock.call('Dealer has 10.'),
                unittest.mock.call('Drew a 7'),
                unittest.mock.call('Final hand: 17.')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_56_check_uppercase_y(self):
        result = self.blackjack.check('Y', 10)
        self.assertEqual(result, 'y')

    
    def test_case_57_check_uppercase_n(self):
        result = self.blackjack.check('N', 10)
        self.assertEqual(result, 'n')

    
    def test_case_58_check_empty_input_then_y(self):
        self.input_mock.side_effect = ['', 'y']
        result = self.blackjack.check('', 10)
        self.assertEqual(result, 'y')
        self.assertEqual(self.print_mock.call_count, 1)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_59_check_numeric_input_then_n(self):
        self.input_mock.side_effect = ['123', 'n']
        result = self.blackjack.check('123', 10)
        self.assertEqual(result, 'n')
        self.assertEqual(self.print_mock.call_count, 1)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_60_game_both_bust_dealer_wins(self):
        self.blackjack.uservalue = 22
        self.blackjack.dealervalue = 25
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Dealer wins!")

    
    def test_case_61_usersum_hit_with_ace_to_21(self):
        self.blackjack.uservalue = 10
        self.input_mock.return_value = 'y'
        self.rand_mock.return_value = 1  
        with patch.object(self.blackjack, 'value', return_value=11):
            self.blackjack.usersum(10)
            self.assertEqual(self.blackjack.uservalue, 21)
            self.print_mock.assert_any_call('Final hand: 21.')
            self.print_mock.assert_any_call('BLACKJACK!')

    
    def test_case_62_dealersum_multiple_hits_to_17(self):
        self.blackjack.dealervalue = 5
        self.rand_mock.side_effect = [6, 6]  
        with patch.object(self.blackjack, 'value', side_effect=[6, 6]):
            self.blackjack.dealersum(5)
            expected_calls = [
                unittest.mock.call('Dealer has 5.'),
                unittest.mock.call('Drew a 6'),
                unittest.mock.call('Dealer has 11.'),
                unittest.mock.call('Drew a 6'),
                unittest.mock.call('Final hand: 17.')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(self.blackjack.dealervalue, 17)

    
    def test_case_63_check_mixed_case_y(self):
        result = self.blackjack.check('YeS', 10)
        
        self.input_mock.return_value = 'y'
        self.assertEqual(result, 'y')
        self.assertEqual(self.print_mock.call_count, 1)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_64_check_mixed_case_n(self):
        result = self.blackjack.check('No', 10)
        
        self.input_mock.return_value = 'n'
        self.assertEqual(result, 'n')
        self.assertEqual(self.print_mock.call_count, 1)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_65_usersum_hit_multiple_aces_bust(self):
        self.blackjack.uservalue = 11  
        self.input_mock.side_effect = ['y', 'y']
        self.rand_mock.side_effect = [1, 1]  
        with patch.object(self.blackjack, 'value', return_value=11):
            self.blackjack.usersum(11)
            self.assertEqual(self.blackjack.uservalue, 33)
            expected_calls = [
                unittest.mock.call('Drew an Ace'),
                unittest.mock.call('Drew an Ace'),
                unittest.mock.call('Final hand: 33.'),
                unittest.mock.call('BUST.')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)

    
    def test_case_66_dealersum_hit_ace_exact_21(self):
        self.blackjack.dealervalue = 10
        self.rand_mock.return_value = 1  
        with patch.object(self.blackjack, 'value', return_value=11):
            self.blackjack.dealersum(10)
            expected_calls = [
                unittest.mock.call('Dealer has 10.'),
                unittest.mock.call('Drew an Ace'),
                unittest.mock.call('Final hand: 21.'),
                unittest.mock.call('BLACKJACK!')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(self.blackjack.dealervalue, 21)

    
    def test_case_67_check_repeated_invalid_inputs_then_y(self):
        self.input_mock.side_effect = ['?', 'invalid', 'y']
        result = self.blackjack.check('?', 10)
        self.assertEqual(result, 'y')
        self.assertEqual(self.print_mock.call_count, 2)
        self.print_mock.assert_called_with("Sorry I didn't get that.")

    
    def test_case_68_dealersum_multiple_aces_bust(self):
        self.blackjack.dealervalue = 10
        self.rand_mock.side_effect = [1, 1]  
        with patch.object(self.blackjack, 'value', return_value=11):
            self.blackjack.dealersum(10)
            expected_calls = [
                unittest.mock.call('Dealer has 10.'),
                unittest.mock.call('Drew an Ace'),
                unittest.mock.call('Dealer has 21.'),
                unittest.mock.call('BLACKJACK!')
            ]
            self.print_mock.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(self.blackjack.dealervalue, 21)

    
    def test_case_69_game_user_wins_with_higher_score(self):
        self.blackjack.uservalue = 19
        self.blackjack.dealervalue = 18
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("You win!")

    
    def test_case_70_game_dealer_wins_with_higher_score(self):
        self.blackjack.uservalue = 18
        self.blackjack.dealervalue = 19
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Dealer wins!")

    
    def test_case_71_game_push_both_blackjack(self):
        self.blackjack.uservalue = 21
        self.blackjack.dealervalue = 21
        self.blackjack.evaluate_game_result()
        self.print_mock.assert_called_with("Push.")

    
    def test_case_72_usersum_hit_non_ace_card(self):
        self.blackjack.uservalue = 10
        self.input_mock.return_value = 'y'
        self.rand_mock.return_value = 7
        with patch.object(self.blackjack, 'value', return_value=7):
            self.blackjack.usersum(10)
            self.assertEqual(self.blackjack.uservalue, 17)
            self.print_mock.assert_any_call('Final hand: 17.')

    
    def test_case_73_dealersum_stands_at_17_without_hitting(self):
        self.blackjack.dealervalue = 17
        self.blackjack.dealersum(17)
        self.print_mock.assert_called_with('Final hand: 17.')
        self.assertEqual
