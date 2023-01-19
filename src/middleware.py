from fastapi import Header, HTTPException

async def tokenCheck(authorization: str = Header(default=None)):
    try:
        authHeader = authorization.split()
        authType = authHeader[0]
        token = authHeader[1]
        if authType != 'Bearer' and token != 'token-jabar-juara':
            raise HTTPException(401, detail='Anda tidak memiliki hak akses')
    except:
        raise HTTPException(401)