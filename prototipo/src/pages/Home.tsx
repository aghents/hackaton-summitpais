import React from 'react';
import Chat from './Chat'

function Home() {
  let id = "y8iEEBxM1UU"
  let url = `https://www.youtube.com/embed/${id}?si=sprDRkbDz6z5zD7_`
  return (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      {/* The content of your Home page */}
      <div>
        <iframe width="560" height="315" src={url} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
      </div>
    <Chat></Chat>
    </div>
  );
}

export default Home;
