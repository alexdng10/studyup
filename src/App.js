// where we use components

// App.js
import { Routes, Route } from "react-router-dom"
import Home from "./components/Home"
import FilterButton from "./components/FilterButton";
import AddQuiz from "./components/AddQuiz";
import React from 'react';
import Search from './components/Search';
import initialDetails from './data/initialDetails';
import Card from './components/Card';
  
function App(props) {
  // console.log("completed")

  const quizList = props.quizzes?.map((quiz) => (
  <AddQuiz id={quiz.id} name={quiz.name} completed={quiz.completed} key={quiz.id} /> ));

  return (
    <section className="garamond">
        <div className="navy georgia ma0 grow">
            <Card />
            <h1 className="f1">StudyUp</h1>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/search" element={<Search details={props.quizzes} />} />
            </Routes>
        </div>
    </section>
);
  }

export default App;
  