from fastapi import FastAPI, Path
from fastapi.params import Query
from .schema import Item
from .models import User, Product
from uuid import uuid4, UUID
import time
from typing import Annotated
from datetime import timedelta
app = FastAPI()

# create a constant that has 100 fake users
id = uuid4()
users= [User(search_id=str(id), user_id =str(i),  name=f"User{i}", age=20 + i % 10, timestamp=int(time.thread_time_ns())) for i in range(5)]

@app.get("/add-product")
def add_products():
    start_time = time.perf_counter()
    id = uuid4()
    products= [Product(search_id=str(id), product_id =str(i),  name=f"Product{i}" , timestamp=int(time.thread_time_ns()) ) for i in range(100)]
    i=0
    with Product.batch_write() as batch:
       
        for product in products:
            i+=1
            batch.save(product)
            print(i)
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)        
    return {"message": len(products)}

@app.get("/products/{search_id}")
def read_products(search_id:Annotated[UUID,Path()], limit:Annotated[int,Query()]=10, offset:Annotated[int,Query()]=0):
    results = []
    start_time = time.perf_counter()
    # query =  Product.query(str(search_id), limit=limit)
    # items = [product.attribute_values for product in query]

    # query = Product.view_index.query(str(search_id), Product.timestamp > offset, limit=limit)
    # items = [product.attribute_values for product in query]
    # return {"message": items}
    index_results = list(Product.view_index.query(str(search_id), Product.timestamp > offset, limit=limit, last_evaluated_key=None))
    keys_to_fetch = [(item.search_id, item.product_id) for item in index_results]
    print(f"Keys to fetch: {keys_to_fetch}")
    if keys_to_fetch:
        for full_item in Product.batch_get(keys_to_fetch):
            results.append(full_item.attribute_values)
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)
    return {"message": results, "lastIndex": index_results[-1].timestamp if index_results else None, "last_index_item": index_results[-1].attribute_values if index_results else None, "keys_to_fetch": keys_to_fetch}

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



@app.delete("/{search_id}")
def delete_products(search_id:Annotated[UUID,Path()]):
    start_time = time.perf_counter()
    delete_count = 0
    for product in Product.query(str(search_id)):
        product.delete()
        delete_count += 1
    end_time = time.perf_counter()
    elapsed_time_secs = end_time - start_time
    msg = f"Execution took: {timedelta(seconds=round(elapsed_time_secs))} (Wall clock time)"
    print(msg)        
    return {"message": delete_count}