from typing import List, Optional, Set, Tuple

Grid = List[List[int]]

def solve_6x6_sudoku(board: Grid, box_r: int = 2, box_c: int = 3) -> Optional[Grid]:
    N = 6
    DIGITS = set(range(1, N + 1))

    # Basic validation
    if len(board) != N or any(len(row) != N for row in board):
        raise ValueError("Board must be 6x6.")
    if box_r * box_c != N:
        raise ValueError("For a 6x6 Sudoku, box_r * box_c must equal 6 (e.g., 2x3 or 3x2).")

    # Precompute peers for each cell (same row, col, or box)
    peers = {}
    for r in range(N):
        for c in range(N):
            ps = set()
            ps.update({(r, cc) for cc in range(N) if cc != c})
            ps.update({(rr, c) for rr in range(N) if rr != r})

            br = (r // box_r) * box_r
            bc = (c // box_c) * box_c
            ps.update({
                (rr, cc)
                for rr in range(br, br + box_r)
                for cc in range(bc, bc + box_c)
                if (rr, cc) != (r, c)
            })
            peers[(r, c)] = ps

    def candidates(b: Grid, r: int, c: int) -> Set[int]:
        used = {b[rr][cc] for (rr, cc) in peers[(r, c)] if b[rr][cc] != 0}
        return DIGITS - used

    def propagate_naked_singles(b: Grid) -> bool:
        changed = True
        while changed:
            changed = False
            for r in range(N):
                for c in range(N):
                    if b[r][c] == 0:
                        cand = candidates(b, r, c)
                        if not cand:
                            return False
                        if len(cand) == 1:
                            b[r][c] = next(iter(cand))
                            changed = True
        return True

    def find_mrv_cell(b: Grid) -> Optional[Tuple[int, int, Set[int]]]:
        
        best = None
        best_cand = None
        for r in range(N):
            for c in range(N):
                if b[r][c] == 0:
                    cand = candidates(b, r, c)
                    if not cand:
                        return None
                    if best is None or len(cand) < len(best_cand):
                        best = (r, c)
                        best_cand = cand
                        if len(best_cand) == 1:
                            return (r, c, best_cand)
        if best is None:
            return None
        return (best[0], best[1], best_cand)

    def backtrack(b: Grid) -> Optional[Grid]:
        if not propagate_naked_singles(b):
            return None

      
        if all(b[r][c] != 0 for r in range(N) for c in range(N)):
            return b

        mrv = find_mrv_cell(b)
        if mrv is None:
            return None

        r, c, cand = mrv
        for v in sorted(cand):
            b2 = [row[:] for row in b]
            b2[r][c] = v
            sol = backtrack(b2)
            if sol is not None:
                return sol
        return None

    start = [row[:] for row in board]
    return backtrack(start)

board = [
  [0, 0, 0, 0, 6, 0],
  [0, 0, 0, 4, 0, 0],
  [0, 5, 0, 0, 0, 2],
  [0, 0, 2, 0, 0, 0],
  [0, 0, 6, 0, 0, 0],
  [3, 0, 0, 0, 0, 0],
]

sol = solve_6x6_sudoku(board, box_r=2, box_c=3)
print(sol)

