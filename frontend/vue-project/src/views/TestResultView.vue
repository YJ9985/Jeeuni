<template>
  <div class="page-scroll-wrapper">

    <div class="result-container" v-if="result">
      <div class="result-wrapper-1">
        <section class="result-page">
          <h2 class="result-title">{{ userName }} 님의 문해력 테스트 결과</h2>
          <div class="result-info">
            <div class="result-count">
              <div class="result-card">
                <img class="result-image" src="@/assets/result_bulb.png" alt="light bulb">
                <h3 class="result-subtitle">정답 개수</h3>
                <p class="result-total">총 15문제에서</p>
                <h2 class="result-yours">{{ correctCount }}문제 정답</h2>
              </div>
            </div>
            <div class="cross-line"></div>
            <div class="result-level">
              <div class="result-card">
                <img class="result-image" src="@/assets/result_magnifier.png" alt="magnifier">
                <h3 class="result-subtitle">문해력 수준</h3>
                <p class="result-total">1~5단계 중</p>
                <h2 class="result-yours">{{ result.literacy_level }}단계</h2>
              </div>
              <div class="result-modal">
                <a class="result-modal-text" href="" @click.prevent="showModal = true">문해력 수준 자세히 살펴보기 ></a>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  
    <div class="result-container">
      <div class="result-wrapper-2">
        <section class="problem-page">
          <h2 class="result-title">
            오답률 1위 문제,<br>같이 풀어볼까요?
            <p style="font-size: 20px; color:#C0C7BE; margin-top:16px;">틀린 문제 오답 기능은 추후에 추가될 예정이에요.</p>
          </h2>
          <div class="result-problem-info">
            <div class="result-problem">
              <img class="result-problem-image" src="@/assets/top1_problem.png" alt="questions">
            </div>
            <div class="result-questions">
              <div class="result-options">
                <p class="result-options-title">1.&nbsp;㉠은 행정 행위와 종속적인 관계를 갖는 부수적 요소이다.</p>
                <p class="result-options-text">→ ‘㉠ 조건’을 포함한 부관은 “행정 행위에 부수적인 사항”이라고 했으므로 정확한 설명입니다.</p>
              </div>
              <div class="result-options">
                <p class="result-options-title">2.&nbsp;㉠은 조건 성취 여부에 따라 정지 조건과 해제 조건으로 나뉜다.</p>
                <p class="result-options-text">→ 조건은 효력의 발생/소멸 기준으로 정지 조건, 해제 조건으로 나뉘므로 지문과 일치합니다.</p>
              </div>
              <div class="result-options">
                <p class="result-options-title">3.&nbsp;주차장을 설치하면 건축 허가의 효력이 발생하게 하는 경우는 ㉡이다.</p>
                <p class="result-options-text">→ ㉡은 정지 조건이며, “설치하면 효력이 발생”하는 조건이므로 지문과 정확히 일치합니다.</p>
              </div>
              <div class="result-options">
                <p class="result-options-title">4.&nbsp;㉢은 허가의 효력이 발생하지 않았을 때만 소멸시킬 수 있다.</p>
                <p class="result-options-text">→ 이미 발생한 효력을 소멸하게 하는 부관은 해제 조건, 즉 ㉢에 해당하므로 틀린 설명입니다.</p>
              </div>
              <div class="result-answer">
                <p class="result-answer-text">㉢은 허가의 효력이 발생하지 않았을 때만 소멸시킬 수 있다.</p>
              </div>
            </div>
          </div>
  
        </section>
      </div>
    </div>
    <div class="result-container">
      <div class="result-wrapper-3">
        <section class="result-page">
          <h2 class="result-title">
            피드백 및 학습 방향
            <p style="font-size: 28px; color:#C0C7BE; margin-top:8px;">독서, 지금부터는 더 똑똑하게</p>
          </h2>
          <div class="result-info">
            <div class="result-count">
              <div class="result-feedback-card">
                <h3 class="result-subtitle">테스트 결과 피드백</h3>
                <img style="margin: 52px 0;" class="result-image" src="@/assets/result_servey.png" alt="light bulb">
                <p class="result-feedback-text">{{ result.feedback }}</p>
              </div>
            </div>
            <div class="result-level">
              <div class="result-feedback-card">
                <h3 class="result-subtitle">추천 학습 방향</h3>
                <img style="margin: 52px 0;" class="result-image" src="@/assets/result_newbulb.png" alt="magnifier">
                <p class="result-feedback-text">{{ result.recommendation_direction }}</p>
              </div>
            </div>
          </div>
  
        </section>
  
      </div>
    </div>
    <div class="result-container outro-container">
      <div class="outro-wrapper">
        <h2 class="outro-title">이제 AI가 당신에게 맞는 책을 추천해드릴게요</h2>
        <button class="outro-button" @click="getRecommendations">추천 받기</button>
      </div>
    </div>
  </div>
  
  <Teleport to="body">
  <div v-if="showModal">
    <div class="modal-overlay"></div>

      <div class="modal-container"><button class="modal-close" @click="showModal = false">×</button>
        <div class="modal-title">문해력 수준 자세히 알아보기</div>
        <img class="modal-image" src="@/assets/level_table.png" alt="level table">
      <div class="modal-subtitle">*해당 기준표는 ‘국가문해교욱센터’의 문해력 수준을 기반으로 재구성한 정보입니다.</div>

    </div>
  </div>
  </Teleport>
