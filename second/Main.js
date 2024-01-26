// Main.js
import React, { useState } from 'react';
import Question from './Question';
import './Main.css'; // Your CSS file for styling

function Main() {
    const [fetchNewQuiz, setFetchNewQuiz] = useState(0);
    const [showAnswer, setShowAnswer] = useState(false);

    const handleNextQuiz = () => {
        setFetchNewQuiz(fetchNewQuiz + 1); // Increment to trigger new quiz fetch
        setShowAnswer(false);
    };

    const handleRevealAnswer = () => {
        setShowAnswer(true);
    };

    return (
        <div className="quiz-container">
            <Question fetchNewQuiz={fetchNewQuiz} />
            {showAnswer && (
                <p className="answer">Correct Answer: { /* Display the correct answer */ }</p>
            )}
            <button onClick={handleNextQuiz}>Next Quiz</button>
          
        </div>
    );
}

export default Main;