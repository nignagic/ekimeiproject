import { useEffect, useMemo, useState } from "react";
import { Link, Route, Routes } from "react-router-dom";

const LEGACY_BASE = "http://localhost:8000";
const QUESTIONS_PER_PLAY = 5;
const BASE_POINT = 10;
const LINE_STATION_POINT = 2;
const LINE_ORDER_BONUS = 20;

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

  if (loading) return <section className="panel">Loading...</section>;
  if (error) return <section className="panel error">{error}</section>;
  if (!data) return <section className="panel error">No data</section>;

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
    </div>
  );
}

function AdjacentStationQuizMode() {
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
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
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
      .finally(() => setLoadingQuestions(false));
  };

  useEffect(() => {
    fetchQuestions(false);
  }, []);

  const restartGame = (nextIncludeClosed) => {
    const includeClosed = nextIncludeClosed ?? includeClosedStations;
    fetchQuestions(includeClosed);
  };

  const submitAnswer = (event) => {
    event.preventDefault();
    if (!currentQuestion || isAnswered) return;

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
    if (!isAnswered) return;
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
    <div className="mode-card">
      <h3>モードA: 前後駅ヒント</h3>
      <p className="quiz-note">1プレイ{QUESTIONS_PER_PLAY}問。ヒント利用で減点。</p>
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
          廃駅を含む（将来用）
        </label>
        <button type="button" onClick={() => restartGame()}>最初からプレイ</button>
      </div>

      {loadingQuestions ? <p>問題を読み込み中...</p> : null}
      {loadingError ? <p className="error">{loadingError}</p> : null}
      {!loadingQuestions && !loadingError && questions.length === 0 ? <p>出題可能な問題がありません。</p> : null}

      {isGameFinished ? (
        <div className="quiz-finished">
          <p>ゲーム終了！最終スコア: {score}pt</p>
          <button type="button" onClick={() => restartGame()}>もう一度プレイ</button>
        </div>
      ) : null}

      {!loadingQuestions && !loadingError && currentQuestion && currentIndex < questions.length ? (
        <>
          <p className="quiz-progress">第 {currentIndex + 1} 問 / {questions.length} 問 ・合計 {score}pt</p>
          <div className="quiz-question-box">
            <p>路線: {currentQuestion.line}</p>
            <p>前の駅: {currentQuestion.prev}</p>
            <p>次の駅: {currentQuestion.next}</p>
          </div>
          <form onSubmit={submitAnswer} className="quiz-answer-form">
            <input value={answerText} onChange={(event) => setAnswerText(event.target.value)} placeholder="駅名を入力" disabled={isAnswered} />
            <button type="submit" disabled={isAnswered || !answerText.trim()}>回答する</button>
          </form>
          <div className="quiz-hints">
            <button
              type="button"
              onClick={() => {
                if (!currentQuestion || lengthHintOpened || isAnswered) return;
                setLengthHintOpened(true);
                setHintPenalty((prev) => prev + 2);
              }}
              disabled={lengthHintOpened || isAnswered}
            >
              文字数ヒント（-2pt）
            </button>
            <button
              type="button"
              onClick={() => {
                if (!currentQuestion || isAnswered) return;
                if (revealedChars >= currentQuestion.answer.length) return;
                setRevealedChars((prev) => prev + 1);
                setHintPenalty((prev) => prev + 1);
              }}
              disabled={isAnswered}
            >
              頭文字を1文字開く（-1pt）
            </button>
          </div>
          <ul className="quiz-hint-list">
            {lengthHintOpened ? <li>文字数: {currentQuestion.answer.length}文字</li> : null}
            {revealedChars > 0 ? <li>先頭ヒント: {revealedInitial}</li> : null}
            <li>この問題の減点: -{hintPenalty}pt</li>
          </ul>
          {resultMessage ? <p className="quiz-result">{resultMessage}</p> : null}
          {isAnswered ? <button type="button" onClick={goNext}>次の問題へ</button> : null}
        </>
      ) : null}
    </div>
  );
}

