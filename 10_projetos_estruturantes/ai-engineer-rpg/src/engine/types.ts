// Tipos de domínio do jogo. Regras de negócio (pontos, D20, rubricas JEV) vivem
// em módulos puros de src/engine — alcançáveis pelos testes de camada única.

export type Tier = 'iniciante' | 'intermediario' | 'avancado'

export interface GlossaryTerm {
  id: string
  en: string
  pt: string
  def: string
  /** fórmula/relação central em notação plana (dicionário e tooltips) */
  formula?: string
  /** exemplo prático e fácil de entender */
  example?: string
}

export interface Lesson {
  id: string
  title: string
  /** parágrafos didáticos em PT-BR */
  body: string[]
  /** ids de GlossaryTerm usados nesta lição */
  terms: string[]
}

export interface Question {
  id: string
  prompt: string
  options: string[]
  /** índice da opção correta (0-based) */
  correct: number
  explanation: string
  /** obrigatória por questão — comprada por 100 pontos (mecânica do usuário) */
  hint: string
}

export type SourceKind = 'book' | 'course' | 'docs' | 'paper' | 'cookbook'

export interface RealmSource {
  id: string
  title: string
  kind: SourceKind
  url?: string
  /** confiança de curadoria JEV 0..1 — composite scoring (modulo 14) mantido em código */
  confidence: number
  /** data da verificação (curadoria na internet) */
  checkedAt: string
  /** >= 0.7 = auto | 0.5..0.7 = revisar | < 0.5 proibido no pack (modulo 11) */
  flag: 'auto' | 'revisar'
  note?: string
}

export interface Mission {
  id: string
  title: string
  kind: 'mission' | 'boss'
  lessonId: string
  questionIds: string[]
}

export interface Realm {
  id: string
  index: number
  name: string
  tier: Tier
  blurb: string
  /** peso JEV de curadoria; soma dos reinos = 1.0 (validador do pack) */
  jevWeight: number
  lessons: Lesson[]
  missions: Mission[]
  sources: RealmSource[]
}

/** Realm concreto do comic pack: carrega as questões por reino no loader */
export type ContentRealm = Realm & { questions: Question[] }

export interface ContentPack {
  version: string
  organ: string
  realms: ContentRealm[]
  capstone: Capstone
  glossary: GlossaryTerm[]
}

export interface RubricOption {
  text: string
  /** pontos Score 0..4 — rubrica JEV (composite scoring, normalized /4) */
  score: 0 | 1 | 2 | 3 | 4
}

export interface CapstoneTask {
  id: string
  competency: string
  weight: number
  prompt: string
  options: RubricOption[]
}

export interface Capstone {
  dissertation: { prompt: string; minChars: number }
  tasks: CapstoneTask[]
}

// ---------- progresso ----------

export type LedgerKind = 'answer' | 'd20_win' | 'd20_penalty' | 'hint_cost'

export interface LedgerEntry {
  id: string
  kind: LedgerKind
  delta: number
  ref: string
  at: string
}

export interface QuestionState {
  status: 'open' | 'correct'
  via?: 'answer' | 'd20'
  hintBought: boolean
  d20Used: boolean
}

export interface CertificateRecord {
  code: string
  hash: string
  issuedAt: string
  score: number
  name: string
}

export interface CapstoneSubmission {
  scores: Record<string, number>
  essays: Record<string, string>
  dissertation: string
  finalScore: number
  compScores: Record<string, number>
  passed: boolean
}

export interface GameState {
  version: 1
  playerName: string
  ledger: LedgerEntry[]
  questions: Record<string, QuestionState>
  capstone: CapstoneSubmission | null
  certificate: CertificateRecord | null
}

export function emptyGameState(): GameState {
  return {
    version: 1,
    playerName: '',
    ledger: [],
    questions: {},
    capstone: null,
    certificate: null,
  }
}
