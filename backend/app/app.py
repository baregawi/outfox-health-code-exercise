from fastapi import FastAPI


app = FastAPI()
app.add_middleware(
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "This is the Outfox Health coding exercise."}

