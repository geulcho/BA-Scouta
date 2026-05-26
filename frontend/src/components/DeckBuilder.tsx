

export interface Student {
  Id: number;
  Name: string;
  BulletType: string;
  ArmorType: string;
  SquadType: string; // "Main" | "Support"
  TacticRole: string;
  StreetBattle: string;
  PvPMaxHP: number;
  HealPower: number;
  DodgePoint: number;
}

export interface DeckSlot {
  student: Student | null;
  level: number;
  star: number; // 1-5
  ue: number; // 0-3 (Unique Equipment)
}

interface DeckBuilderProps {
  myDeck: DeckSlot[];
  oppDeck: DeckSlot[];
  onSlotClick: (isOpponent: boolean, index: number, targetSquadType: string) => void;
  onLevelChange: (isOpponent: boolean, index: number, level: number) => void;
  onStarChange: (isOpponent: boolean, index: number, star: number, ue: number) => void;
}

const getBulletColor = (bulletType: string) => {
  switch (bulletType) {
    case 'Explosion': return '#e53935'; // Red
    case 'Pierce': return '#fbc02d';    // Yellow
    case 'Mystic': return '#1e88e5';    // Blue
    case 'Sonic': return '#8e24aa';     // Purple
    default: return '#e0e0e0';
  }
};

const getRoleIcon = (role: string) => {
  switch (role) {
    case 'Tanker': return '🛡️';
    case 'DamageDealer': return '⚔️';
    case 'Healer': return '🌿';
    case 'Supporter': return '🪄';
    case 'Vehicle': return '🚜';
    default: return '';
  }
};

export default function DeckBuilder({
  myDeck, oppDeck, onSlotClick, onLevelChange, onStarChange
}: DeckBuilderProps) {

  const renderSlot = (slot: DeckSlot, index: number, isOpponent: boolean, targetSquadType: string) => {
    return (
      <div key={`${isOpponent ? 'opp' : 'my'}-${index}`} className="deck-slot">
        <div 
          className="slot-portrait" 
          onClick={() => onSlotClick(isOpponent, index, targetSquadType)}
        >
          {slot.student ? (
            <img 
              src={`https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/icon/${slot.student.Id}.webp`} 
              alt={slot.student.Name} 
              style={{ borderColor: getBulletColor(slot.student.BulletType) }}
            />
          ) : (
            <div className="empty-slot">?</div>
          )}
        </div>
        
        {slot.student && (
          <div className="slot-controls">
            <div className="student-name" title={slot.student.Name}>
              <span style={{ fontSize: '0.8rem', marginRight: '2px' }}>{getRoleIcon(slot.student.TacticRole)}</span>
              {slot.student.Name}
            </div>
            <div className="control-row">
              <label>Lv.</label>
              <input 
                type="number" 
                value={slot.level} 
                onChange={e => onLevelChange(isOpponent, index, parseInt(e.target.value) || 1)}
                min="1" max="90" 
              />
            </div>
            <div className="control-row">
              <select 
                value={`${slot.star}-${slot.ue}`}
                onChange={e => {
                  const [s, u] = e.target.value.split('-').map(Number);
                  onStarChange(isOpponent, index, s, u);
                }}
              >
                <option value="1-0">1성</option>
                <option value="2-0">2성</option>
                <option value="3-0">3성</option>
                <option value="4-0">4성</option>
                <option value="5-0">5성</option>
                <option value="5-1">전무1</option>
                <option value="5-2">전무2</option>
                <option value="5-3">전무3</option>
              </select>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderDeckRow = (deck: DeckSlot[], isOpponent: boolean) => {
    return (
      <div className="deck-row-container" style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        <div className="sub-deck" style={{ flex: 2, background: 'rgba(255,255,255,0.5)', padding: '15px', borderRadius: '8px' }}>
          <h4 style={{ textAlign: 'center', marginTop: 0, marginBottom: '10px', color: '#555' }}>Striker (스트라이커)</h4>
          <div className="roster-grid">
            {deck.slice(0, 4).map((slot, i) => renderSlot(slot, i, isOpponent, 'Main'))}
          </div>
        </div>
        <div className="sub-deck" style={{ flex: 1, background: 'rgba(255,255,255,0.5)', padding: '15px', borderRadius: '8px' }}>
          <h4 style={{ textAlign: 'center', marginTop: 0, marginBottom: '10px', color: '#555' }}>Special (스페셜)</h4>
          <div className="roster-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(110px, 1fr))' }}>
            {deck.slice(4, 6).map((slot, i) => renderSlot(slot, i + 4, isOpponent, 'Support'))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="deck-builder">
      <div className="deck-section">
        <h3 style={{ color: '#1976d2' }}>내 공격 덱 (6명 필수)</h3>
        <p className="help-text">자신의 편성에 있는 6명(스트라이커 4명, 스페셜 2명)을 모두 입력하세요.</p>
        {renderDeckRow(myDeck, false)}
      </div>

      <div className="deck-section" style={{ marginTop: '30px' }}>
        <h3 style={{ color: '#d32f2f' }}>상대 방어 덱</h3>
        <p className="help-text">상대방 덱에서 보이는 학생들만 입력하세요. 빈칸(?)은 AI가 메타에 따라 예측합니다.</p>
        {renderDeckRow(oppDeck, true)}
      </div>
    </div>
  );
}
