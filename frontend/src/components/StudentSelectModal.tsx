import { useState, useMemo } from 'react';

import type { Student } from './DeckBuilder';

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

interface Props {
  students: Student[];
  targetSquadType: string;
  onSelect: (student: Student) => void;
  onClose: () => void;
}

export default function StudentSelectModal({ students, targetSquadType, onSelect, onClose }: Props) {
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    let filteredList = students.filter(s => s.SquadType === targetSquadType);
    if (search) {
      filteredList = filteredList.filter(s => s.Name.toLowerCase().includes(search.toLowerCase()));
    }
    return filteredList;
  }, [students, search, targetSquadType]);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{targetSquadType === 'Main' ? '스트라이커 선택' : '스페셜 선택'}</h3>
          <button onClick={onClose} className="close-btn">X</button>
        </div>
        
        <input 
          type="text" 
          placeholder="학생 이름 검색..." 
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="search-input"
          autoFocus
        />
        
        <div className="student-list">
          {filtered.map(st => (
            <div key={st.Id} className="student-list-item" onClick={() => onSelect(st)}>
              <img src={`https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/icon/${st.Id}.webp`} alt={st.Name} />
              <span>{getRoleIcon(st.TacticRole)} {st.Name}</span>
            </div>
          ))}
          {filtered.length === 0 && <p style={{textAlign: 'center', padding: '20px'}}>검색 결과가 없습니다.</p>}
        </div>
      </div>
    </div>
  );
}
