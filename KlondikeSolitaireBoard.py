# KlondikeSolitaireBoard.py

import pygame
import traceback

from CardPile import CardPile, WastePile, TableauFaceDownPile, TableauFaceUpPile, StockPile, FoundationPile
from Location import Location
from Instructions import Instructions
import constants

class KlondikeSolitaireBoard:

    # the klondike solitaire board contains
    #   one stock pile                                            self.stock_pile
    #   one waste pile                                            self.waste_pile
    #   four foundation piles                                     self.foundations_piles
    #   seven sets of tableau columns each containing
    #       one face down pile                                    self.tableau_face_down_piles
    #       one face up pile                                      self.tableau_face_up_piles

    def __init__(self, game, card_deck):
        self.game = game
        self.card_deck = card_deck
        self.moves = []
        self._deal()
        self.game_instructions = Instructions(constants.KLONDIKE_INSTRUCTIONS)
        self._set_board_locations()
        self.game_won = False
        
        self.selected_pile = None
        self.selected_cards = None
        self.selected_location = None
        self.selected_rect = None
        self.current_location = None

        self.single_click_pile = None
        self.single_click_card = None
        self.single_click_ticks = 0
 
    def _deal(self):

        self.my_piles = []

        # create tableau face down and face up piles and deal cards into them.
        facedown_pile_lens = [0,1,2,3,4,5,6] 
        self.tableau_face_down_piles = []
        self.tableau_face_up_piles = []
        for i, pile_len in enumerate(facedown_pile_lens):
            tableau_facedown_pile = TableauFaceDownPile(f'Tableau FaceDown pile {i}')
            self.card_deck.deal(pile_len, tableau_facedown_pile)
            self.tableau_face_down_piles.append(tableau_facedown_pile)
            tableau_faceup_pile = TableauFaceUpPile(f'Tableau FaceUp pile {i}', tableau_facedown_pile)
            self.card_deck.deal(1, tableau_faceup_pile)
            self.tableau_face_up_piles.append(tableau_faceup_pile)
        self.my_piles.extend(self.tableau_face_down_piles)
        self.my_piles.extend(self.tableau_face_up_piles)

        # create stock pile and deal remainder of cards into it
        self.stock_pile = StockPile('Stock pile')
        self.card_deck.deal(len(self.card_deck), self.stock_pile)
        self.my_piles.append(self.stock_pile)
 
        # create an empty waste pile
        self.waste_pile = WastePile('Waste pile')
        self.my_piles.append(self.waste_pile)

        # create 4 empty foundation piles
        self.foundation_piles = []
        for i in range(4):
            foundation_pile = FoundationPile(f'Foundation Pile {i}')
            self.foundation_piles.append(foundation_pile)
        self.my_piles.extend(self.foundation_piles)

    # set locations for cards and instructions on board
    def _set_board_locations(self):
        self.stock_pile.location = Location(constants.CELL_WIDTH, constants.CELL_WIDTH)
        self.waste_pile.location = Location(constants.CELL_WIDTH*3, constants.CELL_WIDTH)
        for i, pile in enumerate(self.foundation_piles):
            pile.location = Location(constants.FRAME_MAX_X-constants.CELL_WIDTH*(i+1)*2, constants.CELL_WIDTH)
        for i, tableau_facedown_pile in enumerate(self.tableau_face_down_piles):
            tableau_facedown_pile.location = Location(round(constants.FRAME_MAX_X/8*(i+1),1), constants.CELL_WIDTH*4)
        for i, tableau_faceup_pile in enumerate(self.tableau_face_up_piles):
            tableau_faceup_pile.location = Location(round(constants.FRAME_MAX_X/8*(i+1),1), constants.CELL_WIDTH*4)

    def __str__(self):
        print_string = "KlondikeSolitaireBoard:"
        print_string = print_string + '\n  stock_pile:' + str(self.stock_pile)
        print_string = print_string + '\n  waste_pile:' + str(self.waste_pile)
        print_string = print_string + '\n  foundation piles:'
        for i, pile in enumerate(self.foundation_piles):
            print_string = print_string + f'\n    {i+1}: {pile}'
        for i, pile in enumerate(self.tableau_face_down_piles):
            print_string = print_string + f'\n    {i+1}: {pile}'
        for i, pile in enumerate(self.tableau_face_up_piles):
            print_string = print_string + f'\n    {i+1}: {pile}'
        return print_string

    def is_game_won(self):
        self.game_won = False
        self._try_to_finish_game()
        for foundation_pile in self.foundation_piles:
            if len(foundation_pile.cards) == 0 or foundation_pile.cards[-1].value.value != 13:
                return self.game_won
        self.game_won = True
        return self.game_won

    def _try_to_finish_game(self):
        # if stock_pile, waste_pile, and tableau face down piles are empty finish up game because it is over
        if len(self.stock_pile) != 0 or len(self.waste_pile) != 0 or len(max(self.tableau_face_down_piles, key=len)) != 0:
            return
        while len(max(self.tableau_face_up_piles, key=len)) != 0:
            from_pile = None
            low_card_value = 14
            for tableau_faceup_pile in self.tableau_face_up_piles:
                if len(tableau_faceup_pile) > 0:
                    if tableau_faceup_pile.cards[-1].value.value < low_card_value:
                        low_card_value = tableau_faceup_pile.cards[-1].value.value
                        from_pile = tableau_faceup_pile
            if from_pile is None:
                return
            from_pile.selected_card_index = len(from_pile.cards)-1
            card = from_pile.cards[from_pile.selected_card_index]
            for foundation_pile in self.foundation_piles:
                if foundation_pile.is_valid_move_to(from_pile, card):
                    self._move_cards(from_pile, foundation_pile, 1)
                    break
            self.draw(self.game.controller.screen)
            pygame.time.delay(150)

    def draw(self, screen):
        screen.fill(constants.GREEN)
        self.game_instructions.draw(screen)
        for pile in self.my_piles:
            if not pile == self.selected_pile or self.selected_cards is None or self.selected_rect is None:
                pile.draw(screen)
        # draw selected_pile last
        if not self.selected_pile is None and not self.selected_cards is None and not self.selected_rect is None:
            self.selected_pile.draw(screen, self.selected_cards[0], Location(self.selected_rect.left, self.selected_rect.top))
        pygame.display.flip()

    def undo(self):
        if len(self.moves) != 0:
            move_type, from_pile, to_pile, number_of_cards, waste_pile_cards_to_display = self.moves.pop()
            if move_type == 'move_cards':
                self._undo_move_cards(from_pile, to_pile, number_of_cards, waste_pile_cards_to_display)
            elif move_type == 'deal_cards':
                self._undo_deal_cards(from_pile, to_pile, number_of_cards, waste_pile_cards_to_display)

    def left_mouse_down(self, location):

        for pile in self.my_piles:
            selected, cards, my_rect = pile.selected(location)
            if selected:
                self.selected_pile = pile
                self.selected_cards = cards
                self.current_location = self.selected_location = location
                self.selected_rect = my_rect

    def left_mouse_motion(self, location):
        if not self.selected_pile is None and not self.selected_rect is None:
            self.selected_rect.move_ip(location.x - self.current_location.x, location.y - self.current_location.y)
            self.current_location = location

    def left_mouse_up(self, location):

        if not self.selected_pile is None:
            for pile in self.my_piles:
                selected, cards, my_rect = pile.selected(location)
                if selected:
                    if pile == self.selected_pile:
                        self.click(pile, cards)
                        break
                if not self.selected_rect is None and not self.selected_cards is None and len(self.selected_cards) > 0:
                    self.selected_rect.move_ip(location.x - self.current_location.x, location.y - self.current_location.y)
                    self.current_location = location
                    if pile.intercects(self.selected_rect):
                        if pile.is_valid_move_to(self.selected_pile, self.selected_cards[0]):
                            self._move_cards(self.selected_pile, pile, len(self.selected_cards))
                        break
        self.selected_pile = None
        self.selected_cards = None
        self.selected_location = None
        self.current_location = None
        self.selected_rect = None

    def click(self, pile, cards):
        if isinstance(pile, WastePile) or isinstance(pile, TableauFaceUpPile):
            if not cards is None and len(cards) == 1:
                card = cards[0]
                ticks = pygame.time.get_ticks()
                if not self.single_click_pile is None and self.single_click_pile == pile and self.single_click_card == card and ticks - self.single_click_ticks < 500:   # less than .5 seconds
                    self.double_click(pile, card)
                else:
                    self.single_click_pile = pile
                    self.single_click_card = card
                    self.single_click_ticks = ticks
                    return

        elif isinstance(pile, StockPile):
            if (len(self.stock_pile) != 0):
                cards_to_deal = min(3, len(self.stock_pile))
                self._deal_cards(self.stock_pile, self.waste_pile, cards_to_deal)
                self.waste_pile.cards_to_display = cards_to_deal
            else:
                self._deal_cards(self.waste_pile, self.stock_pile, len(self.waste_pile))

        self.single_click_pile = None
        self.single_click_card = None
        self.single_click_ticks = 0

    def double_click(self, pile, card):

        for foundation_pile in self.foundation_piles:
            if foundation_pile.is_valid_move_to(pile, card):
                self._move_cards(pile, foundation_pile, 1)
                break

        if len(self.waste_pile) > 0 and self.waste_pile.cards_to_display == 0:
            self.waste_pile.cards_to_display = 1


    def _move_cards(self, from_pile, to_pile, cards_to_move):
        to_pile.cards.extend(from_pile.cards[-cards_to_move:])
        from_pile.cards = from_pile.cards[:-cards_to_move]
        waste_pile_cards_to_display = 0
        if isinstance(from_pile, WastePile):
            waste_pile_cards_to_display = from_pile.cards_to_display
            from_pile.cards_to_display = from_pile.cards_to_display - 1
        move = ['move_cards', from_pile, to_pile, cards_to_move, waste_pile_cards_to_display]
        self.moves.append(move)
        if isinstance(from_pile, TableauFaceUpPile):
            if len(from_pile) == 0 and len(from_pile.my_face_down_pile) > 0:
                self._move_cards(from_pile.my_face_down_pile, from_pile, 1)
        if len(self.waste_pile) > 0 and self.waste_pile.cards_to_display == 0:
            self.waste_pile.cards_to_display = 1

    def _deal_cards(self, from_pile, to_pile, cards_to_deal):
        waste_pile_cards_to_display = 0
        if isinstance(from_pile, WastePile):
            waste_pile_cards_to_display = from_pile.cards_to_display
        elif isinstance(to_pile, WastePile):
            waste_pile_cards_to_display = to_pile.cards_to_display
        move = ['deal_cards', from_pile, to_pile, cards_to_deal, waste_pile_cards_to_display]
        self.moves.append(move)
        for i in range(cards_to_deal):
            to_pile.cards.append(from_pile.cards.pop())

    def _undo_move_cards(self, from_pile, to_pile, number_of_cards, waste_pile_cards_to_display):
        from_pile.cards.extend(to_pile.cards[-number_of_cards:])
        to_pile.cards = to_pile.cards[:-number_of_cards]
        if isinstance(from_pile, WastePile):
            from_pile.cards_to_display = waste_pile_cards_to_display
        if isinstance(from_pile, TableauFaceDownPile):
            self.undo()

    def _undo_deal_cards(self, from_pile, to_pile, number_of_cards, waste_pile_cards_to_display):
        for i in range(number_of_cards):
            from_pile.cards.append(to_pile.cards.pop())
        if isinstance(from_pile, WastePile):
            from_pile.cards_to_display = waste_pile_cards_to_display
        elif isinstance(to_pile, WastePile):
            to_pile.cards_to_display = waste_pile_cards_to_display
