"""
queries.py
==========
CIS 3120 · MP02 — SQL and Database
Author 2 module — all query functions
"""

def get_playlist_tracks(conn, playlist_name):
    """Return all tracks on the named playlist."""
    query = """
        SELECT t.title,
               a.name AS artist_name,
               t.duration_seconds,
               pt.position
        FROM PlaylistTrack pt
        JOIN Track t ON pt.track_id = t.track_id
        JOIN Artist a ON t.artist_id = a.artist_id
        JOIN Playlist p ON pt.playlist_id = p.playlist_id
        WHERE p.playlist_name = ?
        ORDER BY pt.position ASC
    """
    return conn.execute(query, (playlist_name,)).fetchall()


def get_tracks_on_no_playlist(conn):
    """Return tracks not in any playlist."""
    query = """
        SELECT t.title,
               a.name AS artist_name
        FROM Track t
        LEFT JOIN PlaylistTrack pt ON t.track_id = pt.track_id
        JOIN Artist a ON t.artist_id = a.artist_id
        WHERE pt.track_id IS NULL
    """
    return conn.execute(query).fetchall()


def get_most_added_track(conn):
    """Return most frequently added track."""
    query = """
        SELECT t.title,
               a.name AS artist_name,
               COUNT(*) AS count
        FROM PlaylistTrack pt
        JOIN Track t ON pt.track_id = t.track_id
        JOIN Artist a ON t.artist_id = a.artist_id
        GROUP BY t.track_id
        ORDER BY count DESC
        LIMIT 1
    """
    return conn.execute(query).fetchone()


def get_playlist_durations(conn):
    """Return playlist durations in minutes."""
    query = """
        SELECT p.playlist_name,
               SUM(t.duration_seconds) / 60.0 AS total_minutes
        FROM PlaylistTrack pt
        JOIN Track t ON pt.track_id = t.track_id
        JOIN Playlist p ON pt.playlist_id = p.playlist_id
        GROUP BY p.playlist_id
        ORDER BY total_minutes DESC
    """
    return conn.execute(query).fetchall()
