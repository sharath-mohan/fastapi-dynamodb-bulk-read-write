from fastapi import FastAPI, Path
from .schema import Item
from .models import User
from uuid import uuid4, UUID
import time
from typing import Annotated
from datetime import timedelta
app = FastAPI()

# create a constant that has 100 fake users
id = uuid4()
users= [User(search_id=str(id), user_id =str(i),  name=f"User{i}", age=20 + i % 10, timestamp=int(time.thread_time_ns())) for i in range(5)]

@app.post("/")
def add_results(item:Item):
    start_time = time.perf_counter()
    i=0
    with User.batch_write() as batch:
       
        for user in users:
            i+=1
            batch.save(user)
            print(i)
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)        
    return {"message": len(users)}

@app.get("/{search_id}")
def read_results(search_id:Annotated[UUID,Path()]):
    start_time = time.perf_counter()
    results = []
    for user in User.query(str(search_id), limit=10):
        results.append(user)
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)
    return {"message": results}

@app.put("/{search_id}")
def update_result(search_id:Annotated[UUID,Path()], user_id: str, subjects: list[str]):
    user = User.get(str(search_id), user_id)
    user.subject = subjects
    user.save()
    return {"message": "Updated successfully"}

@app.get("/count/{search_id}")
def count_results(search_id:Annotated[UUID,Path()]):
    start_time = time.perf_counter()
    count = 0
    for _ in User.query(str(search_id), filter_condition=User.subject.exists()):
        count += 1
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)
    return {"message": count}