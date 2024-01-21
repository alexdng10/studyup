import React from 'react';
import Search from './Search';  // Correct the import path
import SearchList from './SearchList';  // Correct the import path
import Card from './Card';  // Correct the import path

function SearchPage() {
  return (
    <section className="garamond">
      <div className="navy georgia ma0 grow">
        <h1 className="f1">StudyUp</h1>
        {/* Use the components with corrected import paths */}
        <Search />
        <SearchList />
        <Card />
      </div>
    </section>
  );
}

export default SearchPage;