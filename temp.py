from app import app, db, Songs, Albums

# Add audio then run this to insert this into the first album.

with app.app_context():
    album = Albums.query.get(2)

    songs = [
        Songs(songName="SKINNY", year=2024, album=album, audio="../static/audio/album1/skinny.mp3"),
        Songs(songName="LUNCH", year=2024, album=album, audio="../static/audio/album1/lunch.mp3"),
        Songs(songName="CHIHIRO", year=2024, album=album, audio="../static/audio/album1/chihiro.mp3"),
        Songs(songName="BIRDS OF A FEATHER", year=2024, album=album, audio="../static/audio/album1/boaf.mp3"),
        Songs(songName="WILDFLOWER", year=2024, album=album, audio="../static/audio/album1/wildflower.mp3"),
        Songs(songName="THE GREATEST", year=2024, album=album, audio="../static/audio/album1/thegreatest.mp3"),
        Songs(songName="L'AMOUR DE MA VIE", year=2024, album=album, audio="../static/audio/album1/l'amour.mp3"),
        Songs(songName="THE DINER", year=2024, album=album, audio="../static/audio/album1/thediner.mp3"),
        Songs(songName="BITTERSUITE", year=2024, album=album, audio="../static/audio/album1/bittersuite.mp3"),
        Songs(songName="BLUE", year=2024, album=album, audio="../static/audio/album1/blue.mp3")
    ]

    db.session.add_all(songs)
    db.session.commit()

    print("✅ Songs added successfully!")