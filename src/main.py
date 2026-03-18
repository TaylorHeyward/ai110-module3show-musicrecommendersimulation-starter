"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        {"genre": "pop", "mood": "happy", "energy": 0.9, "danceability": 0.8, "tempo_bpm": 130},  # High-Energy Pop
        {"genre": "lofi", "mood": "chill", "energy": 0.3, "danceability": 0.4, "tempo_bpm": 80},   # Chill Lofi
        {"genre": "rock", "mood": "intense", "energy": 0.8, "danceability": 0.6, "tempo_bpm": 140}, # Deep Intense Rock
    ]

    profile_names = ["High-Energy Pop", "Chill Lofi", "Deep Intense Rock"]

    for name, user_prefs in zip(profile_names, profiles):
        print(f"\nTop recommendations for {name} profile:\n")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
