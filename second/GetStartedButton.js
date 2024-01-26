import React from 'react';
import './GetStartedButton.css';

const GetStartedButton = ({ onClick }) => {
    return (
        <div className="button-container">
            <button className="get-started-button" onClick={onClick}>Get Started</button>
        </div>
    );
};

export default GetStartedButton;