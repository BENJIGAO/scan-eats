import React from "react";
import styled from "styled-components";

import "./landingPage.css";
import { useNavigate } from 'react-router-dom'

const Button = styled.div`
  margin: 5%;
  margin-right:60%;
  padding: 2rem;
  font-size: 1rem;
  border: 3px solid #fff;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
  background: transparent;
  color: #fff;
`;


function LandingPage() {
  
    const navigate = useNavigate();
  
    const handleOnSubmit = () => {
      navigate('/scan');
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
          <Button onClick={handleOnSubmit}>
          <text style={{marginLeft:"17%"}}>Get started</text>
          </Button>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
