import { useEffect, useMemo, useState } from "react";
import { Link, Route, Routes } from "react-router-dom";

const LEGACY_BASE = "http://localhost:8000";
const QUESTIONS_PER_PLAY = 5;
const BASE_POINT = 10;

function normalizeText(value) {
  return value.replace(/\s+/g, "").trim();
}

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

function StationQuiz() {
  const [includeClosedStations, setIncludeClosedStations] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answerText, setAnswerText] = useState("");
  const [revealedChars, setRevealedChars] = useState(0);
  const [lengthHintOpened, setLengthHintOpened] = useState(false);
  const [hintPenalty, setHintPenalty] = useState(0);
  const [score, setScore] = useState(0);
  const [resultMessage, setResultMessage] = useState("");
  const [isAnswered, setIsAnswered] = useState(false);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [loadingError, setLoadingError] = useState("");

  const currentQuestion = questions[currentIndex];
  const isGameFinished = !loadingQuestions && questions.length > 0 && currentIndex >= questions.length;

  const resetQuestionState = () => {
    setCurrentIndex(0);
    setAnswerText("");
    setRevealedChars(0);
    setLengthHintOpened(false);
    setHintPenalty(0);
    setScore(0);
    setResultMessage("");
    setIsAnswered(false);
  };

  const fetchQuestions = (nextIncludeClosed) => {
    setLoadingQuestions(true);
    setLoadingError("");

    fetch(`/api/station-quiz/questions/?count=${QUESTIONS_PER_PLAY}&include_closed=${nextIncludeClosed ? "1" : "0"}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((json) => {
        setQuestions(Array.isArray(json.questions) ? json.questions : []);
        resetQuestionState();
      })
      .catch((err) => {
        setQuestions([]);
        setLoadingError(`問題の取得に失敗しました: ${err.message}`);
      })
      .finally(() => {
        setLoadingQuestions(false);
      });
  };

  useEffect(() => {
    fetchQuestions(includeClosedStations);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const restartGame = (nextIncludeClosed) => {
    const includeClosed = nextIncludeClosed ?? includeClosedStations;
    fetchQuestions(includeClosed);
  };

  const openLengthHint = () => {
    if (!currentQuestion || lengthHintOpened || isAnswered) {
      return;
    }
    setLengthHintOpened(true);
    setHintPenalty((prev) => prev + 2);
  };

  const openInitialHint = () => {
    if (!currentQuestion || isAnswered) {
      return;
    }
    const maxChars = currentQuestion.answer.length;
    if (revealedChars >= maxChars) {
      return;
    }
    setRevealedChars((prev) => prev + 1);
    setHintPenalty((prev) => prev + 1);
  };

  const submitAnswer = (event) => {
    event.preventDefault();
    if (!currentQuestion || isAnswered) {
      return;
    }

    const isCorrect = normalizeText(answerText) === normalizeText(currentQuestion.answer);
    if (isCorrect) {
      const gained = Math.max(1, BASE_POINT - hintPenalty);
      setScore((prev) => prev + gained);
      setResultMessage(`正解！ +${gained}pt`);
    } else {
      setResultMessage(`不正解… 正解は「${currentQuestion.answer}」です。`);
    }
    setIsAnswered(true);
  };

  const goNext = () => {
    if (!isAnswered) {
      return;
    }
    setCurrentIndex((prev) => prev + 1);
    setAnswerText("");
    setRevealedChars(0);
    setLengthHintOpened(false);
    setHintPenalty(0);
    setResultMessage("");
    setIsAnswered(false);
  };

  const revealedInitial = currentQuestion?.answer.slice(0, revealedChars) ?? "";

  return (
    <section className="panel station-quiz">
      <h2>駅名クイズ（前後駅ヒント）</h2>
      <p className="quiz-note">
        1プレイ{QUESTIONS_PER_PLAY}問。ヒントを使うと、正解時ポイントが減少します。
      </p>

      <div className="quiz-controls">
        <label>
          <input
            type="checkbox"
            checked={includeClosedStations}
            onChange={(event) => {
              const nextChecked = event.target.checked;
              setIncludeClosedStations(nextChecked);
              restartGame(nextChecked);
            }}
          />
          廃駅を含む
        </label>
        <button type="button" onClick={() => restartGame()}>
          最初からプレイ
        </button>
      </div>

      {loadingQuestions ? <p>問題を読み込み中...</p> : null}
      {loadingError ? <p className="error">{loadingError}</p> : null}

      {!loadingQuestions && !loadingError && questions.length === 0 ? (
        <p>出題可能な問題が見つかりませんでした。</p>
      ) : null}

      {isGameFinished ? (
        <div className="quiz-finished">
          <p>ゲーム終了！最終スコア: {score}pt</p>
          <button type="button" onClick={() => restartGame()}>
            もう一度プレイ
          </button>
        </div>
      ) : null}

      {!loadingQuestions && !loadingError && currentQuestion && currentIndex < questions.length ? (
        <>
          <p className="quiz-progress">
            第 {currentIndex + 1} 問 / {questions.length} 問 ・合計 {score}pt
          </p>
          <div className="quiz-question-box">
            <p>路線: {currentQuestion.line}</p>
            <p>前の駅: {currentQuestion.prev}</p>
            <p>次の駅: {currentQuestion.next}</p>
          </div>

          <form onSubmit={submitAnswer} className="quiz-answer-form">
            <input
              value={answerText}
              onChange={(event) => setAnswerText(event.target.value)}
              placeholder="駅名を入力"
              disabled={isAnswered}
            />
            <button type="submit" disabled={isAnswered || !answerText.trim()}>
              回答する
            </button>
          </form>

          <div className="quiz-hints">
            <button type="button" onClick={openLengthHint} disabled={lengthHintOpened || isAnswered}>
              文字数ヒントを開く（-2pt）
            </button>
            <button type="button" onClick={openInitialHint} disabled={isAnswered}>
              頭文字を1文字開く（-1pt）
            </button>
          </div>

          <ul className="quiz-hint-list">
            {lengthHintOpened ? <li>文字数: {currentQuestion.answer.length} 文字</li> : null}
            {revealedChars > 0 ? <li>先頭ヒント: {revealedInitial}</li> : null}
            <li>この問題の減点: -{hintPenalty}pt</li>
          </ul>

          {resultMessage ? <p className="quiz-result">{resultMessage}</p> : null}

          {isAnswered ? (
            <button type="button" onClick={goNext}>
              次の問題へ
            </button>
          ) : null}
        </>
      ) : null}
    </section>
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
          <Link to="/station-quiz">Station Quiz</Link>
          <Link to="/about">About</Link>
          <a href={`${LEGACY_BASE}/`}>Legacy Top</a>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/station-quiz" element={<StationQuiz />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  );
}
