import galois
import numpy as np
import secrets


P = 2**61 - 1 # Modulo prime number
GF_P = galois.GF(P) # Finite field

def split_shares(d: int, k: int, n: int) -> list[tuple[int, int]]:
    poly = _gen_polynomial(d, k)
    shares = [None] * n
    for i in range(1, n + 1):
        shares[i - 1] = (i, _eval_polynomial(poly, i))
    return shares

def _gen_polynomial(d: int, k: int) -> list[int]:
    poly = [0] * k
    if k > 0:
        poly[0] = d % P
    for i in range(1, k):
        poly[i] = secrets.randbelow(P)
    return poly

def _eval_polynomial(poly: list[int], i: int) -> int:
    share = 0
    for deg, coeff in enumerate(poly):
        share = (share + coeff * i ** deg) % P
    return share

def join_shares(shares: list[tuple[int, int]]) -> int:
    coeff_matrix = []
    target_vec = []
    k = len(shares)
    for share in shares:
        row = [0] * k
        row[0] = 1
        for i in range(1, k):
            row[i] = share[0] ** i
        coeff_matrix.append(row)
        target_vec.append(share[1])
    
    a = GF_P(coeff_matrix)
    b = GF_P(target_vec)
    solution = np.linalg.solve(a, b)
    return int(solution[0])
