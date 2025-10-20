def get_bavg_score(likes: int, dislikes:int,
                   prior_likes: int = 5, prior_dislikes: int = 5) -> float:
    total_likes = likes + prior_likes
    total_votes = likes + dislikes + prior_likes + prior_dislikes

    if total_votes == 0:
        return 0.5
    
    return round(total_likes / total_votes, 3) * 10