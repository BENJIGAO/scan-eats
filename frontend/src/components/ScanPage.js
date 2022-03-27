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
import { Button, Card } from "antd";

function ScanPage() {
  const [intervalId, setIntervalId] = useState(0);
  const [isWebcamOn, setIsWebcamOn] = useState(false);
  const [isFirstTime, setIsFirstTime] = useState(true);
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const imageRef = useRef(null);
  const imageLinkRef = useRef(null);

  useEffect(() => {
    runCoco();
  }, [isFirstTime]);

  // Main function
  const runCoco = async () => {
    // 3. TODO - Load network
    // e.g. const net = await cocossd.load()
    const net = await cocossd.load();

    //  Loop and detect hands
    setIntervalId(
      setInterval(() => {
        detect(net);
      }, 10)
    );
  };

  const detect = async (net) => {
    // Check data is available
    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null &&
      webcamRef.current.video.readyState === 4 &&
      isWebcamOn
    ) {
      // Get Video Properties
      const video = webcamRef.current.video;
      const videoWidth = webcamRef.current.video.videoWidth;
      const videoHeight = webcamRef.current.video.videoHeight;

      // Set video width
      webcamRef.current.video.width = videoWidth;
      webcamRef.current.video.height = videoHeight;

      // Set canvas height and width
      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      // 4. TODO - Make Detections
      // e.g. const obj = await net.detect(video);
      const obj = await net.detect(video);

      obj.forEach((obj) => {
        if (obj.class === "apple" || obj.class === "bottle") {
          // console.log('x: ' + obj.bbox[0].toString() + ', y: ' + obj.bbox[1].toString())
          // console.log('width: ' + obj.bbox[2].toString() + ', height: ' + obj.bbox[3].toString())
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
                obj.bbox[2] * 1.75,
                obj.bbox[3]
              );
            imageRef.current.toBlob((blob) => {
              imageLinkRef.current = blob;
            });
          } else {
            makeAPIRequest(obj.class);
          }
        }
      });

      // Draw mesh
      const ctx = canvasRef.current.getContext("2d");

      // 5. TODO - Update drawing utility
      // drawSomething(obj, ctx)
      drawRect(obj, ctx);
    }
  };

  const makeAPIRequest = async (foodName) => {
    const formData = new FormData();
    formData.append("image", imageLinkRef.current);

    const response = await fetch("/classify/".concat(foodName), {
      method: "POST",
      body: formData,
    });

    if (response.status === 200) {
      const text = await response.text();
      console.log(text);
    } else {
      console.log("Error with POST request");
    }
  };

  const toggleCamera = () => {
    setIsWebcamOn(!isWebcamOn);
    if (isFirstTime) {
      setIsFirstTime(false);
    }
  };

  const navigate = useNavigate();

  const handleOnSubmit = () => {
    navigate("/");
  };

  return (
    <div>
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
    </div>
  );
}

export default ScanPage;
