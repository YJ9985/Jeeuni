<template>
  <main>
    <div class="recommend-container">
      <div class="recommend-wrapper">
        <section class="recommend-left" v-if="recommendations && recommendations.length">
          <h3 class="recommend-left-title">{{ currentRecommendation.reason }}</h3>
          <div class="recommend-info">
            <button :disabled="currentIndex < 1" @click="previousRecommendation" class="nav-button"> < </button>
            <div class="recommend-book-wrapper">
              <div class="circle-outline circle-1"></div>
              <div class="circle-outline circle-2"></div>
              <div class="circle-outline circle-3"></div>

              <div class="recommend-book">
                <h3 class="recommend-book-title">{{ currentRecommendation.title }}</h3>
                <p class="recommend-book-description">{{ currentRecommendation.description }}</p>
              </div>
            </div>
            <button :disabled="currentIndex >= recommendations.length - 1" @click="nextRecommendation" class="nav-button"> > </button>
          </div>
          <div class="recommend-tip">
            <h3 class="recommend-tip-title">Reading Tip</h3>
            <div class="recommend-line"></div>
            <p class="recommend-tip-text">{{ currentRecommendation.reading_tip }}</p>
          </div>

          <div class="recommend-indicators">
            <span
              v-for="(item, index) in recommendations"
              :key="index"
              :class="['indicator-dot', { active: currentIndex === index }]"
            ></span>
          </div>
        </section>

        <section class="recommend-right" v-if="recommendations && recommendations.length">
          <h2 class="recommend-content-title">지금의 당신을 위한, 가장 필요한 책 리스트</h2>
          <p class="recommend-content-text">
            이해력과 사고력 향상에 중점을 둔 개인 맞춤형 추천입니다.<br>
            읽는 만큼 여러분의 독서 근육이 성장할 거예요!
          </p>
        </section>

        <div v-else-if="loading" class="loading status-loading">
          <div class="spinner"></div>
          <p>추천할 도서를 선정하는 중</p>
        </div>
  
        <div v-else-if="error" class="error status-error">
          <p>{{ error }}</p>
          <button @click="getRecommendations" class="retry-button">다시 시도</button>
        </div>
  
        <div v-else class="no-data status-overlay">
          <p>추천할 도서 정보가 없습니다.</p>
          <button @click="getRecommendations" class="retry-button">새로고침</button>
        </div>
      </div>

      <button class="back-button" @click="router.back()">← 결과로 돌아가기</button>
    </div>
    
  </main>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'

  import { useRouter } from 'vue-router'
  import { useTestResultStore } from '@/stores/testResultStore'

  const router = useRouter()
  const testResultStore = useTestResultStore()
  const answersMap = testResultStore.answersMap
  
  const recommendations = ref([])

  const currentIndex = ref(0)
  const loading = ref(true)
  const error = ref(null)

  console.log(recommendations)
  console.log(recommendations.value)
  
  // 계산된 속성
  const currentRecommendation = computed(() => {
    return recommendations.value[currentIndex.value] || null
  })

  // API 요청 함수
  const getRecommendations = async () => {
    loading.value = true
    error.value = null
    console.log(answersMap)

    if (!answersMap || Object.keys(answersMap).length === 0) {
      error.value = '답안 정보가 없어 도서를 추천할 수 없습니다.'
      loading.value = false
      return
    }

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/v2/books/recommend/',
        { 'test_result': answersMap },
        { headers: { 'Content-Type': 'application/json' } }
      )
      recommendations.value = response.data.recommendations
    } catch (err) {
      console.error('도서를 추천 받는데 실패했습니다:', err)
      error.value = '도서를 추천 받는데 실패했습니다.\n서버를 확인해주세요.'
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    getRecommendations()
  })

  // 네비게이션 함수들
  const nextRecommendation = () => {
    if (currentIndex.value < recommendations.value.length - 1) {
      currentIndex.value++
    }
  }

  const previousRecommendation = () => {
    if (currentIndex.value > 0) {
      currentIndex.value--
    }
  }
</script>

