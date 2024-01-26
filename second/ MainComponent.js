// MainComponent.js or in App.js

import React, { useState } from 'react';
import Question from './Question'; // Import the Question component

function MainComponent() {
    const [showQuiz, setShowQuiz] = useState(false);

    const handleCardClick = () => {
        setShowQuiz(true); // Set to true to show the quiz
    };

    return (
        <div>
            {!showQuiz ? (
                <div>
                    <div className="card" onClick={handleCardClick}>
                        Psychology
                    </div>
                    {/* Other cards here */}
                </div>
            ) : (
                <Question />
            )}
        </div>
    );
}

export default MainComponent;   