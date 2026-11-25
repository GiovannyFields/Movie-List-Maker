from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from backend.database import SessionDep
from backend.models import Movie, MovieCreate, MovieList, MovieRead, MovieUpdate

router = APIRouter(tags=["movies"])

# creating and listing go under a list (/lists/1/movies) since a movie needs a list.
# once a movie exists it has its own id, so the rest just use /movies/{movie_id}


def get_movie_or_404(movie_id: int, session: Session) -> Movie:
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# CREATE (add a movie to a list)
@router.post("/lists/{list_id}/movies", response_model=MovieRead, status_code=201)
def add_movie(list_id: int, new_movie: MovieCreate, session: SessionDep):
    if not session.get(MovieList, list_id):
        raise HTTPException(status_code=404, detail="List not found")
    movie = Movie.model_validate(new_movie, update={"list_id": list_id})
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


# READ ALL (every movie in one list)
@router.get("/lists/{list_id}/movies", response_model=list[MovieRead])
def get_movies(list_id: int, session: SessionDep):
    if not session.get(MovieList, list_id):
        raise HTTPException(status_code=404, detail="List not found")
    return session.exec(select(Movie).where(Movie.list_id == list_id)).all()


# READ ONE
@router.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, session: SessionDep):
    return get_movie_or_404(movie_id, session)


# UPDATE (like marking it watched or giving it a rating)
@router.patch("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, changes: MovieUpdate, session: SessionDep):
    movie = get_movie_or_404(movie_id, session)
    movie.sqlmodel_update(changes.model_dump(exclude_unset=True))
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


# DELETE
@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, session: SessionDep):
    movie = get_movie_or_404(movie_id, session)
    session.delete(movie)
    session.commit()
