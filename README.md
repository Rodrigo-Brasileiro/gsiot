# 🆘 Sistema de Detecção de Queda e Sinal de S.O.S com Arduino e Visão Computacional

Este projeto combina **Arduino**, **Python**, **OpenCV** e **MediaPipe** para criar um sistema inteligente capaz de detectar **quedas de pessoas** e reconhecer **sinais manuais de S.O.S em Libras**. O objetivo é oferecer suporte em **situações de emergência**, especialmente em locais com **baixa iluminação**, como durante apagões.

---

## 🧠 Conceito

Pensado para monitorar **idosos ou pessoas vulneráveis**, o sistema usa uma câmera comum para acompanhar movimentos do corpo e mãos. Se uma **queda** for detectada por mais de 3 segundos ou se a pessoa fizer o gesto **S.O.S** com as mãos (em Libras), o sistema envia um sinal ao **Arduino**, que emite **diferentes sons com um buzzer** para identificar o tipo de emergência.

> ⚡ Um sistema de baixo custo e alto impacto, com foco em usabilidade real em emergências.

---

## 🛠️ Componentes Utilizados

### 🔌 Hardware
- 1 Arduino Uno ou Nano
- 1 Buzzer ativo
- Protoboard
- Jumpers macho-macho
- Cabo USB

### 💻 Software
- Python 3.10+
- OpenCV
- cvzone (MediaPipe simplificado)
- pyserial
- Arduino IDE
- Anaconda Navigator (recomendado)

---

## 🚨 O Que o Sistema Faz?

### ✅ Detecção de Quedas
- Verifica se a **cabeça da pessoa está abaixo dos joelhos**.
- Mantém esse estado por **mais de 3 segundos**.
- Envia um sinal `'Q ou F'` via serial para o Arduino.

### ✅ Reconhecimento de Sinal S.O.S
- Detecta gestos em sequência:
  - `S`: todos os dedos fechados `[0, 0, 0, 0, 0]`
  - `O`: polegar e indicador levantados `[1, 1, 0, 0, 0]`
  - `S`: todos os dedos fechados novamente
- Se a sequência for correta, envia `'2'` para o Arduino.

---

## 🔊 Reação do Arduino

| Evento              | Código Serial | Resposta do Arduino       |
|---------------------|---------------|----------------------------|
| Queda               | `'Q'`         | 5 bipes agudos rápidos     |
| Sinal de S.O.S      | `'S'`         | 3 bipes graves e longos    |

---

## 💡 Suporte para Ambientes Escuros

O sistema melhora a visualização em locais escuros:
- Aumento de contraste e brilhom melhorando a qualidade da detecção

> ✅ Assim, continua funcionando mesmo em pouca luz (ideal para apagões).

---

## 🖼️ Visualização na Tela

- A webcam mostra a imagem da pessoa.
- Quando o gesto `S`, `O` ou `S` é reconhecido, a **letra aparece na tela** em tempo real.
- Ao reconhecer a queda ou o gesto completo de S.O.S, o sistema **envia o alerta automaticamente**.

---

## 🧩 Como Usar o Projeto

### 1. Monte o Circuito Arduino
- Conecte o buzzer ao pino digital 8 e GND.
- Use jumpers e protoboard conforme o código.

### 2. Instale os pacotes no Python

```bash
pip install opencv-python cvzone pyserial
```

### Abra o Visual Studio code pela Anaconda Navigator
 Em sequência execute o arquivo selecionando a câmera ou um vídeo para teste

## MEMBROS DO GRUPO:
* NIKOLAS RODRIGUES MOURA DOS SANTOS - RM551566 
* THIAGO JARDIM DE OLIVEIRA - RM551624 
* RODRIGO BRASILEIRO - RM98952 
