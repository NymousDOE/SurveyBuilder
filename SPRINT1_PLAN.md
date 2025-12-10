
# Sprint 1 — Plan (2 tygodnie)

## Cel sprintu
Dostarczyć podstawową funkcjonalność tworzenia ankiet i dodawania pytań różnych typów, zielone CI.

## Zakres (wybrane z BACKLOG.csv)
- US1: Utworzenie ankiety
- US2: Dodanie pytania tekstowego
- US3: Dodanie pytania wielokrotnego wyboru
- US4: Dodanie pytania ze skalą
- US6: Lista ankiet
- TECH1: Pipeline CI
- TECH4: Storage JSON

**Story Points razem**: 17 (realistyczny zakres na 2 tygodnie)

## Zadania techniczne

### Architektura i setup
- Inicjalizacja repo i struktury projektu
- Konfiguracja Python virtual environment
- Setup CI/CD (GitHub Actions)

### Model danych
- Klasa Survey (id, title, description, questions, status, created_at)
- Klasa Question z podtypami:
  - TextQuestion
  - MultipleChoiceQuestion (z opcjami)
  - ScaleQuestion (min=1, max=5)
- Storage manager (in-memory + JSON persistence)

### API Endpoints
- POST /surveys - utworzenie ankiety
- GET /surveys - lista ankiet
- GET /surveys/{id} - szczegóły ankiety
- POST /surveys/{id}/questions - dodanie pytania
- GET /surveys/{id}/questions - lista pytań

### Testy
- Testy jednostkowe dla modeli danych
- Testy dla storage managera
- Testy integracyjne dla API endpoints
- Coverage >= 80%

### CI/CD
- Konfiguracja GitHub Actions
- Testy automatyczne (pytest)
- Linting (flake8)
- Formatowanie (black --check)
- Security scan (bandit)

## Definition of Done
- ✅ Wszystkie zaplanowane user stories zaimplementowane
- ✅ Testy zielone (>= 80% coverage)
- ✅ Lint bez błędów (flake8, black)
- ✅ Security scan bez krytycznych issues
- ✅ PR z code review (>= 1 approval)
- ✅ Uaktualnione README i dokumentacja
- ✅ Demo gotowe do prezentacji

## Podział pracy (sugerowany)
- Developer 1: Model danych + Storage (US1, TECH4)
- Developer 2: API endpoints dla surveys (US1, US6)
- Developer 3: API endpoints dla questions (US2, US3, US4)
- Developer 4: Testy + CI/CD (TECH1)

## Daily Standup
- 10 min każdego dnia roboczego
- Format: Co zrobiłem? Co planuję? Blokery?
- Synchronizacja przez Slack/Discord

## Ryzyka sprintu
- **R1**: Zbyt ambitny zakres
  - *Mitygacja*: MoSCoW prioritization, możliwość przeniesienia US6 do Sprint 2
- **R2**: Problemy z integracją storage
  - *Mitygacja*: Start od prostego in-memory, JSON jako enhancement
- **R3**: Brak doświadczenia z testowaniem API
  - *Mitygacja*: Pair programming, dokumentacja pytest

## Sprint Review
- Data: koniec tygodnia 2
- Agenda: Demo funkcjonalności, retrospektywa
- Uczestnicy: Zespół + prowadzący
