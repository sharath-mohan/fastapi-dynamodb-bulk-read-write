import { useEffect, useState } from 'react'

import './App.css'
export interface Response {
    message:            Message[];
    last_evaluated_key: string;
    lek:                Lek;
    first_index:        number;
}

export interface Lek {
    product_id: ID;
    search_id:  ID;
    timestamp:  Timestamp;
}

export interface ID {
    S: string;
}

export interface Timestamp {
    N: string;
}

export interface Message {
    name:       string;
    product_id: string;
    search_id:  string;
    timestamp:  number;
}
function App() {
  const [data, setData] = useState<Message[]>([])
 const [page, setPage] = useState(0)
 const [isPrevious, setIsPrevious ] = useState(false)
 const [cursor, setCursor] = useState<null | string>(null)
 const goPrevious = ()=>{
  setPage(p=>p-1)
  setIsPrevious(true)
 }
 const goNext = ()=>{
  setPage(p=>p+1)
  setIsPrevious(false)
  const fetchData = async()=>{
    let response;
    if(cursor){
       response = await fetch(`http://127.0.0.1:8000/products/aa421163-d96a-4ce4-aa48-7c8b99768b34?limit=10&cursor=${cursor}`)
    }

    response = await fetch(`http://127.0.0.1:8000/products/aa421163-d96a-4ce4-aa48-7c8b99768b34?limit=10`)
    const _data = await response.json()
    console.log(_data)
    setData(
      _data.message
    )
    setCursor(_data.last_evaluated_key
    )
  }
  fetchData()
 }
 useEffect(()=>{
  const fetchData = async()=>{
    let response;
    if(cursor){
       response = await fetch(`http://127.0.0.1:8000/products/aa421163-d96a-4ce4-aa48-7c8b99768b34?limit=10&cursor=${cursor}`)
    }

    response = await fetch(`http://127.0.0.1:8000/products/aa421163-d96a-4ce4-aa48-7c8b99768b34?limit=10`)
    const _data = await response.json()
    console.log(_data)
    setData(
      _data.message
    )
    setCursor(_data.last_evaluated_key
    )
  }
  fetchData()
 },[])

  return (
    <>
    {data.map(e=><li key={e.timestamp}>{e.name}</li>)}
      <button disabled={page ==0} onClick={goPrevious}>previous</button>
      <button onClick={goNext}>next</button>
    </>
  )
}

export default App
