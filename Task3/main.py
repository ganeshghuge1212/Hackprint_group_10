from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import WebScraper
from typing import Dict, Any

app = FastAPI(title="Web Scraper API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    success: bool
    data: Dict[str, Any] | None = None
    error: str | None = None

@app.get("/")
async def root():
    return {
        "message": "Web Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/scrape": "POST - Scrape a website",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_website(request: ScrapeRequest):
    try:
        scraper = WebScraper(request.url)
        data = scraper.scrape_all()
        return ScrapeResponse(success=True, data=data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
