from fastapi import APIRouter, HTTPException
from sqlmodel import select

from backend.database import SessionDep
from backend.models import Movie, MovieList, Suggestion
from backend.suggestion_data import SUGGESTIONS

router = APIRouter(tags=["suggestions"])


# gives back movies from the suggestion pool that AREN'T already in this list,
# so the Discover page never shows you something you already added.
# ?genre=Horror is optional if you only want one genre.
@router.get("/lists/{list_id}/suggestions", response_model=list[Suggestion])
def get_suggestions(list_id: int, session: SessionDep, genre: str | None = None):
    if not session.get(MovieList, list_id):
        raise HTTPException(status_code=404, detail="List not found")

    in_list = session.exec(select(Movie).where(Movie.list_id == list_id)).all()
    # lowercase so "inception" and "Inception" count as the same movie
    already_added = {movie.title.lower() for movie in in_list}

    results = []
    for s in SUGGESTIONS:
        if s["title"].lower() in already_added:
            continue
        if genre and s["genre"].lower() != genre.lower():
            continue
        results.append(s)
    return results


# list of genres, used for the genre filter dropdown later
@router.get("/genres", response_model=list[str])
def get_genres():
    return sorted({s["genre"] for s in SUGGESTIONS})
