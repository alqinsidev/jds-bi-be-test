from fastapi.responses import JSONResponse
def OK(data,message = 'data berhasil ditemukan'):
    return {"status":200, "message":message, "data":data}

def NOT_FOUND(message='data tidak ditemukan'):
    return JSONResponse(
        status_code=404,
        content={"status":404, "message":message}
    )

def UNAUTHORIZED():
    return JSONResponse(
        status_code=401,
        content={"status":401,"message":"anda tidak memiliki akses untuk sumber ini"}
    )