def get_smarts(group: str, positions: list[int]) -> str:
    """
    Get SMARTS strings for substitued 1,4-hydroquinones.

    Parameters:
    group : str
        Valid SMARTS string for substituent
    positions : list[int]
        Position(s) of substituents on ring

    Returns:
        SMARTS string of substituted 1,4-hydroquinone
    """
    match positions:
        case [2]:  # 2-sub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4][c:5](-[OH:8])[c:6][c:7]1'
        case [2, 3]:  # 2,3-disub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4](-{group})[c:5](-[OH:8])[c:6][c:7]1'
        case [2, 5]:  # 2,5-disub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4][c:5](-[OH:8])[c:6](-{group})[c:7]1'
        case [2, 6]:  # 2,6-disub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4][c:5](-[OH:8])[c:6][c:7]1-{group}'
        case [2, 3, 5]:  # trisub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4](-{group})[c:5](-[OH:8])[c:6][c:7]1-{group}'
        case [2, 3, 5, 6]:  # tetrasub
            return f'[OH:1]-[c:2]1[c:3](-{group})[c:4](-{group})[c:5](-[OH:8])[c:6](-{group})[c:7]1-{group}'
        case _:
            raise ValueError('Invalid positions')