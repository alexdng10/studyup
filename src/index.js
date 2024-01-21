import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import Question from './components/Question';
import { createBrowserRouter, RouterProvider, Route, } from "react-router-dom";
import Home from './pages/Home';
import Navbar from './components/Navbar';
import './index.css';


const DATA = [
  { id: "quiz-0", name: "Quiz 1", completed: true },
  { id: "quiz-1", name: "Quiz 2", completed: false },
  { id: "quiz-2", name: "Quiz 3", completed: true },
];

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <div id="nav">
      <div id="logo"><h1>StudyUP</h1>
      <img src="https://pngtree.com/freepng/white-book-icon_4628601.html" alt="logo"/>
      </div>
      <ul>
        <li>About</li>
        <li>Courses</li>
        <li>Quizzes</li>
      </ul>
      </div>
      <Navbar />
      <Question />
      {/* <App quizzes={DATA} /> */}
      {/* <App />  */}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
