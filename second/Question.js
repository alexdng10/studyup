import React, { useState, useEffect } from 'react';

function Question({ fetchNewQuiz }) {
    const [quizData, setQuizData] = useState(null);
    const [selectedAnswers, setSelectedAnswers] = useState({});
    const [showCorrectAnswers, setShowCorrectAnswers] = useState(false);

    useEffect(() => {
        fetchNewQuizData();
    }, [fetchNewQuiz]);

    const fetchNewQuizData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/quiz');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            setQuizData(data);
        } catch (error) {
            console.error('Error fetching quiz data:', error);
        }
    };

    const handleOptionSelect = (questionIndex, optionIndex) => {
        setSelectedAnswers({
            ...selectedAnswers,
            [questionIndex]: optionIndex
        });
    };

    const handleRevealAnswers = () => {
        setShowCorrectAnswers(true);
    };

    if (!quizData) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            {quizData.map((item, questionIndex) => (
                <div key={questionIndex} className="question-block">
                    <p className="question">{item.question}</p>
                    <ul className="options">
                        {item.options.map((option, optionIndex) => (
                            <li key={optionIndex} 
                                className={`option ${selectedAnswers[questionIndex] === optionIndex ? 'selected' : ''}`}
                                onClick={() => handleOptionSelect(questionIndex, optionIndex)}>
                                {option}
                            </li>
                        ))}
                    </ul>
                    {showCorrectAnswers && (
                        <p className="correct-answer">Correct Answer: {item.options[item.correct_index]}</p>
                    )}
                </div>
            ))}
            <button onClick={handleRevealAnswers}>Reveal Answers</button>
        </div>
    );
}

export default Question;