</template>

<script setup>
  import axios from 'axios'
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useTestResultStore } from '@/stores/testResultStore'

  const router = useRouter()
  const testResultStore = useTestResultStore()
  const result = testResultStore.result
  const answersMap = testResultStore.answersMap

  const correctCount = computed(() => {
    let count = 0
    for (const stageKey in testResultStore.answersMap) {
      for (const entry of testResultStore.answersMap[stageKey]) {
        if (entry.is_correct) count++
      }
    }
    return count
  })

  const showModal = ref(false)

  const userName = ref('')
  userName.value = (result.userName ? result.userName : '사용자')

  // API 요청 함수
  const getRecommendations = () => {      
    router.push('/books/recommend')
  }

  onMounted(() => {
    if (!result || Object.keys(answersMap).length === 0) {
      router.back()
    }
  })

  // 템플릿에서 사용할 함수들을 노출 (필요한 경우)
  defineExpose({
    getRecommendations,
  })
</script>

<style scoped>
  .page-scroll-wrapper {
    height: 100vh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
  }

  .result-container {
    display: flex;
    justify-content: center;
    position: relative;
    align-items: end;
    width: 1920px;
    height: 1080px;
    background-color: #B8BC7F;
    box-sizing: border-box;
    scroll-snap-align: center;
  }

  /* 첫 번째 페이지 - 결과 */
  .result-wrapper-1 {
    width: 100%;
    height: 88%;
    background: #FEFFE9;
    border-radius: 30px 30px 0 0;
    margin: 0 128px;
  }

  .result-title {
    text-align: center;
    font-size: 48px;
    font-weight: 600;
    margin: 100px 0;
    padding: 0;
  }

  .result-page {
    margin: 0 280px;
  }

  .result-info {
    display: flex;
    justify-content: space-between;
    align-items: start;
  }

  .result-card {
    width: 400px;
    height: 400px;
    text-align: center;
    padding: 44px;
    margin-top: 60px;
    border-radius: 24px;
    border: 1px solid #818b7e3b;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
  }

  .result-image {
    width: 160px;
    height: 160px;
  }

  .result-subtitle {
    font-weight: 500;
    margin: 0;
  }

  .result-total {
    color: #818B7E;
    margin: 20px 0 8px;
  }

  .result-yours {
    font-size: 40px;
    font-weight: 600;
    margin: 0;
  }

  .cross-line {
    width: 0;
    height: 560px;
    border-left: 1px solid #818B7E;
    opacity: 0.2;
  }

  .result-modal {
    padding-top: 32px;
    display: flex;
    justify-content: center;
    position: inherit;
    transform: translateX(4px);
  }

  .result-modal-text {
    color: #818B7E;
  }

  .result-modal-text:hover {
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
    transform: translateX(4px);
  }
    

  /* 두 번째 페이지 - 오답 */
  .result-wrapper-2 {
    width: 100%;
    height: 100%;
    background: #FEFFE9;
    margin: 0 128px;
  }

  .problem-page {
    margin: 0 100px;
  }

  .result-problem-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 640px;
    padding: 80px;
    border-radius: 40px;
    background-color: #E5E8BC;
  }

  .result-problem {
    display: flex;
    text-align: center;
    width: 480px;
  }

  .result-problem-image {
    max-width: 480px;
    border-radius: 24px;
  }

  .result-questions {
    width: 700px;
  }

  .result-options {
    width: 100%;
    margin: 0;
  }

  .result-options-title {
    font-size: 20px;
    font-weight: 600;
    margin: 0;
    padding: 0 32px;
  }

  .result-options-text {
    font-size: 16px;
    margin: 4px 0 16px;
    padding: 0 0 0 52px;
  }

  .result-answer {
    width: 100;
    display: flex;
    justify-content: center;
    border-radius: 16px;
    background-color: #818B7E;
    margin: 40px 0 0;

  }

  .result-answer-text {
    color: #ffffff;
    font-size: 20px;
    padding: 16px 0;
    margin: 0;
  }


  /* 세 번째 페이지 - 피드백 */
  .result-wrapper-3 {
    width: 100%;
    height: 100%;
    background: #ffffff;
    margin: 0 128px;
  }

  .result-feedback-card {
    width: 472px;
    height: 600px;
    text-align: center;
    padding: 80px 44px;
    border-radius: 24px;
    background-color: #FEFFE9;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .result-feedback-text {
    font-size: 20px;
    text-align: justify;
  }


  /* 추가 페이지 */
  .outro-container {
    background-color: #B8BC7F;
    display: flex;
    justify-content: center;
    align-items: start;
    height: 560px;
  }

  .outro-wrapper {
    background-color: #818B7E;
    margin: 0 128px;
    padding: 128px 0;
    height: 80%;
    width: 100%;
    border-radius: 0 0 30px 30px;
    text-align: center;
  }

  .outro-title {
    color: #FEFFE9;
    font-size: 36px;
    font-weight: 500;
    margin-bottom: 80px;
    letter-spacing: 4px;
  }

  .outro-button {
    padding: 20px 80px;
    font-size: 20px;
    border-radius: 50px;
    background-color: #FEFFE9;
    color: #818B7E;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    text-decoration: none;
  }

  .outro-button:hover:not(:disabled) {
    background: #E5E8BC;
    color: #454E42;
    transform: translateY(-2px);
  }


  /* 모달 - 문해력 수준 */
  .modal-overlay{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(129, 139, 126, 0.5);
    z-index: 999;
  }

  .modal-container{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 780px;
    height: 560px;
    background-color: #ffffff;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    z-index: 1000;

    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: transparent;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #818B7E;
  }

  .modal-close:hover {
    color: #454E42;
  }

  .modal-title{
    font-size: 24px;
    font-weight: 500;
    color: #000000;
    line-height: 1.2;
    margin-bottom: 12px;
    padding: 0;
  }

  .modal-image{
    width: 640px;
  }

  .modal-subtitle{
    font-size: 14px;
    font-weight: 300;
    color: #818B7E;
    margin: 0;
    padding-top: 0px;
  }

  .modal-label{
    font-size: 14px;
    color: #454E42;
    text-align: left;
    margin-bottom: 4px;
  }

  .modal-input{
    border: 1px solid #454E42;
    width: 100%;
    height: 56px;
    padding: 0 12px;
    border-radius: 12px;
    font-size: 14px;
    color: #454E42;
    box-sizing: border-box;
    margin-bottom: 52px;
  }

  .modal-button-group{
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-top: 12px;
  }

  .modal-button {
    padding: 12px 0;
    width: 140px;
    height: 52px;
    font-size: 18px;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
    display: inline-block;
    text-align: center;
  }

  .modal-button.confirm {
    background-color: #818B7E;
    color: white;
    border: none;
  }

  .modal-button.cancel {
    background-color: white;
    border: 1px solid #454E42;
    color: #454E42;
  }
</style>