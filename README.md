# tiny-chess-4k

A chess engine in 4 KB of Python: 0x88 board, negamax alpha-beta with
quiescence search, transposition table, killer moves, piece-square tables,
and an endgame mate-drive term (bare-king endgames: the king closes in and
drives the enemy king to the edge). Fixed node budget per move (22,000),
no clock, no model calls — deterministic, standard library only.

`main.py` (4,069 bytes) is a packed entrypoint: it unpacks and execs an
LZMA payload with the readable engine. Built for the make.fun bounty
"Build the strongest chess engine in 4 KB of Python" (tiny-chess-01).

Practice trial-0 vs the local env gauntlet: 3-0-3, Elo 1279 (floor 1154).

MIT licensed — see `LICENSE`.
