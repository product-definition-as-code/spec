"""External handwritten SMT interpretation; no natural-language inference or new PDaC fields."""
import hashlib, json
from pathlib import Path
import yaml

DEPENDENCIES={'booking':['BR-A','TERM-A','LC-A'],
              'authorization':['BR-AUTH','TERM-IDENTITY'],
              'examples':['SB-A','SB-AUTH','BR-A','BR-AUTH','TERM-A','TERM-IDENTITY','LC-A']}

CODES={'REQUESTED':0,'CONFIRMED':1,'CANCELLED':2,'EXPIRED':3}
EXPECTED=['sat','unsat','unsat','unsat','unsat','sat','unsat','sat','unsat','sat','sat']
NAMES=['confirm-reachable','confirm-invariant','cancel-invariant','expire-invariant',
       'lead-compliance','structured-example','authorization-adequacy','guard-mutant',
       'vacuous-guard-witness','frame-mutant','double-release-mutant']


def fm(path):return yaml.safe_load(path.read_text().split('---',2)[1])


def encode(artifacts, semantics):
    """Lifecycle topology comes from frontmatter; rule/term meaning is supplied explicitly."""
    assert isinstance(semantics['footprint'],int) and semantics['footprint']>0
    assert isinstance(semantics['lead_days'],int) and semantics['lead_days']>=0
    lc=fm(artifacts['LC-A']);trans={t['id']:t for t in lc['transitions']}
    assert set(CODES)=={s['id'] for s in lc['states']}
    def source(t):return '(or '+' '.join(f'(= state {CODES[s]})' for s in trans[t]['from'])+')'
    def target(t):return CODES[trans[t]['to']]
    assert semantics['expire_requested']==('REQUESTED' in trans['EXPIRE']['from'])
    size=semantics['footprint'];lead=semantics['lead_days'];ex=semantics['example']
    trusted='(or '+' '.join(f'(= issuer {i})' for i in semantics['trusted_issuers'])+')'
    expiry_effect='(ite (= state 0) used (- used footprint))' if semantics['expire_requested'] else '(- used footprint)'
    header=f'''(set-logic QF_LIA)
(set-option :produce-models true)
(declare-const capacity Int)
(declare-const used Int)
(declare-const state Int)
(declare-const days Int)
(declare-const nextUsed Int)
(declare-const nextState Int)
(declare-const owner Int)
(declare-const nextOwner Int)
(declare-const issuer Int)
(declare-const authentic Bool)
(declare-const editor Bool)
(define-fun footprint () Int {size})
(define-fun Inv ((s Int) (u Int)) Bool
 (and (> capacity 0) (<= 0 u) (<= u capacity) (<= 0 s) (<= s 3)
      (=> (= s 1) (>= u footprint))))
(define-fun Guard () Bool (and {source('CONFIRM')} (>= days 0) (<= days {lead}) (<= (+ used footprint) capacity)))
(define-fun Allow () Bool (and authentic editor {trusted}))
'''
    def query(name,body,values=False):
        return f'(echo "{name}")\n(push 1)\n{body}\n(check-sat)\n'+('(get-value (capacity used state days nextUsed nextState issuer owner nextOwner))\n' if values else '')+'(pop 1)\n'
    text=header
    text+=query(NAMES[0],'(assert (Inv state used))\n(assert Guard)',True)
    text+=query(NAMES[1],f'(assert (Inv state used))\n(assert Guard)\n(assert (= nextUsed (+ used footprint)))\n(assert (= nextState {target("CONFIRM")}))\n(assert (not (Inv nextState nextUsed)))')
    for name,t,effect in [(NAMES[2],'CANCEL','(- used footprint)'),(NAMES[3],'EXPIRE',expiry_effect)]:
        text+=query(name,f'(assert (Inv state used))\n(assert {source(t)})\n(assert (= nextUsed {effect}))\n(assert (= nextState {target(t)}))\n(assert (not (Inv nextState nextUsed)))')
    text+=query(NAMES[4],f'(assert Guard)\n(assert (> days {lead}))')
    text+=query(NAMES[5],f'''(assert (= capacity {ex['capacity']}))
(assert (= used 0))
(assert (= state 0))
(assert (= days 30))
(assert Guard)
(assert (= nextUsed (+ used footprint)))
(assert (= nextUsed {ex['next_used']}))
(assert (= nextState {target('CONFIRM')}))
(assert (= nextState 1))''')
    text+=query(NAMES[6],f'(assert (not (= Allow (and authentic editor {trusted}))))')
    text+=query(NAMES[7],f'''(assert (Inv state used))
(assert (= state 0))
(assert (= days 0))
(assert (= nextUsed (+ used footprint)))
(assert (= nextState 1))
(assert (> nextUsed capacity))''',True)
    text+=query(NAMES[8],'(assert (Inv state used))\n(assert (< used 0))')
    text+=query(NAMES[9],'''(assert (Inv state used))
(assert Guard)
(assert (= nextUsed (+ used footprint)))
(assert (= nextState 1))
(assert (not (= nextOwner owner)))''',True)
    text+=query(NAMES[10],'''(assert (Inv state used))
(assert (= state 1))
(assert (= nextUsed (- (- used footprint) footprint)))
(assert (= nextState 3))
(assert (< nextUsed 0))''',True)
    return text


def statuses(output):return [line for line in output.decode().splitlines() if line in ['sat','unsat','unknown']]


def fingerprint(model, solver_digest):
    return hashlib.sha256(model.encode()+b'\0'+solver_digest.encode()).hexdigest()
