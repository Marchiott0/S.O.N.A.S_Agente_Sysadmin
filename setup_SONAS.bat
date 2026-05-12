@echo off
chcp 65001 > nul
title Instalador S.O.N.A.S v7.0
echo ========================================================
echo        S.O.N.A.S - Auto-Instalador de Ambiente
echo ========================================================
echo.

:: 1. Verificando o Python
echo [*] Verificando instalacao do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado no sistema!
    echo Por favor, instale o Python pela Microsoft Store ou python.org e marque a opcao "Add to PATH".
    pause
    exit /b
)
echo [OK] Python detectado.

:: 2. Instalando Dependencias
echo.
echo [*] Instalando bibliotecas do requirements.txt...
pip install -r requirements.txt
echo [OK] Bibliotecas instaladas.

:: 3. Verificando e Instalando o Ollama
echo.
echo [*] Verificando motor de IA Local (Ollama)...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama nao encontrado. Baixando e instalando via winget...
    winget install Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
    echo.
    echo [AVISO IMPORTANTE] O Ollama foi instalado!
    echo Para que o Windows reconheca o comando, feche esta janela, abra o instalador novamente.
    pause
    exit /b
)
echo [OK] Ollama detectado.

:: 4. Baixando o Modelo de Sobrevivencia
echo.
echo [*] Baixando o modelo local Qwen 2.5 Coder (7B)...
echo Isso pode demorar alguns minutos dependendo da sua internet.
ollama pull qwen2.5-coder:7b
echo [OK] Modelo baixado e pronto para uso.

echo.
echo ========================================================
echo   INSTALACAO CONCLUIDA COM SUCESSO!
echo   1. Renomeie o arquivo '.env.example' para '.env'
echo   2. Coloque suas chaves de API
echo   3. Execute o comando: python sonas.py
echo ========================================================
pause