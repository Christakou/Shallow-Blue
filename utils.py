KEYDICT = {"ki": "King", "kn": "Knight", "r": "Rook", "q": "Queen", "b": "Bishop", "p": "Pawn"}
SCREENSIZE = (600, 600)

def coordinates_to_board_position(position):
	return [position[0] * (SCREENSIZE[0] / 8.0), position[1] * (SCREENSIZE[1] / 8.0)]


def in_board(coords):
    if coords[0] >= 0 and coords[0] <8:
        if coords[1] >= 0 and coords[1] < 8:
            return True
    else:
        return False