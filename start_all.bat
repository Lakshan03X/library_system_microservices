@echo off
echo Starting all Library System Microservices...
echo.

cd /d "%~dp0"

start "Book Service (8081)" cmd /k "cd book-service && python -m uvicorn main:app --reload --port 8081"
timeout /t 2 >nul

start "Member Service (8082)" cmd /k "cd member-service && python -m uvicorn main:app --reload --port 8082"
timeout /t 2 >nul

start "Borrow Service (8083)" cmd /k "cd borrow-service && python -m uvicorn main:app --reload --port 8083"
timeout /t 2 >nul

start "Review Service (8084)" cmd /k "cd review-service && python -m uvicorn main:app --reload --port 8084"
timeout /t 2 >nul

start "Staff Service (8085)" cmd /k "cd staff-service && python -m uvicorn main:app --reload --port 8085"
timeout /t 2 >nul

start "Reservation Service (8086)" cmd /k "cd reservation-service && python -m uvicorn main:app --reload --port 8086"
timeout /t 2 >nul

start "API Gateway (8080)" cmd /k "cd api-gateway && python -m uvicorn main:app --reload --port 8080"

echo.
echo ================================================
echo All services are starting in separate windows!
echo ================================================
echo.
echo Service URLs:
echo   Book Service:        http://localhost:8081
echo   Member Service:      http://localhost:8082
echo   Borrow Service:      http://localhost:8083
echo   Review Service:      http://localhost:8084
echo   Staff Service:       http://localhost:8085
echo   Reservation Service: http://localhost:8086
echo   API Gateway:         http://localhost:8080
echo.
echo API Documentation: http://localhost:8080/docs
echo.
pause
