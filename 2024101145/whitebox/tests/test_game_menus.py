import pytest
from unittest.mock import patch, MagicMock
from moneypoly.game import Game
from moneypoly.player import Player

@patch("moneypoly.ui.print_banner")
@patch("builtins.print")
def test_game_run_loop(mock_print, mock_banner):
    g = Game(["Alice", "Bob"])
    g.play_turn = MagicMock()
    def mock_play():
        g.turn_number += 1
    g.play_turn.side_effect = mock_play
    g.turn_number = 99
    # Should stop after 100 turns
    g.run()
    assert mock_banner.called

@patch("moneypoly.ui.print_banner")
@patch("builtins.print")
def test_game_run_loop_winner(mock_print, mock_banner):
    g = Game(["Alice"])
    # 1 player left immediately breaks and wins
    g.run()
    assert mock_banner.called

@patch("moneypoly.ui.safe_int_input")
@patch("builtins.print")
def test_interactive_menu(mock_print, mock_input):
    g = Game(["Alice", "Bob"])
    p = g.players[0]
    
    # sequence of choices: 1 (standings), 2 (board ownership), 6 (loan), 0 (roll)
    mock_input.side_effect = [1, 2, 6, 500, 0]
    g.interactive_menu(p)
    assert p.balance == 2000

@patch("moneypoly.ui.safe_int_input")
@patch("builtins.print")
def test_menu_mortgage_unmortgage(mock_print, mock_input):
    g = Game(["Alice"])
    p = g.players[0]
    prop = g.board.get_property_at(1)
    
    p.add_property(prop)
    prop.owner = p
    
    # Mortgage menu: choose 1
    mock_input.side_effect = [1]
    g._menu_mortgage(p)
    assert prop.is_mortgaged is True
    
    # Unmortgage menu: choose 1
    mock_input.side_effect = [1]
    g._menu_unmortgage(p)
    assert prop.is_mortgaged is False
    
    # Mortgage empty
    g._menu_mortgage(Player("Empty"))
    
    # Unmortgage empty
    g._menu_unmortgage(Player("Empty"))

@patch("moneypoly.ui.safe_int_input")
@patch("builtins.print")
def test_menu_trade(mock_print, mock_input):
    g = Game(["Alice", "Bob"])
    p = g.players[0]
    prop = g.board.get_property_at(1)
    p.add_property(prop)
    prop.owner = p
    
    # choose Bob (1), choose property (1), cash (100)
    mock_input.side_effect = [1, 1, 100]
    g._menu_trade(p)
    
    assert prop.owner == g.players[1]

def test_cards_coverage(monkeypatch):
    g = Game(["Alice", "Bob"])
    p = g.players[0]
    
    # Apply move_to
    card = {"action": "move_to", "value": 15, "description": "Reading RR"}
    g.board.get_property_at(15).owner = g.players[1]
    g.pay_rent = MagicMock()
    g._apply_card(p, card)
    assert p.position == 15
    g.pay_rent.assert_called_once()
    
    # Birthday
    card = {"action": "birthday", "value": 10, "description": "Birthday"}
    g._apply_card(p, card)
    assert p.balance > 1500
    
    # Collect from all
    card = {"action": "collect_from_all", "value": 50, "description": "Opera seats"}
    g._apply_card(p, card)
    assert p.balance > 1500
