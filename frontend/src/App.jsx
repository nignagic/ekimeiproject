import { useEffect, useMemo, useState } from "react";
import { Link, Route, Routes } from "react-router-dom";

const LEGACY_BASE = "http://localhost:8000";

function Home() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    fetch("/api/top/")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((json) => {
        if (mounted) {
          setData(json);
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(`Failed to load top data: ${err.message}`);
        }
      })
      .finally(() => {
        if (mounted) {
          setLoading(false);
        }
      });

    return () => {
      mounted = false;
    };
  }, []);

  const menuCards = useMemo(
    () => [
      { title: "Search by Railway", href: `${LEGACY_BASE}/railway/` },
      { title: "Search by Creator", href: `${LEGACY_BASE}/creator/` },
      { title: "Search by Music", href: `${LEGACY_BASE}/music/` },
    ],
    []
  );

  if (loading) {
    return <section className="panel">Loading...</section>;
  }
  if (error) {
    return <section className="panel error">{error}</section>;
  }
  if (!data) {
    return <section className="panel error">No data</section>;
  }

  return (
    <div className="top-page">
      <section className="panel hero">
        {data.top_image_url ? (
          <div
            className="hero-bg"
            style={{ backgroundImage: `url(${LEGACY_BASE}${data.top_image_url})` }}
          />
        ) : null}
        <div className="hero-inner">
          <h2>Free Word Search</h2>
          <form action={`${LEGACY_BASE}/search/`} method="get" className="search-form">
            <input name="word" placeholder="station, movie title, creator" />
            <button type="submit">Search</button>
          </form>
          <div className="card-grid">
            {menuCards.map((card) => (
              <a key={card.title} className="card" href={card.href}>
                <h3>{card.title}</h3>
              </a>
            ))}
          </div>
        </div>
      </section>

      <section className="panel">
        <h2>Latest Movies</h2>
        <div className="movie-grid">
          {data.movies.map((movie) => (
            <a key={movie.main_id} className="movie-card" href={`${LEGACY_BASE}${movie.detail_url}`}>
              {movie.youtube_id ? (
                <img
                  className="movie-thumb"
                  src={`https://i.ytimg.com/vi/${movie.youtube_id}/hqdefault.jpg`}
                  alt={movie.title}
                />
              ) : null}
              <p className="movie-meta">
                {movie.published_at_text}
                {movie.is_collab ? ` / ${movie.is_collab}` : ""}
              </p>
              <p className="movie-title">{movie.title}</p>
              <p className="movie-sub">
                {movie.channel}
                {movie.duration ? ` - ${movie.duration}` : ""}
              </p>
            </a>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Today Movie ({data.today_text})</h2>
        {data.today_movie ? (
          <a className="movie-card today" href={`${LEGACY_BASE}${data.today_movie.detail_url}`}>
            {data.today_movie.youtube_id ? (
              <img
                className="movie-thumb"
                src={`https://i.ytimg.com/vi/${data.today_movie.youtube_id}/hqdefault.jpg`}
                alt={data.today_movie.title}
              />
            ) : null}
            <p className="movie-title">{data.today_movie.title}</p>
          </a>
        ) : (
          <p>No movie for today.</p>
        )}
      </section>

      <section className="panel two-column">
        <div>
          <h2>Notices</h2>
          <ul className="simple-list">
            {data.notices.map((notice) => (
              <li key={notice.id}>
                <span>{notice.reg_date}</span>{" "}
                <a href={`${LEGACY_BASE}${notice.url}`}>{notice.head}</a>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h2>Updates</h2>
          <ul className="simple-list">
            {data.updates.map((info, idx) => (
              <li key={`${info.reg_date}-${idx}`}>
                <span>{info.reg_date}</span>{" "}
                {info.url ? <a href={`${LEGACY_BASE}${info.url}`}>{info.text}</a> : info.text}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}

function About() {
  return (
    <section className="panel">
      <h2>About This Frontend</h2>
      <p>
        React + React Router are served by Vite on port 5173. Top page data is loaded
        from <code>/api/top/</code>.
      </p>
    </section>
  );
}

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Ekimei React UI</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <a href={`${LEGACY_BASE}/`}>Legacy Top</a>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  );
}
