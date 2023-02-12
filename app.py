
from pickle import APPEND
from fastapi import FastAPI,Request
from fastapi import FastAPI, HTTPException
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
import pydantic

app= FastAPI()

origins=[
    "http://localhost:8000",
    "https://ecse3038-lab3-tester.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Rivbot:ZImDfWoUlYlRUjKh@cluster0.oinoodt.mongodb.net/?retryWrites=true&w=majority")
db= client.water_tank

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

@app.get("/profile")
async def get_all_profiles():
    profiles= await db["profile"].find().to_list(999)
    return profiles[0]

@app.post("/profile")
async def create_new_profile(request:Request):
    tank_object= await request.json()

    new_profile= await db["profile"].insert_one(tank_object)
    created_profile= await db["profile"].find_one({"_id":new_profile.inserted_id})

    return created_profile

@app.get("/data")
async def retrive_tank():
    tanks = await db ["tank"].find().to_list(999)
    return tanks

@app.post("/data")
async def create_new_profile( request: Request):
    tank_object = await request.json()
    new_tank = await db ["tank"].insert_one(tank_object)
    created_tank = await db ["tank"].find_one({"_id": new_tank.inserted_id})

    return created_tank

@app.delete("/data/{id}", status_code=204)
async def delete_tank(id: str):
    tanks = await db["tank"].find_one_and_delete ({"_id": ObjectId(id)})
    return {"the data is deleted"} 

@app.patch ("/data/{id}")
async def do_update(id: str, request: Request):
    update = await request.json()
    result = await db ["tank"]. update_one({"_id":ObjectId(id)}, {'$set': update})
    if result.modified_count == 1:
        if( update_tank := await db ["tank"].find_one({"_id" : id}))is not None:
            return update_tank
        else: 
            raise HTTPException(status_code=404, detail= "data not found")


