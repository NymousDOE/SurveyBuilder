
# Project Charter — Survey Builder Application

## Cel (SMART)
Do **15 grudnia 2025** dostarczyć wersję MVP aplikacji webowej Survey Builder umożliwiającej:
- tworzenie ankiet z pytaniami różnego typu (tekst, wielokrotny wybór, skala),
- publikowanie ankiet i generowanie linków do udostępniania,
- zbieranie odpowiedzi od uczestników,
- przeglądanie podstawowych statystyk i eksport wyników do CSV.
Czas utworzenia ankiety ≤ 2 min; czas udzielenia odpowiedzi ≤ 5 min; błędy krytyczne ≤ 1/100 uruchomień.

## Zakres (in/out)
**IN:** 
- Tworzenie i edycja ankiet
- 3 typy pytań: tekst otwarty, wybór wielokrotny, skala 1-5
- Publikowanie ankiet (generowanie unikalnego linku)
- Zbieranie odpowiedzi anonimowych
- Podstawowe statystyki (liczba odpowiedzi, wykresy)
- Eksport wyników do CSV
- Testy jednostkowe i integracyjne
- CI/CD pipeline

**OUT:** 
- Logowanie użytkowników i zarządzanie kontami
- Zaawansowana analityka i raporty
- Pytania warunkowe (logika rozgałęzień)
- Integracje z zewnętrznymi systemami
- Płatności i plany premium
- Wielojęzyczność

## Interesariusze
- Klient (prowadzący) – priorytety i akceptacja
- PM zespołu studenckiego – prowadzenie backlogu i sprintów
- Zespół dev/test/DevOps – implementacja i zapewnienie jakości
- Użytkownicy końcowi (twórcy ankiet, respondenci)

## Kryteria sukcesu
- Przejście demo i akceptacja kryteriów z `docs/ACCEPTANCE_CRITERIA.md`
- Zielone pipeline'y w CI (testy, linting, analiza bezpieczeństwa)
- Dokumentacja ukończona (README, DoR/DoD, kryteria akceptacji)
- Możliwość stworzenia ankiety, zebrania odpowiedzi i wyeksportowania wyników

## Założenia
- Zespół 4-5 osób
- 1-2 sprinty (2-4 tygodnie)
- Dostęp do środowiska developerskiego
- Podstawowa znajomość Python i REST API

## Ograniczenia
- Brak prawdziwej bazy danych (storage in-memory z JSON)
- Brak autentykacji i autoryzacji
- Brak UI (tylko API endpoints, ewentualnie prosty HTML)
- Limit 100 odpowiedzi na ankietę dla MVP

## Budżet i zasoby
- Czas: 40-80 godzin roboczych zespołu
- Infrastruktura: bezpłatne narzędzia (GitHub, GitHub Actions)
- Zero kosztów licencyjnych

## Harmonogram (wstępny)
- Sprint 1 (2 tyg.): Tworzenie ankiet, pytania, podstawowe testy
- Sprint 2 (2 tyg.): Zbieranie odpowiedzi, statystyki, eksport, finalizacja
