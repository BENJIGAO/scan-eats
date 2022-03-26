// Import dependencies
import React, { useRef, useState, useEffect } from "react"
import * as tf from "@tensorflow/tfjs"
// 1. TODO - Import required model here
// e.g. import * as tfmodel from "@tensorflow-models/tfmodel"
import * as cocossd from "@tensorflow-models/coco-ssd"
import Webcam from "react-webcam"
import "./App.css"
// 2. TODO - Import drawing utility here
// e.g. import { drawRect } from "./utils/drawRect.js";
import { drawRect } from './utils/drawRect'

function App() {
  const [intervalId, setIntervalId] = useState(0)
  const webcamRef = useRef(null)
  const canvasRef = useRef(null)
  const imageRef = useRef(null)

  // Main function
  const runCoco = async () => {
    // 3. TODO - Load network 
    // e.g. const net = await cocossd.load()
    const net = await cocossd.load()
    
    //  Loop and detect hands
    setIntervalId(setInterval(() => {
      detect(net)
    }, 10))
  };

  const detect = async (net) => {
    // Check data is available
    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null &&
      webcamRef.current.video.readyState === 4
    ) {
      // Get Video Properties
      const video = webcamRef.current.video
      const videoWidth = webcamRef.current.video.videoWidth
      const videoHeight = webcamRef.current.video.videoHeight

      // Set video width
      webcamRef.current.video.width = videoWidth
      webcamRef.current.video.height = videoHeight

      // Set canvas height and width
      canvasRef.current.width = videoWidth
      canvasRef.current.height = videoHeight

      // 4. TODO - Make Detections
      // e.g. const obj = await net.detect(video);
      const obj = await net.detect(video)

      obj.forEach(obj => {
        if (obj.class === 'banana') {
          // console.log('x: ' + obj.bbox[0].toString() + ', y: ' + obj.bbox[1].toString())
          console.log('width: ' + obj.bbox[2].toString() + ', height: ' + obj.bbox[3].toString())
          imageRef.current.getContext('2d').drawImage(video, obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3], 0, 0, obj.bbox[2] + 125, obj.bbox[3])
          clearInterval(intervalId)
        }
      })

      // Draw mesh
      const ctx = canvasRef.current.getContext("2d")

      // 5. TODO - Update drawing utility
      // drawSomething(obj, ctx)
      drawRect(obj, ctx)
    }
  };

  useEffect(()=>{runCoco()},[]);

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column' }}>
      <header className="App-header">
        <Webcam
          ref={webcamRef}
          muted={true} 
          style={{
            position: "absolute",
            top: 250,
            left: 200,
            zindex: 9,
            width: 640,
            height: 480,
          }}
        />

        <canvas
          ref={canvasRef}
          style={{
            position: "absolute",
            top: 250,
            left: 200,
            zindex: 8,
            width: 640,
            height: 480,
          }}
        />
      </header>
      <canvas
          ref={imageRef}
          style={{
            position: "absolute",
            top: 250,
            right: 200,
            zindex: 8,
            width: 480,
            height: 480,
          }}
        />
    </div>
  );
}

export default App;