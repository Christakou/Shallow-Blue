import numpy as np
import pygame
import math
import random
from utils import KEYDICT, SCREENSIZE, coordinates_to_board_position
from board import Board
import concurrent.futures


class GameManager():
    def __init__(self):
        self.main_board = Board()
        self.main_board.initialize()
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self._load_images()
        self.suggested_moves = []
        self.done = False
        self.any_selected = []

    def _load_images(self):
        self.board_sprite = pygame.image.load("./assets/chessboard.png")
        self.board_sprite = pygame.transform.scale(self.board_sprite, SCREENSIZE)
        self.selected_sprite = pygame.image.load("./assets/Selected.png")
        self.legal_move_sprite = pygame.image.load("./assets/LegalMove.png")

    def _blit_board(self):
        self.screen.blit(self.board_sprite, (0, 0))

    def _blit_pieces(self):
        self.suggested_moves = []
        for piece in self.main_board.all_pieces():
            piece.coord = coordinates_to_board_position(piece.position)
            self.screen.blit(pygame.image.load('./assets/' + piece.image_path), piece.coord)
            if piece.selected:
                self.screen.blit(self.selected_sprite, piece.coord)
                if piece.moves() is not None:
                    for a in piece.moves():
                        self.suggested_moves.append(a)

    def _blit_suggested_moves(self):
        for move in self.suggested_moves:
            self.screen.blit(self.legal_move_sprite, (move[0] * (SCREENSIZE[0] / 8.0), move[1] * (SCREENSIZE[1] / 8.0)))

    def _event_quit_handler(self, event):
        self.done = True

    def _event_mousebuttondown_handler(self, event):
        selected_pos = [int(math.floor((event.pos[0] * 8.0 / SCREENSIZE[0]))),
                        int(math.floor(event.pos[1] * 8.0 / SCREENSIZE[1]))]
        for p in self.main_board.all_pieces():
            if p.selected is True:
                self.any_selected.append(True)

            else:
                self.any_selected.append(False)

            if any(self.any_selected):
                if p.selected is True:
                    if tuple(p.position) == tuple(selected_pos):
                        p.selected = False
                    elif p.position != selected_pos:
                        if self.main_board.is_occupied(selected_pos) and p.can_take(selected_pos):
                            taken = tuple(selected_pos)
                            takes = p
                            self.any_selected = []
                            p.selected = False
                        else:
                            print("Score is " + str(self.main_board.get_score()))
                            p.move_to(selected_pos)
                            p.selected = False
                            self.any_selected = []
            else:
                if tuple(p.position) == tuple(selected_pos):
                    if self.main_board.move_count % 2 == 0 and p.color == "W":
                        p.selected = True

        try:
            takes.take(taken)
        except Exception as err:
            print(err)


    def update_board(self):
            self._blit_board()
            self._blit_pieces()
            self._blit_suggested_moves()


    def event_loop(self):
        takes = [0]
        taken = [0]
        any_selected = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._event_quit_handler(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._event_mousebuttondown_handler(event)
                self.update_board()
        if self.main_board.move_count % 2 == 1:
            Calculate(self.main_board)
        pygame.display.flip()

GM = GameManager()
GM.update_board()

def get_board_parent_at_depth(board, depth):
    if board.depth == depth:
        print(f'reached board at depth: {depth}')
        return board
    if board.parent is None:
        return board
    get_board_parent_at_depth(board.parent, depth-1)

def minimax(position, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return position.get_score()
    if maximizing_player:
        maxEval = -np.Inf
        for child_board in position.children:
            eval = minimax(child_board, depth -1, alpha, beta, False)
            maxEval = max(maxEval,eval)
            print(f'{maxEval=} {eval=} {depth=}')
            alpha = max(alpha, eval)
            if beta <= alpha:
               break
        print(f'{maxEval=}')
        return maxEval
    else:
        minEval = np.inf
        for child_board in position.children:
            eval = minimax(child_board, depth-1, alpha, beta, True)
            minEval = min(minEval, eval)
            print(f'{minEval=} {eval=} {depth=}')
            beta = min(beta, eval)
            print(f'{alpha=} {beta=}')
            if beta <= alpha:
               break
        print(f'{minEval=}')
        return minEval


def Calculate(main_board, depth=4):
    print('Calculating')
    print(f'board:move_count:{main_board.move_count}')
    main_board.children = []
    next_boards = [main_board] # TODO: Change order so we're iterating first on boards, then pieces and finally depth
                            # this way we can use minmax to prune on board generation as well
    for i in range(0,depth):
        if i==3:
            print('hey')
        relevant_board = [board for board in next_boards if board.depth == i]
        for board in relevant_board:
            print(f'Generating position tree at depth = {i}')
            if i % 2 == 0:
                for piece in board.blackPieces[:5]:
                    move_list = piece.moves()
                    random.shuffle(move_list)
                    with  concurrent.futures.ProcessPoolExecutor() as executor:
                        def create_board(mv):
                            fake_board = Board()
                            fake_board.copy_state(board)
                            fake_board.occupier(piece.position).move_to(mv)
                            next_boards.append(fake_board)
                        for mv in move_list[:2]:
                            executor.submit(create_board(mv))

            elif i % 2 == 1:
                for piece in board.whitePieces[:5]:
                    move_list = piece.moves()
                    random.shuffle(move_list)
                    with  concurrent.futures.ProcessPoolExecutor() as executor:
                        def create_board(mv):
                            fake_board = Board()
                            fake_board.copy_state(board)
                            fake_board.occupier(piece.position).move_to(mv)
                            next_boards.append(fake_board)

                        for mv in move_list[:2]:
                            executor.submit(create_board(mv))

    best_board = sorted(GM.main_board.children, key=lambda board:minimax(board, 3, -np.inf, np.inf, True))[0]
    print(best_board)
    print(minimax(best_board, 2, -np.inf, np.inf, False))

    GM.main_board.occupier(best_board.last_move[0]).move_to(best_board.last_move[1])
    print('moved?')
    GM.update_board()
while not GM.done:
    GM.event_loop()