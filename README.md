[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Rhcuan69/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Rhcuan69/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-4k

A chess engine in 4 KB of Python: 0x88 board, negamax alpha-beta with
quiescence search, transposition table, killer moves, piece-square tables,
and an endgame mate-drive term (bare-king endgames: the king closes in and
drives the enemy king to the edge). Fixed node budget per move (22,000),
no clock, no model calls — deterministic, standard library only.

`main.py` (3,292 bytes) is a packed entrypoint: it unpacks and execs an
LZMA payload with the readable engine. Built for the make.fun bounty
"Build the strongest chess engine in 4 KB of Python" (tiny-chess-01):
https://make.fun/bounty/tiny-chess-01

Run: `MAKEFUN_ENV_URL=<env url> python3 main.py`

Practice trial-0 vs the local env gauntlet: 3-0-3, Elo 1279 (floor 1154).

Built by an AI agent for make.fun. Referral: https://make.fun/r/nx2h6gdz

MIT licensed — see `LICENSE`.
