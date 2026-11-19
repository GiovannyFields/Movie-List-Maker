# the pool of movies the Discover page pulls from.
# it's just a python list, not a db table, since nobody edits it from the app.
# to add more, copy a line and change it.

SUGGESTIONS = [
    # Horror
    {"title": "Get Out", "year": 2017, "genre": "Horror", "overview": "A weekend visit to meet his girlfriend's parents gets stranger by the hour."},
    {"title": "Hereditary", "year": 2018, "genre": "Horror", "overview": "After a family loss, something in the house starts coming apart."},
    {"title": "The Conjuring", "year": 2013, "genre": "Horror", "overview": "Two paranormal investigators help a family whose farmhouse won't leave them alone."},
    {"title": "A Quiet Place", "year": 2018, "genre": "Horror", "overview": "A family survives by staying silent, because the things outside hunt by sound."},
    {"title": "It Follows", "year": 2014, "genre": "Horror", "overview": "Something slow and relentless is following her, and only she can see it."},
    {"title": "The Shining", "year": 1980, "genre": "Horror", "overview": "A winter caretaker job at an empty hotel goes very wrong."},
    # Comedy
    {"title": "Superbad", "year": 2007, "genre": "Comedy", "overview": "Two best friends try to make one last high school party count."},
    {"title": "The Grand Budapest Hotel", "year": 2014, "genre": "Comedy", "overview": "A hotel concierge and his lobby boy get caught up in a stolen painting caper."},
    {"title": "Step Brothers", "year": 2008, "genre": "Comedy", "overview": "Two grown men who still live at home become stepbrothers and hate it."},
    {"title": "Booksmart", "year": 2019, "genre": "Comedy", "overview": "Two straight-A students try to cram four years of fun into one night."},
    {"title": "Hot Fuzz", "year": 2007, "genre": "Comedy", "overview": "A big-city cop gets sent to a sleepy village that's hiding something."},
    # Action
    {"title": "Mad Max: Fury Road", "year": 2015, "genre": "Action", "overview": "A nonstop chase across the desert in a world that ran out of everything."},
    {"title": "John Wick", "year": 2014, "genre": "Action", "overview": "A retired hitman comes back after some guys make a very bad mistake."},
    {"title": "The Dark Knight", "year": 2008, "genre": "Action", "overview": "Batman goes up against the Joker, who just wants to watch Gotham burn."},
    {"title": "Top Gun: Maverick", "year": 2022, "genre": "Action", "overview": "A veteran pilot trains a new class for a mission that seems impossible."},
    {"title": "Mission: Impossible - Fallout", "year": 2018, "genre": "Action", "overview": "Ethan Hunt races to stop a disaster after a mission goes sideways."},
    # Sci-Fi
    {"title": "Interstellar", "year": 2014, "genre": "Sci-Fi", "overview": "Astronauts travel through a wormhole looking for a new home for humanity."},
    {"title": "The Matrix", "year": 1999, "genre": "Sci-Fi", "overview": "A hacker finds out the world he knows isn't real."},
    {"title": "Arrival", "year": 2016, "genre": "Sci-Fi", "overview": "A linguist tries to talk to aliens before the world panics."},
    {"title": "Inception", "year": 2010, "genre": "Sci-Fi", "overview": "A thief who steals secrets from dreams takes on one last job."},
    {"title": "Dune", "year": 2021, "genre": "Sci-Fi", "overview": "A young heir is thrown into a fight over the most valuable planet in the galaxy."},
    {"title": "Ex Machina", "year": 2014, "genre": "Sci-Fi", "overview": "A programmer is invited to test whether a robot can really think."},
    # Drama
    {"title": "Parasite", "year": 2019, "genre": "Drama", "overview": "A poor family slowly works its way into a rich family's life."},
    {"title": "Whiplash", "year": 2014, "genre": "Drama", "overview": "A young drummer and a brutal teacher push each other to the edge."},
    {"title": "The Shawshank Redemption", "year": 1994, "genre": "Drama", "overview": "A banker sent to prison for life holds onto hope for decades."},
    {"title": "Moonlight", "year": 2016, "genre": "Drama", "overview": "Three chapters in one man's life, growing up in Miami."},
    {"title": "Good Will Hunting", "year": 1997, "genre": "Drama", "overview": "A janitor with a genius for math has to figure out what he actually wants."},
    # Animation
    {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "genre": "Animation", "overview": "Miles Morales becomes Spider-Man and meets other Spider-people from other worlds."},
    {"title": "Spirited Away", "year": 2001, "genre": "Animation", "overview": "A girl gets stuck in a spirit world and has to work to free her parents."},
    {"title": "Coco", "year": 2017, "genre": "Animation", "overview": "A kid who loves music ends up in the Land of the Dead."},
    {"title": "Up", "year": 2009, "genre": "Animation", "overview": "An old man ties balloons to his house and flies off, with a stowaway."},
    {"title": "Ratatouille", "year": 2007, "genre": "Animation", "overview": "A rat who wants to be a chef teams up with a clumsy kitchen worker."},
    # Thriller
    {"title": "Gone Girl", "year": 2014, "genre": "Thriller", "overview": "A woman goes missing and everyone starts looking at her husband."},
    {"title": "Prisoners", "year": 2013, "genre": "Thriller", "overview": "A father takes things into his own hands when his daughter disappears."},
    {"title": "Knives Out", "year": 2019, "genre": "Thriller", "overview": "A detective investigates a rich author's death and his very suspicious family."},
    {"title": "Se7en", "year": 1995, "genre": "Thriller", "overview": "Two detectives hunt a killer whose crimes follow a disturbing pattern."},
    # Romance
    {"title": "La La Land", "year": 2016, "genre": "Romance", "overview": "A jazz pianist and an actress fall in love while chasing their dreams in LA."},
    {"title": "Pride & Prejudice", "year": 2005, "genre": "Romance", "overview": "Elizabeth Bennet and Mr. Darcy can't stand each other, at first."},
    {"title": "About Time", "year": 2013, "genre": "Romance", "overview": "A guy who can time travel uses it to try to get his love life right."},
    {"title": "Crazy Rich Asians", "year": 2018, "genre": "Romance", "overview": "She finds out her boyfriend's family is extremely rich, and not thrilled about her."},
]
