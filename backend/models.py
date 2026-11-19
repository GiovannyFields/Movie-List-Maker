from sqlmodel import Field, Relationship, SQLModel

# ---------- Lists ----------


# fields every version of a list shares
class MovieListBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


# table=True makes this one an actual table in the database
class MovieList(MovieListBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # cascade_delete means deleting a list also deletes the movies in it
    movies: list["Movie"] = Relationship(back_populates="movie_list", cascade_delete=True)


# what the API expects when you create a list (no id, the db makes that)
class MovieListCreate(MovieListBase):
    pass


# what the API sends back (always has an id)
class MovieListRead(MovieListBase):
    id: int


# for PATCH everything is optional so you can change just one thing
class MovieListUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


# ---------- Movies (each one belongs to a list) ----------


class MovieBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=1888, le=2100)  # 1888 = first film ever
    genre: str | None = Field(default=None, max_length=50)
    overview: str | None = Field(default=None, max_length=500)
    rating: int | None = Field(default=None, ge=1, le=10)
    watched: bool = False


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    list_id: int = Field(foreign_key="movielist.id", ondelete="CASCADE")
    movie_list: MovieList = Relationship(back_populates="movies")


# list_id isn't in here because it comes from the URL (/lists/{list_id}/movies)
class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id: int
    list_id: int


class MovieUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=1888, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    overview: str | None = Field(default=None, max_length=500)
    rating: int | None = Field(default=None, ge=1, le=10)
    watched: bool | None = None


# ---------- Suggestions (not a table, just the shape the API sends back) ----------


class Suggestion(SQLModel):
    title: str
    year: int
    genre: str
    overview: str
