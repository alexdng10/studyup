import { useState, useEffect } from 'react';
import '../index.css';

function Question() {

    const[data, setData] = useState([{}])

    useEffect(() => {
        fetch("/quiz").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])

    const answers = document.getElementById
    const[isVisibile, setIsVisible] = useState(false);

    const handleClick = (event) => {
        event.preventDefault();
        setIsVisible(true);
    }

    const handleSubmit = (event) => {

    }


    return(
        <div>
            {(typeof data[0].question === 'undefined') ? (
                <p>Loading...</p>
            ): (
                <form onSubmit={handleSubmit}>
                {data.map((q, i) => (
                    <div key={i}>
                    <p>{q.question}</p>
                        <input type="radio" id="0" value='0' name={i} />
                        <label for="1">{q.options[0]}</label><br/>
                        <input type="radio" id="1" value='1' name={i} />
                        <label for="1">{q.options[1]}</label><br/>
                        <input type="radio" id="2" value='2' name={i} />
                        <label for="1">{q.options[2]}</label><br/>
                        <input type="radio" id="3" value='3' name={i} />
                        <label for="1">{q.options[3]}</label><br/>
                    <p id={isVisibile ? 'reveal' : 'hiding'} className={i == q.correct_index ? 'correct' : 'incorrect'}> correct answer: {q.options[q.correct_index]}</p>
                    {console.log(i)}
                    {console.log(q.correct_index)}
                    <br/>
                    </div>
                ))}
                <input type="submit" value="New Quiz!"></input><br/>
                <button onClick={handleClick}>reveal answers</button>
                </form>
            )}
        </div>
    )
}

export default Question;