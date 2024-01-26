import React from 'react';
import './Header.css'; 
const Header = () => {
    return (
        <header>
            <nav>
                <div className="logo">Study Up</div>
                <ul className="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Courses</a></li>
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;