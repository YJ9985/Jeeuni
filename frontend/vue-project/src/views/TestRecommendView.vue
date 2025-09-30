정보를<template>
  <main>
    <div class="literacy-container">
      <div class="literacy-full-wrapper">
        
        <section class="literacy-intro">
          <h2 class="literacy-intro-title">"당신의 독서, 지금보다 더 깊어질 수 있습니다."</h2>
          
          <div class="literacy-intro-container">
            <div>
              <img class="literacy-intro-image" src="@/assets/feedback.png" alt="feedback">
            </div>
            
            <div class="literacy-intro-test">
              <p class="literacy-intro-description">
                국가문해교육센터의 데이터를 바탕으로 설계된<br>
                과학적 문해력 테스트를 통해 당신의 독서 수준을 진단하고,<br>
                AI 분석을 더해 이해도와 관심사에 딱 맞는 도서를 추천해드립니다.
              </p>
              <RouterLink :to="{ name: 'TestLiteracy'}" class="literacy-test-link">지금 테스트하기 →</RouterLink>
            </div>
          </div>
        </section>
  
        <section class="literacy-section text-left">
          <div class="literacy-content">
            <h3 class="literacy-subtitle">문해력이란 무엇인가요?</h3>
            <p class="literacy-text">
              문해력은 일상생활에서 다양한 형식의 글과 정보를 정확하게 읽고, 이해하며, 활용할 수 있는 능력을 말합니다.<br>
              단순한 문자 해독을 넘어, 정보 해석과 비판적 사고까지 포함하는 핵심 역량입니다.
            </p>
          </div>
        </section>
        
        <section class="literacy-section text-right">
          <div class="literacy-content">
            <h3 class="literacy-subtitle">문해 능력 기준은 어떻게 판단하나요?</h3>
            <p class="literacy-text">
              지은이는 <strong>국가문해교육센터</strong>의 기준을 참고하여, 실생활 활용에 초점을 맞춘 5단계 문해력 진단 체계를 구축했습니다.<br>
              15문항의 테스트 결과를 바탕으로 여러분의 문해 능력을 종합적으로 분석하여 1단계부터 5단계까지 수준을 안내해드립니다.
            </p>
          </div>
        </section>
        <div class="literacy-ellipse top-ellipse"></div>
        <div class="literacy-ellipse bottom-ellipse"></div>
      </div>
      
    </div>
  </main>
</template>

<script setup>
import "@fontsource/noto-serif-kr";


import { RouterLink } from 'vue-router'
</script>

<style scoped>
.literacy-container {
  display: flex;
  justify-content: center;
  width: 100%;
  background-color: #FEFFE9;
  z-index: 1;
  overflow: hidden;
}

.literacy-full-wrapper {
  box-sizing: border-box;
  position: relative;
  min-width: 1440px;
  max-width: 1600px;
  box-sizing: border-box;
}

.literacy-intro {
  text-align: center;
  margin-top: 188px;
  margin-bottom: 400px;
}

.literacy-intro-title {
  font-size: 40px;
  font-family: "Noto Serif KR", sans-serif;
  font-weight: 300;
  color: #333;
}

.literacy-intro-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 96px;
}

.literacy-intro-image {
  width: 800px;
  height: 520px;
  border-radius: 12px;
  position: relative;
  z-index: 1;
}

.literacy-intro-test {
  width: 520px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 56px;
}

.literacy-intro-description {
  font-size: 20px;
  text-align: left;
}

.literacy-test-link {
  text-align: right;
  font-size: 24px;
  font-weight: 500;
  letter-spacing: 4px;
  color: #444;
  text-decoration: none;
  transition: all 0.3s ease;
}

.literacy-test-link:hover {
  color: #818B7E;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
  transform: translateX(4px);
}

.literacy-section {
  min-height: 156px;
  max-height: 156px;
}

.text-right {
  text-align: right;
  border-right: 3px solid #818B7E;
}

.text-left {
  text-align: left;
  border-left: 3px solid #818B7E;
}

.literacy-section {
  display: flex;
  align-items: center;
  min-height: 156px;
  max-height: 156px;
  margin-bottom: 200px;
}

.literacy-content {
  width: 100%;
}

.literacy-subtitle {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  padding-left: 40px;
  padding-right: 40px;
  margin-bottom: 20px;
}

.literacy-text {
  font-size: 20px;
  font-weight: 400;
  color: #444;
  padding-left: 40px;
  padding-right: 40px;
  margin-bottom: 0px;
}

.literacy-ellipse {
  width: 1620px;
  height: 1620px;
  border: 0.5px solid #95a191;
  opacity: 0.2;
  border-radius: 50%;
  position: absolute;
  z-index: 0;
  pointer-events: none;
}

.top-ellipse {
  top: -640px;
  right: -560px;
}

.bottom-ellipse {
  top: 520px;
  left: -520px;
}
</style>