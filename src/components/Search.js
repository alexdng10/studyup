import SearchList from './SearchList';
import { Link } from 'react-router-dom';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import React, { useState } from 'react';

function Search({ details }) {

    const [searchField, setSearchField] = useState("");

    const filteredQuizzes = details && Array.isArray(details)
    ? details.filter(quiz => quiz.name.toLowerCase().includes(searchField.toLowerCase()))
    : [];
  
    // const filteredQuizzes = details.filter(
    //   quiz => {
    //     return (
    //       quiz
    //       .name
    //       .toLowerCase()
    //       .includes(searchField.toLowerCase()) 
    //     );
    //   }
    // );
  
    const handleChange = e => {
      setSearchField(e.target.value);
    };
  
    function searchList() {
        return <SearchList filteredQuizzes={filteredQuizzes} />;
    }

    return (
        <section className="garamond">
            <div className="navy garamond ma0 flex items-center justify-center">
                <p className="f1">Search Your Course</p>
            </div>
            <div className="pa0 flex items-center justify-center">
                <input
                    className="pa3 bb br3 grow b--none bg-lightest-blue ma3"
                    type="search"
                    placeholder="Search"
                    onChange={handleChange}
                />
            </div>
            <Link to="/search">Search</Link>
            {searchList()}
        </section>
    );
  }
  
  export default Search;