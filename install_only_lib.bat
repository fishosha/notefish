@echo off
chcp 65001 >nul
cls

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════
echo       Notefish - Расширенная установка
echo ════════════════════════════════════════════════════
echo.

:: Переменные
set "PYTHON=python"
set "PIP=pip"
set "REQUIREMENTS=requirements.txt"

:: Проверка Python
echo [1/6] Проверка Python...
%PYTHON% --version >nul 2>&1
if !errorlevel! neq 0 (
    :: Пробуем python3
    python3 --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON=python3"
        set "PIP=pip3"
    ) else (
        echo ❌ Python не найден!
        echo Установите Python с python.org
        pause
        exit /b 1
    )
)

for /f "tokens=*" %%i in ('%PYTHON% --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo ✅ !PYTHON_VERSION!
echo.

:: Создание виртуального окружения
echo [2/6] Создание виртуального окружения...
%PYTHON% -m venv venv 2>nul
if exist venv (
    echo ✅ Виртуальное окружение создано
    set "PYTHON=venv\Scripts\python"
    set "PIP=venv\Scripts\pip"
) else (
    echo ⚠ Не удалось создать виртуальное окружение
    echo Продолжаем с системным Python...
)
echo.

:: Обновление pip
echo [3/6] Обновление pip...
%PYTHON% -m pip install --upgrade pip --quiet
echo ✅ pip обновлен
echo.

:: Проверка tkinter
echo [4/6] Проверка tkinter...
%PYTHON% -c "import tkinter" 2>nul
if !errorlevel! equ 0 (
    echo ✅ tkinter установлен
) else (
    echo ❌ tkinter не найден!
    echo Программа не будет работать без tkinter
    echo.
    pause
    exit /b 1
)
echo.

:: Создание файла требований
echo [5/6] Создание файла требований...
(
echo pillow^>=9.0.0
echo pygments^>=2.11.0
echo ttkthemes^>=3.2.0
echo pyperclip^>=1.8.2
) > %REQUIREMENTS%

echo Файл %REQUIREMENTS% создан
echo.

:: Установка библиотек
echo [6/6] Установка библиотек из %REQUIREMENTS%...
%PIP% install -r %REQUIREMENTS% --quiet
if !errorlevel! equ 0 (
    echo ✅ Все библиотеки установлены
) else (
    echo ⚠ Возникли проблемы при установке
    echo Попробуйте установить библиотеки вручную:
    echo %PIP% install pillow pygments ttkthemes pyperclip
)
echo.

:: Очистка
del %REQUIREMENTS% 2>nul

echo ════════════════════════════════════════════════════
echo          Установка завершена!
echo ════════════════════════════════════════════════════
echo.
if exist venv (
    echo Для запуска в виртуальном окружении:
    echo venv\Scripts\python notefish.py
    echo.
) else (
    echo Для запуска программы:
    echo %PYTHON% notefish.py
    echo.
)
echo Список установленных библиотек:
%PYTHON% -m pip list --format=columns
echo.
pause