
# Definition of Ready (DoR)

User Story jest gotowe do realizacji gdy:
- ✅ Ma jasny opis w formacie "Jako [rola] chcę [funkcjonalność] aby [cel]"
- ✅ Ma zdefiniowane kryteria akceptacji (testowalne)
- ✅ Ma estymację story points (Fibonacci: 1, 2, 3, 5, 8)
- ✅ Ma przypisany priorytet (MUST/SHOULD/COULD/WON'T)
- ✅ Jest zrozumiałe dla całego zespołu (brak blokujących pytań)
- ✅ Nie ma zależności blokujących (lub są one rozwiązane)
- ✅ Jest możliwe do zrealizowania w ramach jednego sprintu

# Definition of Done (DoD)

User Story jest ukończone gdy:
- ✅ Kod jest napisany zgodnie z wymaganiami
- ✅ Kod jest pokryty testami jednostkowymi (>= 80% coverage)
- ✅ Wszystkie testy przechodzą (unit + integration)
- ✅ Kod przeszedł review (min. 1 approval)
- ✅ Kod jest zgodny z linting rules (flake8, black)
- ✅ Security scan nie wykrył krytycznych problemów (bandit)
- ✅ Kod jest zmergowany do main branch
- ✅ Dokumentacja jest zaktualizowana (README, docstrings)
- ✅ Funkcjonalność została zademostrowana Product Ownerowi
- ✅ Kryteria akceptacji zostały spełnione i zweryfikowane

## Dodatkowe kryteria dla Release
- ✅ CI/CD pipeline jest zielony
- ✅ Dokumentacja API jest kompletna
- ✅ Release notes są przygotowane
- ✅ Znane bugi są udokumentowane
