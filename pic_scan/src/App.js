import './App.css';
import { io } from 'socket.io-client';
import {useEffect, useState} from "react";

const socket = io("http://127.0.0.1:5000");

const App = () => {

    const [counter, setCounter] = useState(0)

    useEffect(() => {
        socket.on('connect', () => {
            console.log("WS Connected")
        });

        socket.on('message', () => {
            setCounter(counter + 1);
        });
    }, [counter]);

    const send = () => {
        socket.emit("message", "Click");
        console.log("CLICKED")
    }

  return (
    <div className="App">
        <h1>Hello</h1>
        <button type="button" className="btn btn-primary" onClick={send}>Primary</button>
        <p>{counter}</p>
    </div>
  );
}

export default App;
