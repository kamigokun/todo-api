from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, todos

# This create FastAPI application.
# title , description, version show up in swagger docs automatically
app = FastAPI(
    title = "Todo API",
    description = "A production ready TODO REST API with JWT authentication",
    version= "1.0.0"
)


# -----------CORS Middleware----------------
# CORS = Cross Origin Resource Sharing
# this allows API to be called from a frontend app
# running on a different domain/part - like react on localhost: 3000
# calling your API on localhost:3000
# without this browsers block the request automatically.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          #in production level word replace * with your frontend URL.
    allow_credentials = True,
    allow_methods=["*"],            # allow all HTTP methods
    allow_headers=["*"],              # allow all headers

)



# ------------Routers-----------------------------------
# This is where im connecting my routers to the main app.
# Every route defined in auth.router and todos.router
# is now party of my app.
app.include_router(auth.router)
app.include_router(todos.router)




# -----------------Global Error Handlers------------------------------
# These catch errors that aren't caught anywhere else.
# Instead of crashing or returning ugly errors.
# i'll return clean JSON responses every time.

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """
    catches any 404 error across the whole app.
    for example hitting /randomendpoint that doesn't exist.
    """

    return JSONResponse(
        status_code = 404,
        content = {"message": "The resource you are looking or does not exist"}
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    """
    catches any unexpected server crash.
    Insteasd of leaking internal error details to the user.
    we return a clean generic message.
    NEVER EXPOSE INTERNAL ERRORS TO THE OUTSIDE WORLD.
    """

    return JSONResponse(
        status_code = 500,
        content={"message": "An internal server error occurred"}
    )



# ------------Health Check---------------------
# This is a simple endpoint to check if API is running.
# Used by deployment  platforms. Docker, and monitoring tools
# to know that app is alive and healthy.
# HIT GET/ and if you get a response, the app is running.
@app.get("/", tags = ["Health"])
def health_check():
    return {"status": "ok", "message": "Todo API is running"}