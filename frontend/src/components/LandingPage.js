import React from "react";
import "./landingPage.css";
import { useNavigate } from "react-router-dom";
import { Button } from "antd";
import Pic from '../assets/fruit.png'

function LandingPage() {
  const navigate = useNavigate();

  const handleOnSubmit = () => {
    navigate("/scan");
  };

  return (
    <div className="container">
      <div className="header"></div>

      <div className="content">
        <div className="box">
          <text className="scaneats">ScanEATS</text>
          <div>
            <text className="subtext">Scan food to get started</text>
          </div>
          <Button type="link" onClick={handleOnSubmit}>
            Click to get started
          </Button>
        </div>
        <div className='picture'>
        <img src={Pic}/>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
