from fastapi import APIRouter, Depends

from app.authorization.fastapi_users_auth.auth import current_user

bucket_router = APIRouter(tags=["Bucket"], dependencies=[Depends(current_user)])


@bucket_router.get("/getBucketOfUser")
async def get_user_bucket():
    return "User bucket GET"


@bucket_router.post("/postBucketOfUser")
async def post_user_bucket():
    return "User bucket POST"
