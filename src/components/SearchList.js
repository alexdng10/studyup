// src/components/SearchList.js

import React from 'react';
import Card from './Card';

function SearchList({ filteredQuizzes }) {
  const filtered = filteredQuizzes.map(quiz =>  <Card key={quiz.id} quiz={quiz} />); 
  return (
    <div>
      {filtered}
    </div>
  );
}

export default SearchList;