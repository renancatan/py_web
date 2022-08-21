import json
# import uvicorn
from fastapi import FastAPI, Request, Form
from scrapes.scrape_music import scrape
from scrapes.scrape_corner import C_t3
from apis.general_pages.route_homepage import general_pages_router

from fastapi.templating import Jinja2Templates
import pathlib
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

BASE_DIR = pathlib.Path(__file__).resolve().parent  # app/
TEMPLATE_DIR = BASE_DIR / "templates"  # / "general_pages"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# if __name__ == '__main__':
data = scrape()
data_t3 = C_t3()


# context = {
#         "request": data_t3.scraper_t3() # [2][0]
#     }
#
# print(context)
#
# for x in context['request']:
#     print(x)

def include_router(app):
    return app.include_router(general_pages_router)


@app.get("/scrape", status_code=200)
async def scraper():
    context = {
        "request": data_t3.scraper_t3()[0]
    }
    print(context)
    return templates.TemplateResponse("general_pages/homepage.html", context)


#     return templates.TemplateResponse("homepage.html", context)  # data_t3.scraper_t3()[2][0]

# @app.get("/scrape", status_code=200,  response_class=HTMLResponse)
# def login_get_view(request: Request):
#     return templates.TemplateResponse("general_pages/homepage.html", {
#         "request": request,
#     })

# @app.get("/scrape/{id}", status_code=200)
# async def prod_id(id: int):
#     print(id)
#     return id


@app.get("/data")
async def song():
    return data.scrapedata()


# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=8000)
