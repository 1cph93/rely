from fastapi import FastAPI

from rely.services.score_repo_service import RepoResult, score_repo


app = FastAPI()


@app.get("/score_repo")
async def score(repo_url: str) -> RepoResult:
    """Score repo endpoint."""

    return await score_repo(repo_url)
