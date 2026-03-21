import pytest
from moneypoly.cards import CardDeck, CHANCE_CARDS

def test_carddeck_initialization():
    deck = CardDeck([{"id": 1}, {"id": 2}])
    assert len(deck) == 2
    assert deck.cards_remaining() == 2

def test_carddeck_draw():
    deck = CardDeck([{"id": 1}, {"id": 2}])
    
    c1 = deck.draw()
    assert c1["id"] == 1
    assert deck.cards_remaining() == 1
    
    c2 = deck.draw()
    assert c2["id"] == 2
    assert deck.cards_remaining() == 2 # Cycles back to 2
    
    c3 = deck.draw()
    assert c3["id"] == 1
    
    empty_deck = CardDeck([])
    assert empty_deck.draw() is None

def test_carddeck_peek():
    deck = CardDeck([{"id": 1}, {"id": 2}])
    
    assert deck.peek()["id"] == 1
    assert deck.peek()["id"] == 1 # Does not advance
    deck.draw()
    assert deck.peek()["id"] == 2
    
    empty_deck = CardDeck([])
    assert empty_deck.peek() is None

def test_carddeck_reshuffle():
    deck = CardDeck(CHANCE_CARDS)
    orig = list(deck.cards)
    deck.draw()
    deck.reshuffle()
    
    assert deck.cards_remaining() == len(CHANCE_CARDS)
    # The order will likely change on shuffle
    # We can't guarantee random.shuffle changes order so we just test it resets the index
    assert deck.index == 0

def test_carddeck_repr():
    deck = CardDeck([{"id": 1}])
    assert repr(deck) == "CardDeck(1 cards, next=0)"
