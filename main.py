from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import SauceURLChoices, MenuCreate,MenuWithID,  Menu, Siders 
from typing import Annotated
from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)  # Instantiate FastAPI


# @app.get('/')
# async def index() -> dict[str, str]:
#     return {'hello': 'world'}


@app.get('/menu')
async def menu(sauce: SauceURLChoices | None = None,
               q: Annotated[str | None, Query(max_length=10)] = None,
                session: Session = Depends(get_session)
               ) -> list[Menu]:

    all_menu = session.exec(select(Menu)).all()
    if sauce:
        all_menu = [
            m for m in all_menu if m.sauce.value.lower() == sauce.value.lower()
        ]
    if q:
        all_menu = [
            m for m in all_menu if q.lower() in m.name.lower()
        ]
    return all_menu


@app.get('/menu/{menu_id}')
async def about(
    menu_id: Annotated[int, Path(title="Menu_ID")],
    session: Session = Depends(get_session)
) -> Menu:
    menu = session.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail='Menu item not found')
    return menu
 


# @app.get('/menu/sauce/{sauce}')
# async def menu_for_sauce(sauce: SauceURLChoices) -> list[MenuWithID]:
#     # Filter menus by sauce (case-insensitive)
#     result = [MenuWithID(**m) for m in Menu_List if m['sauce'].lower() == sauce.value.lower()]
#     if not result:
#         raise HTTPException(status_code=404, detail="No menu items found for the given sauce.")
#     return result


@app.post('/menu')
async def create_menu_item(
    menu_data: MenuCreate,
    session: Session = Depends(get_session)
    ) -> Menu:
    menu = Menu(name = menu_data.name, sauce = menu_data.sauce)

    session.add(menu)

    if menu_data.siders:
        for sider in menu_data.siders:
            sider_obj = Siders(title=sider.title, release_date = sider.release_date, menu = menu)
            session.add(sider_obj)
    session.commit()
    session.refresh(menu)
    return menu