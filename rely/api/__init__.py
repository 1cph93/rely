from fastapi import FastAPI

from rely.services.score_repo_service import RepoScore, score_repo


app = FastAPI()


@app.get("/score")
async def score(owner_name: str, repo_name: str) -> RepoScore:
    return await score_repo(owner_name, repo_name)
