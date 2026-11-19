from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from backend.database import create_tables, get_session
from backend.models import MovieList, MovieListCreate, MovieListRead, MovieListUpdate


# runs once when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Movie List Maker API", lifespan=lifespan)


# CREATE
@app.post("/lists", response_model=MovieListRead, status_code=201)
def create_list(new_list: MovieListCreate, session: Session = Depends(get_session)):
    movie_list = MovieList.model_validate(new_list)
    session.add(movie_list)
    session.commit()
    session.refresh(movie_list)  # pulls the new id back from the db
    return movie_list


# READ ALL
@app.get("/lists", response_model=list[MovieListRead])
def get_lists(session: Session = Depends(get_session)):
    return session.exec(select(MovieList)).all()


# READ ONE
@app.get("/lists/{list_id}", response_model=MovieListRead)
def get_list(list_id: int, session: Session = Depends(get_session)):
    movie_list = session.get(MovieList, list_id)
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found")
    return movie_list


# UPDATE
@app.patch("/lists/{list_id}", response_model=MovieListRead)
def update_list(
    list_id: int, changes: MovieListUpdate, session: Session = Depends(get_session)
):
    movie_list = session.get(MovieList, list_id)
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found")
    # exclude_unset means only the fields actually sent get changed
    movie_list.sqlmodel_update(changes.model_dump(exclude_unset=True))
    session.add(movie_list)
    session.commit()
    session.refresh(movie_list)
    return movie_list


# DELETE
@app.delete("/lists/{list_id}", status_code=204)
def delete_list(list_id: int, session: Session = Depends(get_session)):
    movie_list = session.get(MovieList, list_id)
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found")
    session.delete(movie_list)
    session.commit()
