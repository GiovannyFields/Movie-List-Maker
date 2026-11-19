from sqlmodel import Field, SQLModel


# fields every version of a list shares
class MovieListBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


# table=True makes this one an actual table in the database
class MovieList(MovieListBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


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
