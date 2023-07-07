from Api import SapConnection
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI()


class CargoRequest(BaseModel):
    ROWSKIPS: int = 0
    ROWCOUNT: int = 1000
    FIELDS: List[str] = []
    WHERE: List[Dict[str, str]] = []
    CONFIG :Dict[str,str] = []


class RfcRequest(BaseModel):
    ROWSKIPS: int = 0
    ROWCOUNT: int = 1000
    FIELDS: List[str] = []
    WHERE: List[Dict[str, str]] = []
    CONFIG :Dict[str,str] = []
    TABELA: str


class BapiRequest(BaseModel):
    BAPI: str
    CONFIG :Dict[str,str] = [] 
    KWARGS : Dict[str,str] = {}
    

@app.get("/")
async def root():
    return {"message": "Conexao SAPRFC-PYRFC- Para Swagger: http://seuip:8080/docs "}


@app.post("/bapi")
async def Bapi(request: BapiRequest, parametro: str = Query('')):

    try:
        call = SapConnection(request.CONFIG)
        result = call.GenericABAPI(
            BAPI = request.BAPI,
            **request.KWARGS

        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/rfc")
async def Rfc(request: RfcRequest, parametro: str = Query('')):


    try:
        call = SapConnection(request.CONFIG)
        result = call.RFCgenericTable(
            QUERY_TABLE = request.TABELA,
            ROWSKIPS=request.ROWSKIPS,
            ROWCOUNT=request.ROWCOUNT,
            FIELDS=request.FIELDS,
            OPTIONS=request.WHERE,
        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == '__main__':
    uvicorn.run("MainBaseModel:app", port=8080, host='0.0.0.0', reload=True)
