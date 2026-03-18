from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a numeric score and reasons for a song based on user preferences."""
    score = 0.0
    reasons = []
    # Genre match (weight halved)
    if song.get('genre') == user_prefs.get('favorite_genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")
    # Mood match
    if song.get('mood') == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
    # Energy match (within 0.2, weight doubled)
    if abs(song.get('energy', 0) - user_prefs.get('target_energy', 0)) <= 0.2:
        score += 2.0
        reasons.append("energy close (+2.0)")
    # Danceability match (within 0.2)
    if abs(song.get('danceability', 0) - user_prefs.get('target_danceability', 0)) <= 0.2:
        score += 1.0
        reasons.append("danceability close (+1.0)")
    # Tempo match (within ±10 BPM)
    if abs(song.get('tempo_bpm', 0) - user_prefs.get('target_tempo', 0)) <= 10:
        score += 1.0
        reasons.append("tempo close (+1.0)")
    return score, reasons
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numerical fields."""
    import csv
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numerical fields
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs using score_song and return the top k recommendations."""
    # Ensure user_prefs keys match those used in score_song
    # If user_prefs uses 'genre', 'mood', 'energy', map to expected keys
    prefs = {
        'favorite_genre': user_prefs.get('genre'),
        'favorite_mood': user_prefs.get('mood'),
        'target_energy': user_prefs.get('energy'),
        'target_danceability': user_prefs.get('danceability', 0.5),
        'target_tempo': user_prefs.get('tempo_bpm', 120)
    }
    results = []
    for song in songs:
        score, reasons = score_song(prefs, song)
        explanation = "; ".join(reasons)
        results.append((song, score, explanation))
    top_k = sorted(results, key=lambda x: x[1], reverse=True)[:k]
    return top_k