<style scoped>
  .recommend-container {
    position: relative;
    display: flex;
    justify-content: center;
    width: 1920px;
    height: 1080px;
    background-color: #818B7E;
    box-sizing: border-box;
    overflow: hidden;
  }

  .recommend-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 1560px;
    margin: 128px 0 128px;
  }

  .recommend-left {
    width: 600px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 60px;
  }

  .recommend-left-title {
    text-align: center;
    color: #FEFFE9;
    font-size: 32px;
    font-weight: 400;
    margin: 0;
  }

  .recommend-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 28px;
  }

  .recommend-book-wrapper {
    position: relative;
    width: 400px;
    height: 400px;
  }

  .circle-outline {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.2);
    z-index: 0;
  }

  .circle-1 {
    width: 320px;
    height: 320px;
    top: 100px;
    right: -20px;
  }

  .circle-2 {
    width: 360px;
    height: 360px;
    top: 16px;
    left: -32px;
  }

  .circle-3 {
    width: 412px;
    height: 412px;
    top: -20px;
    left: -5px;
  }

  .recommend-book {
    position: relative;
    z-index: 1;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background-color: #DBDFAD;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 8px;
  }

  .recommend-book-title {
    text-align: center;
    color: #454E42;
    font-weight: 700;
    margin: 0;
  }

  .recommend-book-description {
    text-align: center;
    color: #454E42;
    font-weight: 400;
    font-size: 20px;
    margin: 0;
  }

  .nav-button {
    width: 40px;
    height: 80px;
    border-radius: 50%;
    border: 0;
    margin: 0 12px;
    background-color: #ffffff00;
    color: #ffffff;
    text-align: center;
    font-weight: 600;
    font-size: 40px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .nav-button:hover:not(:disabled) {
    color: white;
    transform: translateY(-2px);
  }

  .nav-button:disabled {
    color: #ffffff1e;
    transform: none;
    box-shadow: none;
  }

  .recommend-tip {
    width: 400px;
  }

  .recommend-tip-title {
    color: #FEFFE9;
    text-align: left;
    font-weight: 400;
    margin: 0;
  }

  .recommend-line {
    height: 1px;
    background-color: #FEFFE9;
    border-radius: 2px;
    margin: 16px 0;
  }

  .recommend-tip-text {
    color: #FEFFE9;
    text-align: right;
    font-weight: 300;
    font-size: 20px;
    margin: 0;
  }

  .recommend-indicators {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 0;
  }

  .indicator-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #ffffff4d;
    transition: background-color 0.3s;
  }

  .indicator-dot.active {
    background-color: #FEFFE9;
  }

  .recommend-right {
    display: flex;
    flex-direction: column;
    text-align: right;
    gap: 40px;
  }

  .recommend-content-title {
    color: #FEFFE9;
    text-align: right;
    font-weight: 500;
    font-size: 44px;
    margin: 0;
  }

  .recommend-content-text {
    text-align: right;
    font-weight: 300;
    font-size: 20px;
    color: #454E42;
    margin: 0;
  }

  /* 추가 기능 */
  .loading {
    background-color: #ffffff00;
    text-align: center;
    padding: 60px;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #454E42;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 32px;
  }

  .loading p {
    font-size: 20px;
    color: #fff;
    margin: 0;
  }

  .error, .no-data {
    text-align: center;
    padding: 60px;
    /* margin: 500px 0; */
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .error p, .no-data p {
    color: #dc3545;
    font-size: 18px;
    margin-bottom: 20px;
    white-space: pre-line;
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

  .status-error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 60px;
    text-align: center;
    z-index: 10;
    width: 500px;
  }

  .status-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 60px;
    text-align: center;
    z-index: 10;
    width: 500px;
  }

  .back-button {
    position: absolute;
    bottom: 180px;
    right: 212px;
    background-color: #ffffff00;
    color: #e6e6d6;
    border: none;
    font-size: 20px;
    font-weight: 500;
    cursor: pointer;
    z-index: 20;
    transition: background-color 0.3s, transform 0.2s;
  }

  .back-button:hover {
    color: #FEFFE9;
    transform: translateY(-2px);
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>