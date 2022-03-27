// Import dependencies
import React, { useRef, useState, useEffect } from "react";
// 1. TODO - Import required model here
// e.g. import * as tfmodel from "@tensorflow-models/tfmodel"
import * as tf from "@tensorflow/tfjs";
import * as cocossd from "@tensorflow-models/coco-ssd";
import Webcam from "react-webcam";
import "../App.css";
// 2. TODO - Import drawing utility here
// e.g. import { drawRect } from "./utils/drawRect.js";
import { drawRect } from "../utils/drawRect";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { Button, Spin, Modal } from "antd";

function ScanPage() {
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [isScanActive, setIsScanActive] = useState(true)
  const [isLoading, setIsLoading] = useState(true)
  const [isWebcamOn, setIsWebcamOn] = useState(false)
  const [result, setResult] = useState('')
  const [isFirstTime, setIsFirstTime] = useState(true)
  const webcamRef = useRef(null)
  const canvasRef = useRef(null)
  let imageRef = useRef(null)
  let imageLinkRef = useRef(null)

  useEffect(() => {
    runCoco();
  }, [isFirstTime])

  // Main function
  const runCoco = async () => {
    // 3. TODO - Load network
    // e.g. const net = await cocossd.load()
    const net = await cocossd.load()

    //  Loop and detect hands
    setInterval(() => {
      detect(net)
    }, 10)
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
      // e.g. const obj = await net.detect(video)
      const obj = await net.detect(video)

      obj.forEach((obj) => {
        if (obj.class === "apple" || obj.class === "banana") {
          const factor = obj.class === 'apple' ? 1.75 : 2.25
          if (!imageLinkRef.current) {
            imageRef.current
              .getContext("2d")
              .drawImage(
                video,
                obj.bbox[0],
                obj.bbox[1],
                obj.bbox[2],
                obj.bbox[3],
                0,
                0,
                obj.bbox[2] * factor,
                obj.bbox[3]
              );
            imageRef.current.toBlob((blob) => {
              imageLinkRef.current = blob
              makeAPIRequest(obj.class)
            })
            setIsScanActive(false)
          }
        }
      });

      if (!isScanActive) {
        return
      }

      // Draw mesh
      const ctx = canvasRef.current.getContext("2d")

      // 5. TODO - Update drawing utility
      // drawSomething(obj, ctx)
      drawRect(obj, ctx)
    }
  };

  const makeAPIRequest = async (foodName) => {
    const formData = new FormData()
    formData.append("image", imageLinkRef.current)

    const response = await fetch("/classify/".concat(foodName), {
      method: "POST",
      body: formData,
    });

    if (response.status === 200) {
      const text = await response.text()
      setResult(text)
      setIsLoading(false)
      setIsModalVisible(true)
    } else {
      console.log("Error with POST request")
    }
  };

  const toggleCamera = () => {
    setIsWebcamOn(!isWebcamOn)
    if (isFirstTime) {
      setIsFirstTime(false)
    }
  };

  const navigate = useNavigate()

  const handleOnSubmit = () => {
    navigate("/");
  }

  const handleRescan = () => {
    setIsScanActive(true)
    imageRef = null
    imageLinkRef.current = null
    imageLinkRef = null
    setResult('')
    setIsLoading(true)
  }

  return (
    <Spin spinning={isLoading && !isScanActive}>
      <Modal title="Results" visible={isModalVisible} onOk={() => setIsModalVisible(false)} onCancel={() => setIsModalVisible(false)}>
        <p>{result}</p>
      </Modal>
      <div className="container">
        <div className="header"></div>

        <div className="content">
          <Button
            type="primary"
            style={{ margin: "0.5%" }}
            onClick={handleOnSubmit}
            size="default"
          >
            Home
          </Button>
          <Button
            type="primary"
            style={{ margin: "0.5%" }}
            onClick={toggleCamera}
          >
            {isWebcamOn ? "Camera: ON" : "Camera: OFF"}
          </Button>
          {!isScanActive &&
            <Button
            type="primary"
            style={{ margin: "0.5%" }}
            onClick={handleRescan}
            >
              Scan Again
            </Button>
          }
          {isWebcamOn && (
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
          )}
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
      </div>
    </Spin>
  );
}

export default ScanPage;
