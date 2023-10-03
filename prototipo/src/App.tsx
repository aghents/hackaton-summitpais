import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import { BsSearch, BsPerson } from 'react-icons/bs';

import Home from './pages/Home';
import About from './pages/About';

function App() {
  return (
    <Router>
      <Navbar bg="light" expand="lg" fixed="top">
        <Container>
          {/* Left Side */}
          <Navbar.Brand className="d-flex align-items-center">
            <span className="fs-4">Business Name</span>
          </Navbar.Brand>

          {/* Right Side */}
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <Nav.Link as={Link} to="/about">About</Nav.Link>
            </Nav>
            <Form className="d-flex align-items-center">
              <Form.Control type="text" placeholder="Search" className="me-2" />
              <BsSearch className="search-icon me-2" />
              <BsPerson className="person-icon" />
            </Form>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Routes>
        <Route path="/about" element={<About />} />
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
