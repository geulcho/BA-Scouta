import { useState, useEffect } from 'react';
import DeckBuilder from './components/DeckBuilder';
import type { DeckSlot, Student } from './components/DeckBuilder';
import StudentSelectModal from './components/StudentSelectModal';

const createEmptyDeck = (size: number): DeckSlot[] => 
  Array(size).fill(null).map(() => ({ student: null, level: 90, star: 3, ue: 0 }));

export default function App() {
  const [allStudents, setAllStudents] = useState<Student[]>([]);
  const [myDeck, setMyDeck] = useState<DeckSlot[]>(createEmptyDeck(6));
  const [oppDeck, setOppDeck] = useState<DeckSlot[]>(createEmptyDeck(6));
  const [loading, setLoading] = useState(false);
  const [guide, setGuide] = useState<string | null>(null);
  
  const [editingSlot, setEditingSlot] = useState<{isOpponent: boolean, index: number, targetSquadType: string} | null>(null);

  useEffect(() => {
    fetch('/api/students')
      .then(res => res.json())
      .then(data => setAllStudents(data.students))
      .catch(err => console.error('Failed to load students', err));
  }, []);

  const handleSlotClick = (isOpponent: boolean, index: number, targetSquadType: string) => {
    setEditingSlot({ isOpponent, index, targetSquadType });
  };

  const handleLevelChange = (isOpponent: boolean, index: number, level: number) => {
    const newDeck = isOpponent ? [...oppDeck] : [...myDeck];
    newDeck[index].level = level;
    isOpponent ? setOppDeck(newDeck) : setMyDeck(newDeck);
  };

  const handleStarChange = (isOpponent: boolean, index: number, star: number, ue: number) => {
    const newDeck = isOpponent ? [...oppDeck] : [...myDeck];
    newDeck[index].star = star;
    newDeck[index].ue = ue;
    isOpponent ? setOppDeck(newDeck) : setMyDeck(newDeck);
  };

  const handleSelectStudent = (st: Student) => {
    if (!editingSlot) return;
    
    const { isOpponent, index } = editingSlot;
    const newDeck = isOpponent ? [...oppDeck] : [...myDeck];
    newDeck[index].student = st;
    
    // Default to level 90, 5 star UE1 if not set
    if (!newDeck[index].level) newDeck[index].level = 90;
    
    isOpponent ? setOppDeck(newDeck) : setMyDeck(newDeck);
    setEditingSlot(null);
  };

  const requestPrediction = async () => {
    const myValidCount = myDeck.filter(s => s.student !== null).length;
    if (myValidCount < 6) {
      alert("공격 덱 6명을 모두 채워주세요.");
      return;
    }
    
    setLoading(true);
    setGuide(null);
    try {
      const res = await fetch('/api/predict_manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          my_deck: myDeck,
          opp_deck: oppDeck
        }),
      });
      
      const data = await res.json();
      if (data.guide) setGuide(data.guide);
    } catch (err) {
      console.error(err);
      alert('가이드 생성 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header style={{ textAlign: 'center', marginBottom: '40px' }} className="animate-entrance">
        <h1>BA Scouta</h1>
        <p style={{ fontSize: '1.2rem', color: '#666' }}>블루 아카이브 전술 대회(PvP) 승률 예측 LLM 어시스턴트</p>
      </header>

      <main>
        <section className="card animate-entrance">
          <h2>덱 편성</h2>
          <DeckBuilder 
            myDeck={myDeck} 
            oppDeck={oppDeck}
            onSlotClick={handleSlotClick}
            onLevelChange={handleLevelChange}
            onStarChange={handleStarChange}
          />
          <div style={{ textAlign: 'center', marginTop: '30px' }}>
            <button className="btn" onClick={requestPrediction} disabled={loading}>
              {loading ? '예측 중... ⏳' : '결과 예측하기'}
            </button>
          </div>
        </section>

        {guide && (
          <section className="card animate-entrance" style={{ animationDelay: '0.2s' }}>
            <h2>🤖 전술 가이드 및 승률 예측</h2>
            <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px', whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
              {guide}
            </div>
          </section>
        )}
      </main>

      {editingSlot && (
        <StudentSelectModal 
          students={allStudents}
          targetSquadType={editingSlot.targetSquadType}
          onSelect={handleSelectStudent}
          onClose={() => setEditingSlot(null)}
        />
      )}
    </div>
  );
}
