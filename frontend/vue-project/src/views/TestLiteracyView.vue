<template>
  <main>
    <div class="test-container">
      <div class="test-wrapper" v-if="currentQuestion">
        <section class="test-question">
          <div class="test-level-badge">Level {{ currentQuestion.level }}</div>
          <h1 class="test-question-text">{{ currentQuestion.id }}. {{ currentQuestion.question }}</h1>
          <div class="test-line"></div>
        </section>

        <section class="test-content" v-if="shouldShowContent()">
          <p class="test-content-text" v-if="currentQuestion.content">
            {{ currentQuestion.content }}
          </p>
          <img 
            class="test-content-image" 
            v-if="currentQuestion.img_content"
            :src="`/literacy_tests/${currentQuestion.img_content.split('/').pop()}`"
            :alt="currentQuestion.question"
          />
        </section>

        <section class="test-choices" v-if="shouldShowChoices()">
          <div class="test-choices-text">
            <div 
              v-for="(choice, index) in currentQuestion.choices" 
              :key="index"
              class="choice-item"
              @click="selectChoice(index + 1)"
              :class="{ 'selected': selectedChoice === index + 1 }"
            >
              <p class="choice-circle">○</p>
              <p class="choice-text">
                <!-- {{ index + 1 }}. -->
                {{ choice }}
              </p>
              
            </div>
          </div>
        </section>

        <!-- 네비게이션 버튼 -->
        <section class="test-navigation">
          <button 
            @click="previousQuestion" 
            :disabled="currentIndex === 0"
            class="nav-button"
          >
            이전
          </button>
          <span class="question-counter">
            {{ currentIndex + 1 }} / {{ questions.length }}
          </span>

          <!-- 다음 버튼 (마지막 문제가 아닐 때만 표시) -->
          <button 
            v-if="currentIndex < questions.length - 1"
            @click="nextQuestion"
            :disabled="answers[currentQuestion.id] === undefined"
            class="nav-button"
          >
            다음
          </button>

          <!-- 제출 버튼 (마지막 문제일 때만 표시 + 정답이 15개 이상일 때 활성화) -->
          <button 
            v-else
            @click="submitAnswers"
            :disabled="Object.keys(answers).length < 15"
            class="submit-button"
          >
            제출
          </button>
        </section>
      </div>

      <!-- 로딩 상태 -->
      <div v-else-if="loading" class="loading">
        <div class="spinner"></div>
        <p>데이터를 불러오는 중...</p>
      </div>

      <!-- 에러 상태 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="fetchQuestions" class="retry-button">다시 시도</button>
      </div>

      <!-- 데이터 없음 -->
      <div v-else class="no-data">
        <p>문제 데이터가 없습니다.</p>
        <button @click="fetchQuestions" class="retry-button">새로고침</button>
      </div>
    </div>
  </main>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'

  import { useRouter } from 'vue-router'
  import { useAccountStore  } from '@/stores/accounts'
  import { useTestResultStore } from '@/stores/testResultStore'

  const router = useRouter()
  const testResultStore = useTestResultStore()
  const accountStore = useAccountStore()
  const isLogin = computed(() => accountStore.isLogin)

  // 반응형 데이터
  const questions = ref([])
  const currentIndex = ref(0)
  const selectedChoice = ref(null)
  const answers = ref({})
  const answersMap = ref({})
  const results = ref({})
  const loading = ref(true)
  const error = ref(null)

  // 계산된 속성
  const currentQuestion = computed(() => {
    return questions.value[currentIndex.value] || null
  })

  // API 요청 함수
  const fetchQuestions = async () => {
    try {
      loading.value = true
      // Django API에서 모든 문제 가져오기 (올바른 URL 사용)
      const response = await axios.get('http://127.0.0.1:8000/api/v2/literacy/test/')
      questions.value = response.data
      
      // 첫 번째 문제의 답안 불러오기
      loadCurrentAnswer()
    } catch (err) {
      console.error('문제를 불러오는데 실패했습니다:', err)
      error.value = '문제를 불러오는데 실패했습니다.\n서버를 확인해주세요.'
    } finally {
      loading.value = false
    }
  }

  // 선택지 관련 함수들
  const selectChoice = (choiceIndex) => {
    selectedChoice.value = choiceIndex
    // 현재 문제의 답안 저장
    if (currentQuestion.value) {
      const questionId = currentQuestion.value.id
      const level = currentQuestion.value.level
      const answer = currentQuestion.value.answer
      const stageKey = `stage_${level}`

      answers.value[questionId] = choiceIndex

      if (!answersMap.value[stageKey]) {
        answersMap.value[stageKey] = []
      }

      const existingIndex = answersMap.value[stageKey].findIndex(
        (entry) => entry.question_id === questionId
      )

      const newEntry = {
        question_id: questionId,
        is_correct: answer === choiceIndex
      }

      if (existingIndex !== -1) {
        answersMap.value[stageKey][existingIndex] = newEntry
      } else {
        answersMap.value[stageKey].push(newEntry)
      }
    }
  }

  // 네비게이션 함수들
  const nextQuestion = () => {
    if (currentIndex.value < questions.value.length - 1) {
      currentIndex.value++
      loadCurrentAnswer()
    }
  }

  const previousQuestion = () => {
    if (currentIndex.value > 0) {
      currentIndex.value--
      loadCurrentAnswer()
    }
  }

  const loadCurrentAnswer = () => {
    // 현재 문제에 대한 기존 답안이 있으면 불러오기
    if (currentQuestion.value && answers.value[currentQuestion.value.id] !== undefined) {
      selectedChoice.value = answers.value[currentQuestion.value.id]
    } else {
      selectedChoice.value = null
    }
  }

  // 조건부 렌더링을 위한 함수들
  const shouldShowContent = () => {
    return currentQuestion.value && (currentQuestion.value.content || currentQuestion.value.img_content)
  }

  const shouldShowChoices = () => {
    return currentQuestion.value && currentQuestion.value.choices && currentQuestion.value.choices.length > 0
  }

  // 답안 제출
  const submitAnswers = async () => {
    try {
      loading.value = true
      const response = await axios.post(
        'http://127.0.0.1:8000/api/v2/literacy/evaluate/',
        answersMap.value,
        {headers: {'Content-Type': 'application/json'}}
      )
      testResultStore.setResult(response.data)
      testResultStore.setAnswersMap(answersMap.value)

      router.push('/test/literacy/result')
      
    } catch (error) {
      console.error('제출 중 오류 발생:', error)
    } finally {
      loading.value = false
    }
  }

  // 컴포넌트 마운트 시 실행
  onMounted(async () => {
    // 로그인 상태 체크
    if (!isLogin) {
      router.push('/accounts/login')
      return
    }

    // 로그인되어 있다면 문제 가져오기
    fetchQuestions()
  })

  // 템플릿에서 사용할 함수들을 노출 (필요한 경우)
  defineExpose({
    fetchQuestions,
    submitAnswers
  })
