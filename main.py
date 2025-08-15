import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import uvicorn

load_dotenv()

DESCRIPTION = """
Download Spotify music with album art and metadata.

With Downtify you can download Spotify musics containing album art, track names, album title and other metadata about the songs.
"""


class Message(BaseModel):
    message: str = Field(examples=['Download sucessful'])


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Add security headers
        response = await call_next(request)
        
        # Force HTTPS in production
        if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('FORCE_HTTPS'):
            if request.headers.get('x-forwarded-proto') == 'http':
                url = str(request.url)
                url = url.replace('http://', 'https://', 1)
                return RedirectResponse(url=url, status_code=301)
        
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add CSP header to prevent mixed content
        csp = "default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; img-src 'self' data: https:; font-src 'self' https://cdnjs.cloudflare.com; connect-src 'self' https:;"
        response.headers['Content-Security-Policy'] = csp
        
        return response

app = FastAPI(
    title='Downtify',
    version='0.3.2',
    description=DESCRIPTION,
    contact={
        'name': 'Downtify',
        'url': 'https://github.com/henriquesebastiao/downtify',
        'email': 'contato@henriquesebastiao.com',
    },
    terms_of_service='https://github.com/henriquesebastiao/downtify/',
)

# Add security middleware
app.add_middleware(SecurityMiddleware)


# Configure download directory for Railway storage
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', '/data/downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


@app.on_event("startup")
async def startup_event():
    print("🚀 Downtify application starting up...")
    print(f"📁 Download directory: {DOWNLOAD_DIR}")
    print(f"🌐 Application will be available on port {os.getenv('PORT', '8000')}")

app.mount('/downloads', StaticFiles(directory=DOWNLOAD_DIR), name='downloads')
templates = Jinja2Templates(directory='templates')

DOWNLOADER_OPTIONS: DownloaderOptions = {
    'output': os.getenv(
        'OUTPUT_PATH', default=f'{DOWNLOAD_DIR}/{{artists}} - {{title}}.{{output-ext}}'
    ),
    'ffmpeg': '/downtify/ffmpeg',
}


@lru_cache(maxsize=1)
def get_spotdl():
    return Spotdl(
        client_id=os.getenv(
            'CLIENT_ID', default='5f573c9620494bae87890c0f08a60293'
        ),
        client_secret=os.getenv(
            'CLIENT_SECRET', default='212476d9b0f3472eaa762d90b19b0ba8'
        ),
        downloader_settings=DOWNLOADER_OPTIONS,
    )


def get_downloaded_files() -> str:
    download_path = DOWNLOAD_DIR
    try:
        files = os.listdir(download_path)
        file_links = [
            f'<li class="list-group-item"><a href="/download-file/{file}" download="{file}" class="text-decoration-none"><i class="fa-solid fa-download me-2"></i>{file}</a></li>'
            for file in files
        ]
        files = (
            ''.join(file_links)
            if file_links
            else '<li class="list-group-item">No files found.</li>'
        )
    except Exception as e:
        files = f'<li class="list-group-item text-danger">Error: {str(e)}</li>'

    return files


@app.get(
    '/',
    response_class=HTMLResponse,
    tags=['Web UI'],
    summary='Application web interface',
)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get(
    '/health',
    tags=['Health'],
    summary='Health check endpoint',
)
def health_check():
    """Health check endpoint for Railway monitoring"""
    return {"status": "healthy", "service": "downtify"}


@app.post(
    '/download-web/',
    response_class=HTMLResponse,
    tags=['Downloader'],
    summary='Download one or more songs from a playlist via the WEB interface',
)
def download_web_ui(
    spotdlc: Spotdl = Depends(get_spotdl),
    url: str = Form(...),
):
    """
    You can download a single song or all the songs in a playlist, album, etc.

    - **url**: URL of the song or playlist to download.

    ### Responses

    - `200` - Download successful.
    """
    try:
        songs = spotdlc.search([url])
        spotdlc.download_songs(songs)
    except Exception as error:
        return f"""
    <div>
        <button type="submit" class="btn btn-lg btn-light fw-bold border-white button mx-auto" id="button-download" style="display: block;"><i class="fa-solid fa-down-long"></i></button>
        <div class="alert alert-danger mx-auto" id="success-card" style="display: none;">
            <strong>Error: {error}</strong>
        </div>
    </div>
    """

    return """
    <div>
        <button type="submit" class="btn btn-lg btn-light fw-bold border-white button mx-auto" id="button-download" style="display: block;"><i class="fa-solid fa-down-long"></i></button>
        <div class="alert alert-success mx-auto success-card" id="success-card" style="display: none;">
            <strong>Download completed!</strong>
        </div>
    </div>
    """


@app.post(
    '/download/',
    response_class=JSONResponse,
    response_model=Message,
    tags=['Downloader'],
    summary='Download a song or songs from a playlist',
)
def download(
    url: str,
    spotdlc: Spotdl = Depends(get_spotdl),
):
    """
    You can download a single song or all the songs in a playlist, album, etc.

    - **url**: URL of the song or playlist to download.

    ### Responses

    - `200` - Download successful.
    """
    try:
        songs = spotdlc.search([url])
        spotdlc.download_songs(songs)
        return {'message': 'Download sucessful'}
    except Exception as error:  # pragma: no cover
        return {'detail': error}


@app.get(
    '/list',
    response_class=HTMLResponse,
    tags=['Web UI'],
    summary='List downloaded files',
)
def list_downloads_page(request: Request):
    files = get_downloaded_files()
    return templates.TemplateResponse(
        'list.html', {'request': request, 'files': files}
    )


@app.get(
    '/list-items',
    response_class=HTMLResponse,
    tags=['Web UI'],
    summary='Returns downloaded files to list',
)
def list_items_of_downloads_page():
    files = get_downloaded_files()
    return files


@app.get(
    '/download-file/{filename}',
    tags=['Downloader'],
    summary='Download a specific file',
)
def download_file(filename: str):
    """Download a specific file from the downloads directory"""
    import mimetypes
    from fastapi.responses import FileResponse
    
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=mime_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    try:
        # Handle PORT environment variable more robustly
        port_str = os.getenv("PORT", "8000")
        try:
            port = int(port_str)
        except ValueError:
            print(f"Warning: Invalid PORT value '{port_str}', using default port 8000")
            port = 8000
        
        print(f"Starting Downtify on port {port}")
        print(f"Download directory: {DOWNLOAD_DIR}")
        print(f"Static files mounted at: /static, /assets, /downloads")
        print(f"Health check available at: /health")
        
        # Test if directories exist
        print(f"Checking directories...")
        print(f"Static directory exists: {os.path.exists('static')}")
        print(f"Templates directory exists: {os.path.exists('templates')}")
        print(f"Assets directory exists: {os.path.exists('assets')}")
        print(f"Download directory exists: {os.path.exists(DOWNLOAD_DIR)}")
        
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
