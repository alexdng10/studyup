// where we use components

// App.js
import FilterButton from "./components/FilterButton";
import AddQuiz from "./components/AddQuiz";
import React from 'react';
import Search from './components/Search';
import initialDetails from './data/initialDetails';
  
function App(props) {
  // console.log("completed")

  const quizList = props.quizzes?.map((quiz) => (
  <AddQuiz id={quiz.id} name={quiz.name} completed={quiz.completed} key={quiz.id} /> ));

  return (
    <section className="garamond">
    <div className="navy georgia ma0 grow">
    {/* <div className="studyapp stack-large">
      <h1>StudyUp</h1> */}
      <Search details={initialDetails}/>
      
        {/* <h2 className="label-wrapper">
          <label htmlFor="new-quiz-input" className="label__lg">
            Which course do you want to study?
          </label>
        </h2>
        <input
          type="text"
          id="new-quiz-input"
          className="input input__lg"
          name="text"
          autoComplete="off"
        />
        <button type="submit" className="btn btn__primary btn__lg">
          Add
        </button>
      </form> */}
      {/* <div className="filters btn-group stack-exception">
        <FilterButton />
        <FilterButton />
        <FilterButton /> */}
        {/* <button type="button" className="btn toggle-btn" aria-pressed="true">
          <span className="visually-hidden">Show </span>
          <span>All</span>
          <span className="visually-hidden"> Quizzes</span>
        </button>
        <button type="button" className="btn toggle-btn" aria-pressed="false">
          <span className="visually-hidden">Show </span>
          <span>Active</span>
          <span className="visually-hidden"> Quizzes</span>
        </button>
        <button type="button" className="btn toggle-btn" aria-pressed="false">
          <span className="visually-hidden">Show </span>
          <span>Completed</span>
          <span className="visually-hidden"> Quizzes</span>
        </button> */}
      {/* </div>
      <h2 id="list-heading">3 Quizzes Remaining</h2>
      <ul
        role="list"
        className="quiz-list stack-large stack-exception"
        aria-labelledby="list-heading"> */}
        {/* {quizList} */}
        {/* <AddQuiz name = "Quiz 1" id="quiz-0" completed />
        <AddQuiz name = "Quiz 2" id="quiz-1" completed />
        <AddQuiz name = "Quiz 3" id="quiz-2"/> */}
      {/* </ul> */}
    </div>
    </section>
  );
}

export default App;