</script>

<style scoped>
  .test-container {
    display: flex;
    justify-content: center;
    width: 100%;
    height: auto;
    background-color: #FEFFE9;
    box-sizing: border-box;
    overflow: hidden;
  }

  .test-wrapper {
    width: 960px;
    background: #ffffff;
    border-radius: 12px;
    padding: 68px;
    margin: 128px auto 128px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .test-question {
    position: relative;
  }

  .test-level-badge {
    display: inline-block;
    background: linear-gradient(45deg, #458f00, #1b5c07);
    /* background: #818B7E; */
    color: white;
    padding: 6px 16px;
    border-radius: 24px;
    font-size: 16px;
    font-weight: 600;
  }

  .test-question-text {
    font-size: 28px;
    font-weight: 700;
    color: #333;
    padding: 0 24px;
    margin: 36px 0;
  }

  .test-line {
    height: 3px;
    background: linear-gradient(90deg, #458f00, #1b5c07);
    border-radius: 2px;
  }

  .test-content {
    margin: 36px 0;
    /* display: flex;
    justify-content: center; */
  }

  .test-content-text {
    font-size: 24px;
    text-align: justify;
    line-height: 1.7;
    padding: 0 24px;
    margin: 36px 0;
    color: #555;
    white-space: pre-line;
  }

  .test-content-image {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 36px 0;
    padding: 0 20px;
  }

  .test-choices {
    margin: 36px 0;
    padding: 0 20px;
  }

  .choice-item {
    display: flex;
    align-items: center;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 20px;
    line-height: 1.5;
  }

  .choice-item:hover {
    border-color: #458f00;
    background-color: #fafdf7;
    transform: translateX(4px);
  }

  .choice-item.selected {
    border: 1px solid #333;
    /* background: linear-gradient(135deg, #458f00, #1b5c07); */
    background: #1b5c07;
    color: #fafdf7;
    font-weight: 600;
    transform: translateX(4px);
    box-shadow: 0 4px 12px #e0e0e0;
  }

  .choice-circle {
    margin-bottom: 0px;
    margin-right: 20px;
  }

  .choice-text {
    margin: 0;
  }

  .test-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
    padding: 40px 20px 0;
    border-top: 2px solid #f0f0f0;
  }

  .nav-button {
    padding: 12px 28px;
    border: 2px solid #458f00;
    background: white;
    color: #458f00;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 600;
    font-size: 16px;
  }

  .nav-button:hover:not(:disabled) {
    background: #458f00;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px #e0e0e0;
  }

  .nav-button:disabled {
    border-color: #ccc;
    color: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .question-counter {
    font-weight: bold;
    color: #666;
    font-size: 18px;
    background: #f8f9fa;
    padding: 8px 16px;
    border-radius: 20px;
  }

  .test-submit {
    text-align: center;
    padding-top: 25px;
    border-top: 2px solid #f0f0f0;
  }

  .submit-button {
    padding: 12px 28px;
    border: 2px solid #458f00;
    background: white;
    color: #458f00;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 600;
    font-size: 16px;

    /* background: linear-gradient(45deg, #28a745, #20c997);
    color: white;
    border: none;
    padding: 15px 40px;
    margin-top: 30px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease; */
  }

  .submit-button:disabled {
    border-color: #ccc;
    color: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .submit-button:hover:not(:disabled) {
    background: #458f00;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
  }

  .loading {
    margin: 500px 0;
    text-align: center;
    padding: 60px;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #458f00;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
  }

  .loading p {
    font-size: 18px;
    color: #458f00;
    margin: 0;
  }

  .error, .no-data {
    text-align: center;
    white-space: pre;
    padding: 60px;
    margin: 500px 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .error p, .no-data p {
    color: #dc3545;
    font-size: 18px;
    margin-bottom: 20px;
  }

  .retry-button {
    background: #dc3545;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s ease;
  }

  .retry-button:hover {
    background: #c82333;
    transform: translateY(-2px);
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .test-container {
      min-width: 720px;
    }
    /* .test-wrapper {
      width: 960px;
      background: #ffffff;
      border-radius: 12px;
      padding: 68px;
      margin: 128px auto 128px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    } */
      
    .test-wrapper {
      padding: 68px;
      margin: 128px 24px ;
    }
    
    .test-question-text {
      font-size: 20px;
    }
    
    .test-content-text {
      font-size: 20px;
    }
  }
</style>