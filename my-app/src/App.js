import React, { useState, useEffect } from 'react';
import './App.css';
import articlesData from './240301_240310_all_cats_arxiv_metadata.json';
import Latex from 'react-latex-next';

const Article = ({ title, author, date, link, summary }) => (
  <div className="article">
    <h2>
      <a href={link} target="_blank" rel="noopener noreferrer">
        {title}
      </a>
    </h2>
    <p className="author-date">By {author} on {date}</p>
    <Latex>{summary}</Latex>
    <div className="article-footer">
      <a href={link} target="_blank" rel="noopener noreferrer">Read more</a>
    </div>
  </div>
);

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const articles = Object.values(articlesData).map((article, index) => ({
      id: index + 1,
      title: article.title,
      author: article.authors.join(', '),
      date: article.updated,
      link: article.url,
      summary: article.summary, 
    }));
    setArticles(articles);
  }, []);




  return (
    <div className="App">
      <header className="App-header">
        <h1>Science Dejargonizer</h1>
      </header>
      <div className="search-bar">
        <input type="text" placeholder="Search..." />
        <button type="button">Submit</button>
      </div>
      <main>
        {articles.map(article => (
          <Article key={article.id} {...article} />
        ))}
      </main>
    </div>
  );
}

export default App;
