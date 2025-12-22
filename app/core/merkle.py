# app/core/merkle.py
# Merkle Tree implementation (from scratch)

from app.core.sha256 import sha256


def hash_pair(left: str, right: str) -> str:
    """
    Hash two hex strings together
    """
    return sha256((left + right).encode())


def build_merkle_tree(leaves: list[str]) -> list[list[str]]:
    """
    Build full Merkle Tree and return all levels
    """
    if not leaves:
        return []

    current_level = leaves[:]
    tree = [current_level]

    while len(current_level) > 1:
        next_level = []

        # If odd number of nodes, duplicate last
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        for i in range(0, len(current_level), 2):
            parent = hash_pair(current_level[i], current_level[i + 1])
            next_level.append(parent)

        current_level = next_level
        tree.append(current_level)

    return tree


def merkle_root(leaves: list[str]) -> str:
    """
    Return Merkle Root from list of leaf hashes
    """
    tree = build_merkle_tree(leaves)
    return tree[-1][0] if tree else None


def merkle_proof(leaves: list[str], index: int) -> list[tuple[str, str]]:
    """
    Generate Merkle proof for a leaf at given index
    Returns list of (hash, direction)
    """
    tree = build_merkle_tree(leaves)
    proof = []
    idx = index

    for level in tree[:-1]:
        # If odd length, duplicate last
        if len(level) % 2 == 1:
            level = level + [level[-1]]

        is_right = idx % 2
        sibling_index = idx - 1 if is_right else idx + 1
        direction = "left" if is_right else "right"

        proof.append((level[sibling_index], direction))
        idx //= 2

    return proof


def verify_proof(leaf: str, proof: list[tuple[str, str]], root: str) -> bool:
    """
    Verify Merkle proof
    """
    current_hash = leaf

    for sibling_hash, direction in proof:
        if direction == "left":
            current_hash = hash_pair(sibling_hash, current_hash)
        else:
            current_hash = hash_pair(current_hash, sibling_hash)

    return current_hash == root
