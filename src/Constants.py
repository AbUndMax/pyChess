
FILE_SIZE: int = 8
"""Board size in squares, x (= horizontal = files) direction"""

RANK_SIZE: int = 8
"""Board size in squares, y (= vertical = ranks) direction"""

SQUARE_PX: int = 80

BOARD_FILE_PX: int = FILE_SIZE * SQUARE_PX

BOARD_RANK_PX: int = RANK_SIZE * SQUARE_PX

BOARD_GEOMETRY: str = f"{int(BOARD_FILE_PX * 1.03)}x{int(BOARD_RANK_PX * 1.03)}"

IMG_PATHS = {
    "bB": "resources/pixl_pieces/bB.png",
    "bK": "resources/pixl_pieces/bK.png",
    "bN": "resources/pixl_pieces/bN.png",
    "bP": "resources/pixl_pieces/bP.png",
    "bQ": "resources/pixl_pieces/bQ.png",
    "bR": "resources/pixl_pieces/bR.png",
    "wB": "resources/pixl_pieces/wB.png",
    "wK": "resources/pixl_pieces/wK.png",
    "wN": "resources/pixl_pieces/wN.png",
    "wP": "resources/pixl_pieces/wP.png",
    "wQ": "resources/pixl_pieces/wQ.png",
    "wR": "resources/pixl_pieces/wR.png"
}