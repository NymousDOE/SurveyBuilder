
# Acceptance Criteria — MVP

## Funkcjonalność

### 1. Tworzenie ankiety (US1)
- **GIVEN** użytkownik ma dostęp do API
- **WHEN** wysyła POST /surveys z `{"title": "My Survey", "description": "Survey description"}`
- **THEN** 
  - Otrzymuje status 201 Created
  - Response zawiera `{"id": "uuid", "title": "My Survey", "description": "Survey description", "status": "draft"}`
  - Ankieta jest dostępna w GET /surveys

### 2. Dodawanie pytań tekstowych (US2)
- **GIVEN** istnieje ankieta o ID = "survey-123"
- **WHEN** wysyła POST /surveys/survey-123/questions z `{"type": "text", "question": "What is your name?"}`
- **THEN**
  - Otrzymuje status 201 Created
  - Pytanie pojawia się w GET /surveys/survey-123/questions
  - Pytanie ma unikalny ID

### 3. Dodawanie pytań wielokrotnego wyboru (US3)
- **GIVEN** istnieje ankieta o ID = "survey-123"
- **WHEN** wysyła POST /surveys/survey-123/questions z 
  ```json
  {
    "type": "multiple_choice",
    "question": "Choose your favorite color",
    "options": ["Red", "Blue", "Green"]
  }
  ```
- **THEN**
  - Otrzymuje status 201 Created
  - Pytanie zawiera wszystkie opcje
  - Można wybrać dokładnie jedną opcję przy odpowiadaniu

### 4. Dodawanie pytań ze skalą (US4)
- **GIVEN** istnieje ankieta o ID = "survey-123"
- **WHEN** wysyła POST /surveys/survey-123/questions z `{"type": "scale", "question": "Rate our service", "min": 1, "max": 5}`
- **THEN**
  - Otrzymuje status 201 Created
  - Pytanie akceptuje tylko wartości 1-5
  - Wartości spoza zakresu są odrzucane

### 5. Publikacja ankiety (US5)
- **GIVEN** istnieje ankieta w statusie "draft"
- **WHEN** wysyła POST /surveys/survey-123/publish
- **THEN**
  - Status ankiety zmienia się na "published"
  - Generowany jest unikalny URL: `/surveys/survey-123/respond`
  - Ankieta staje się dostępna dla uczestników

### 6. Lista ankiet (US6)
- **GIVEN** istnieją 3 ankiety w systemie
- **WHEN** wysyła GET /surveys
- **THEN**
  - Otrzymuje listę wszystkich ankiet
  - Każda ankieta zawiera: id, title, status, question_count, response_count

### 7. Udzielanie odpowiedzi (US7)
- **GIVEN** ankieta o ID = "survey-123" jest opublikowana
- **WHEN** uczestnik wysyła POST /surveys/survey-123/responses z odpowiedziami
  ```json
  {
    "responses": [
      {"question_id": "q1", "answer": "John Doe"},
      {"question_id": "q2", "answer": "Blue"},
      {"question_id": "q3", "answer": 5}
    ]
  }
  ```
- **THEN**
  - Otrzymuje status 201 Created
  - Odpowiedź jest zapisana z unikalnym ID
  - Licznik response_count jest inkrementowany

### 8. Podgląd wyników (US8)
- **GIVEN** ankieta ma 10 odpowiedzi
- **WHEN** wysyła GET /surveys/survey-123/results
- **THEN**
  - Otrzymuje `{"response_count": 10, "questions": [...]}`
  - Dla pytań wielokrotnego wyboru: rozkład procentowy odpowiedzi
  - Dla pytań ze skalą: średnia, min, max
  - Dla pytań tekstowych: liczba odpowiedzi

### 9. Eksport CSV (US9)
- **GIVEN** ankieta ma odpowiedzi
- **WHEN** wysyła GET /surveys/survey-123/export
- **THEN**
  - Otrzymuje plik CSV z nagłówkami
  - Każdy wiersz = jedna odpowiedź
  - Kolumny: response_id, timestamp, question_1, question_2, ...

## Jakość kodu

### CI/CD (TECH1)
- ✅ GitHub Actions workflow jest skonfigurowany
- ✅ Przy każdym push do main uruchamiają się:
  - pytest (wszystkie testy muszą przejść)
  - flake8 (zero błędów)
  - black --check (kod jest sformatowany)
  - bandit (zero krytycznych issues)
- ✅ Pull Requesty wymagają zielonego CI przed merge

### Code Quality
- ✅ Test coverage >= 80%
- ✅ Wszystkie funkcje publiczne mają docstringi
- ✅ Kod zgodny z PEP 8
- ✅ Brak hardcoded secrets
- ✅ Error handling dla wszystkich API endpoints

## Performance (dla MVP)
- Utworzenie ankiety: < 100ms
- Dodanie pytania: < 50ms
- Udzielenie odpowiedzi: < 200ms
- Eksport CSV (do 100 odpowiedzi): < 1s

## Bezpieczeństwo
- ✅ Walidacja wszystkich inputów
- ✅ Brak SQL injection (używamy JSON storage)
- ✅ Rate limiting (opcjonalne dla MVP)
- ✅ CORS properly configured
