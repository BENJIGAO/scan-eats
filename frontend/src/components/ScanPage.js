// Import dependencies
import React, { useRef, useState, useEffect } from "react"
// 1. TODO - Import required model here
// e.g. import * as tfmodel from "@tensorflow-models/tfmodel"
import * as tf from "@tensorflow/tfjs"
import * as cocossd from "@tensorflow-models/coco-ssd"
import Webcam from "react-webcam"
import "../App.css"
// 2. TODO - Import drawing utility here
// e.g. import { drawRect } from "./utils/drawRect.js";
import { drawRect } from '../utils/drawRect'
import styled from 'styled-components';

const Section = styled.section`
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #131313;
`;

const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100vh;
  padding: 3rem calc((100vw - 1300px) / 2);

  @media screen and (max-width: 768px) {
    grid-grid-template-columns: 1fr;
  }
`;

const Button = styled.div`
padding: 1rem 3rem;
  font-size: 1rem;
  border: 2px solid #fff;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  background: transparent;
  color: #fff;
`;

const ColumnLeft = styled.div`
  display: flex;
  color: #fff;
  flex-direction: column;
  justify-content: top;
  align-items: flex-start;
  padding: 9rem 100rem;

  h1 {
    margin-bottom: 0.5rem;
    font-size: 2rem;
  }
  p {
    margin: 2rem 0;
    font-size: 4rem;
    line-height: 1.1;
  }
`;

function ScanPage() {
  const [intervalId, setIntervalId] = useState(0)
  const [isWebcamOn, setIsWebcamOn] = useState(false)
  const [isFirstTime, setIsFirstTime] = useState(true)
  const webcamRef = useRef(null)
  const canvasRef = useRef(null)
  const imageRef = useRef(null)
  const imageLinkRef = useRef(null)

  useEffect(()=> {
    runCoco()
  }, [isFirstTime])

  // Main function
  const runCoco = async () => {
    // 3. TODO - Load network 
    // e.g. const net = await cocossd.load()
    const net = await cocossd.load()
    
    //  Loop and detect hands
    setIntervalId(setInterval(() => {
      detect(net)
    }, 10))
  }

  const detect = async (net) => {
    // Check data is available
    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null &&
      webcamRef.current.video.readyState === 4 &&
      isWebcamOn
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
        if (obj.class === 'apple' || obj.class === 'banana') {
          // console.log('x: ' + obj.bbox[0].toString() + ', y: ' + obj.bbox[1].toString())
          // console.log('width: ' + obj.bbox[2].toString() + ', height: ' + obj.bbox[3].toString())
          if (!imageLinkRef.current) {
            imageRef.current.getContext('2d').drawImage(video, obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3], 0, 0, obj.bbox[2] * 1.75, obj.bbox[3])
            imageRef.current.toBlob(blob => {
              imageLinkRef.current = blob
            })
          } else {
            makeAPIRequest(obj.class)
          }
          
        }
      })

      // Draw mesh
      const ctx = canvasRef.current.getContext("2d")

      // 5. TODO - Update drawing utility
      // drawSomething(obj, ctx)
      drawRect(obj, ctx)
    }
  }

  const makeAPIRequest = async (foodName) => {
    const formData = new FormData()
    formData.append('image', imageLinkRef.current)

    const response = await fetch('/classify/'.concat(foodName), {
      method: "POST",
      body: formData
    })

    if (response.status === 200) {
      const text = await response.text()
      console.log(text)
    } else {
      console.log('Error with POST request')
    }
  }

  const toggleCamera = () => {
    setIsWebcamOn(!isWebcamOn)
    if (isFirstTime) {
      setIsFirstTime(false)
    }
  }

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column' }}>
      <header className="App-header">
        {isWebcamOn &&
          <>
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
          </>
        }
        
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
      <Section>
        <Container>
          <ColumnLeft>
            <Button onClick={toggleCamera}>
              {isWebcamOn ? 'Turn Camera off' : 'Turn Camera On'}
            </Button>
          </ColumnLeft>
        </Container>
      </Section>
    </div>
  );
}

export default ScanPage;