function LineCompleteQuizMode() {
  const [includeClosedStations, setIncludeClosedStations] = useState(false);
  const [lineQuestion, setLineQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [inputText, setInputText] = useState("");
  const [score, setScore] = useState(0);
  const [message, setMessage] = useState("");
  const [answeredNames, setAnsweredNames] = useState([]);
  const [submissionOrder, setSubmissionOrder] = useState([]);
  const [bonusGranted, setBonusGranted] = useState(false);

  const stations = lineQuestion?.stations ?? [];
  const normalizedStations = useMemo(() => stations.map((name) => normalizeText(name)), [stations]);
  const answeredSet = useMemo(() => new Set(answeredNames), [answeredNames]);
  const isCompleted = stations.length > 0 && answeredNames.length === stations.length;

  const fetchLineQuestion = (nextIncludeClosed) => {
    setLoading(true);
    setError("");
    setMessage("");
    fetch(`/api/station-quiz/line-mode/?include_closed=${nextIncludeClosed ? "1" : "0"}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setLineQuestion(json);
        setInputText("");
        setScore(0);
        setAnsweredNames([]);
        setSubmissionOrder([]);
        setBonusGranted(false);
      })
      .catch((err) => {
        setLineQuestion(null);
        setError(`問題の取得に失敗しました: ${err.message}`);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLineQuestion(false);
  }, []);

  const tryBonus = (nextOrder) => {
    if (nextOrder.length !== stations.length || bonusGranted) {
      return;
    }
    const forward = nextOrder.every((index, i) => index === i);
    const backward = nextOrder.every((index, i) => index === stations.length - 1 - i);
    if (forward || backward) {
      setScore((prev) => prev + LINE_ORDER_BONUS);
      setBonusGranted(true);
      setMessage(`全駅制覇！始点→終点の順で回答できたのでボーナス +${LINE_ORDER_BONUS}pt`);
      return;
    }
    setMessage("全駅制覇！ボーナス条件（始点から終点まで順番回答）は未達成です。");
  };

  const submitStation = (event) => {
    event.preventDefault();
    if (!lineQuestion || !inputText.trim() || isCompleted) {
      return;
    }

    const normalizedInput = normalizeText(inputText);
    const foundIndex = normalizedStations.findIndex((name) => name === normalizedInput);

    if (foundIndex === -1) {
      setMessage("この路線には存在しない駅名です。もう一度入力してください。");
      return;
    }

    const actualName = stations[foundIndex];
    if (answeredSet.has(actualName)) {
      setMessage("その駅はすでに回答済みです。");
      return;
    }

    const nextAnsweredNames = [...answeredNames, actualName];
    const nextOrder = [...submissionOrder, foundIndex];

    setAnsweredNames(nextAnsweredNames);
    setSubmissionOrder(nextOrder);
    setInputText("");
    setScore((prev) => prev + LINE_STATION_POINT);
    setMessage(`正解！ ${actualName} (+${LINE_STATION_POINT}pt)`);

    if (nextAnsweredNames.length === stations.length) {
      tryBonus(nextOrder);
    }
  };

  return (
    <div className="mode-card">
      <h3>モードB: 路線全駅コンプリート</h3>
      <p className="quiz-note">ランダムな路線の全駅を、順番自由で入力して埋めてください。</p>
      <div className="quiz-controls">
        <label>
          <input
            type="checkbox"
            checked={includeClosedStations}
            onChange={(event) => {
              const nextChecked = event.target.checked;
              setIncludeClosedStations(nextChecked);
              fetchLineQuestion(nextChecked);
            }}
          />
          廃駅を含む（将来用）
        </label>
        <button type="button" onClick={() => fetchLineQuestion(includeClosedStations)}>別の路線で再挑戦</button>
      </div>

      {loading ? <p>問題を読み込み中...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      {lineQuestion && !loading ? (
        <>
          <div className="quiz-question-box">
            <p>路線: {lineQuestion.line}</p>
            <p>駅数: {stations.length}</p>
            <p>獲得ポイント: {score}pt</p>
          </div>

          <form onSubmit={submitStation} className="quiz-answer-form">
            <input value={inputText} onChange={(event) => setInputText(event.target.value)} placeholder="この路線の駅名を入力" disabled={isCompleted} />
            <button type="submit" disabled={isCompleted || !inputText.trim()}>回答する</button>
          </form>

          <p className="quiz-progress">回答済み: {answeredNames.length} / {stations.length}</p>
          <div className="answer-chip-list">
            {stations.map((stationName) => (
              <span
                key={stationName}
                className={answeredSet.has(stationName) ? "answer-chip answered" : "answer-chip"}
              >
                {answeredSet.has(stationName) ? stationName : "??"}
              </span>
            ))}
          </div>

          {message ? <p className="quiz-result">{message}</p> : null}
        </>
      ) : null}
    </div>
  );
}

function StationQuiz() {
  const [mode, setMode] = useState("adjacent");

  return (
    <section className="panel station-quiz">
      <h2>駅名クイズ</h2>
      <div className="mode-switch">
        <button type="button" className={mode === "adjacent" ? "active" : ""} onClick={() => setMode("adjacent")}>モードA: 前後駅ヒント</button>
        <button type="button" className={mode === "line" ? "active" : ""} onClick={() => setMode("line")}>モードB: 路線全駅</button>
      </div>
      {mode === "adjacent" ? <AdjacentStationQuizMode /> : <LineCompleteQuizMode />}
    </section>
  );
}

function About() {
  return (
    <section className="panel">
      <h2>About This Frontend</h2>
      <p>React + React Router are served by Vite on port 5173.</p>
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
