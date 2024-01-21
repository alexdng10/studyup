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
                    <div key={i} className="quest">
                    <h2>{q.question}</h2>
                        <div id="ans">
                            <input type="radio" id="0" value='0' name={i} />
                            <label for="1">{q.options[0]}</label><br/>
                        </div>
                        <div id="ans">
                            <input type="radio" id="1" value='1' name={i} />
                            <label for="1">{q.options[1]}</label><br/>
                        </div>
                            <div id="ans">
                            <input type="radio" id="2" value='2' name={i} />
                            <label for="1">{q.options[2]}</label><br/>
                        </div>
                        <div id="ans">
                            <input type="radio" id="3" value='3' name={i} />
                            <label for="1">{q.options[3]}</label><br/>
                        </div>
                    <h3 id={isVisibile ? 'reveal' : 'hiding'} className={i == q.correct_index ? 'correct' : 'incorrect'}> correct answer: {q.options[q.correct_index]}</h3>
                    {console.log(i)}
                    {console.log(q.correct_index)}
                    <br/>
                    </div>
                ))}
                <div id="buttons" class="center">
                    <button type="submit">New Quiz!</button><br/>
                    <button onClick={handleClick}>Reveal Answers</button>
                </div>
                </form>
            )}
        </div>
    )
}

export default Question;