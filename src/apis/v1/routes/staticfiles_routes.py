from os.path import isfile
from fastapi import Response
from mimetypes import guess_type
from fastapi import APIRouter, Request
from starlette.responses import FileResponse



router = APIRouter(tags=["SSO Assets"])

@router.get("/image/{filename}")
async def serve_spa(request: Request, filename):
    if len(filename) == 0:
        return Response(status_code=404)
    local_path = './public/assets/'+filename

    if not isfile(local_path):
        return Response(status_code=404)

    content_type, _ = guess_type(local_path)
    return FileResponse(local_path, media_type=content_type)


@router.get("/user/profile-image/{filename}",summary="Access User Profile Image using file name")
async def serve_image(request: Request, filename):

    if len(filename) == 0:
        return Response(status_code=404)
    #  because we have saved it in db as  './public/profile_image/'+filename' getting it the same from fe.
    local_path = "./public/profile_image/"+filename

    if not isfile(local_path):
        return Response(status_code=404)

    content_type, _ = guess_type(local_path)

    return FileResponse(local_path, media_type=content_type)

