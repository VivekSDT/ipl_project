import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Landing from './components/Landing';
import YearPage from './components/YearPage';

export default function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path='/' element={<Landing />} />
        <Route path='/year/:year' element={<YearPage />} />
      </Routes>
    </Router>
  );
}
