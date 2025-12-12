<template>
  <div class="home-container">
    <section class="page-section section1">
      <div class="screen">
        <div class="screen-image">
          <img src="@/assets/home-image.png" alt="HomeImage">
        </div>
        <div class="overlap"></div>
        <div class="text-items">
          <div class="p">당신의 독서가 어렵게 느껴졌던 이유,</div>
          <div class="headline">
            <span class="logo">JEEUN-I</span>
            <span class="p2">를 통해</span>
          </div>
          <div class="p3">지금의 문해력 수준에 꼭 맞는 책을 추천받고 이해력과 사고력을 함께 키워보세요.</div>
           <button class="animated-button" @click="goToTest">
              <svg xmlns="http://www.w3.org/2000/svg" class="arr-2" viewBox="0 0 24 24">
                <path d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"/>
              </svg>
              <span class="text">지금 테스트하기</span>
              <span class="circle"></span>
              <svg xmlns="http://www.w3.org/2000/svg" class="arr-1" viewBox="0 0 24 24">
                <path d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"/>
              </svg>
           </button>
        </div>
      </div>
    </section>

    <section class="page-section section2">
       <div class="second-header">
        <div class="header-text">Wherever You are,</div>
        <div class="header-text2">Books will lead you</div>
       </div>
       <div class="second-image">
        <img class="img" src="@/assets/books.jpg" alt="BooksPath">
       </div>
    </section>

    <section class="page-section section3">
      <div class="sec3-container">
        <div class="sec3p1">
          <p>Literacy that broadens your thinking,</p>
          <p>A reading recommendation platform that connects books and you.</p>
          <p>At Jeeun-i, your journey of reading begins —</p>
          <p>one that strengthens your thoughts and deepens your emotions.</p>
        </div>
        <div class="sec3p2">
          <p>생각의 폭을 넓히는 문해력, 책과 나를 이어주는 독서 추천 플랫폼.</p>
          <p>지은이에서 당신의 생각을 더 단단하게,</p>  
          <p>당신의 감정을 더 넓게 만드는 독서가 시작됩니다.</p>
        </div>
      </div>
    </section>

    <section class="page-section section4">
      <div class="page-wrapper">

        <!-- 메뉴 -->
        <div class="menu-container">
          <div
            v-for="(label, idx) in ['베스트 셀러','신착 도서','JE\'s PICK']"
            :key="idx"
            class="menu-item"
            :class="{ active: selected===idx }"
            @click="onSelect(idx)"
          >{{ label }}</div>
        </div>
        <div class="menu-line"></div>
  
        <!-- 단일 이미지 슬라이더 -->
        <div class="book-display">
  
          <!-- 화면 왼쪽의 도서 정보 패널 -->
          <div class="info-panel" v-if="visibleBooks.length">
            <h3 class="title">{{ currentBook.title }}</h3>
            <p class="author">{{ currentBook.author }}</p>
            <p class="desc">{{ currentBook.description }}</p>
            <button class="learn-more" @click="goDetail(currentBook.id)">
              <span class="circle" aria-hidden="true">
                <span class="icon arrow"></span>
              </span>
              <span class="button-text">Learn More</span>
            </button>
          </div>
  
          <!-- 화면 오른쪽의 단일 책 이미지 -->
          <div class="book-image-container" v-if="visibleBooks.length">
            <div class="book-card">
              <img 
                :src="currentBook.cover" 
                class="cover" 
                :alt="currentBook.title"
                :key="currentIndex"
              />
            </div>
          </div>
        </div>
  
        <p v-if="!visibleBooks.length" class="no-book">해당 카테고리의 도서가 없습니다.</p>
      </div>
    </section>
    
    <section class="page-section section5">
      <!-- 다섯 번째 섹션 내용 -->
      <div class="outro">
        <div class="outro-left">
          <h3>Jeeun-i</h3>
          <p>Made by Yeji, YeaEun</p>
        </div>
        <div class="outro-right">
          <a>Subscribe Our Story</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const selected = ref(0)
const allBooks = ref([])
const currentIndex = ref(0)
const API_BASE = import.meta.env.VITE_API_BASE_URL
let timer = null

function goToTest() {
  if (accountStore.isLogin) {
    router.push({ name: 'TestRecommendView' })
  } else {
    router.push({ name: 'LogInView' })
  }
}

// 1) 메뉴 클릭
function onSelect(idx){
  selected.value = idx
  currentIndex.value = 0
}

// 2) API 로드
onMounted(async ()=>{
  try {
    const res = await axios.get(`${API_BASE}/api/v1/books/`)
    allBooks.value = res.data
  } catch (error) {
    console.error('Failed to load books:', error)
  }
})

onUnmounted(()=> {
  if (timer) {
    clearInterval(timer)
  }
})

// 3) 메뉴별 필터된 리스트
const visibleBooks = computed(()=>{
  const list = allBooks.value
  if(selected.value===0) return list.filter(b=>b.is_bestseller)
  if(selected.value===1) return list.filter(b=>b.is_new)
  if(selected.value===2) return list.filter(b=>b.is_J_recommended)
  return []
})

// 4) 현재 보여줄 책 정보
const currentBook = computed(() => {
  if (!visibleBooks.value.length) return {}
  return visibleBooks.value[currentIndex.value]
})

// 5) 자동 슬라이드 로직
watch(visibleBooks, (newBooks) => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  
  if (!newBooks.length) return
  
  currentIndex.value = 0
  
  timer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % newBooks.length
  }, 3000)
}, { immediate: true })

// 6) 특정 인덱스로 이동
function goToIndex(idx) {
  currentIndex.value = idx
  // 타이머 리셋
  if (timer) {
    clearInterval(timer)
    timer = setInterval(() => {
      currentIndex.value = (currentIndex.value + 1) % visibleBooks.value.length
    }, 3000)
  }
}

// 7) 디테일 이동
function goDetail(id){
  router.push({ name:'BookDetailView', params:{ id } })
}
</script>

<style scoped>
.home-container {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  overflow-x: hidden;
}

.page-section {
  scroll-snap-align: start;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 첫 번째 섹션 */
.section1 {
  position: relative;
  background: #C0C7BE;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 0;
}

.screen {
  position: relative;
  width: 100%;
  height: 95vh;
  overflow: hidden;
  margin: 0;
}

.screen-image {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.screen-image img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

.overlap {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(119, 120, 105, 0.43);
  pointer-events: none;
  z-index: 5;
}

.text-items {
  position: absolute;
  left: 12.8vw;
  top: 25.7vh;
  z-index: 999;
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.text-items > * {
  margin: 0;
  padding: 0;
}

.text-items .p {
  font-size: 1.4vw;
  color: #C0C7BE;
  margin-bottom: 0.5vh;
  margin-left: 1.8vh;
}

.headline {
  display: flex;
  align-items: baseline;
  gap: 1.5vw;
  margin-bottom: 2.5vh;
}

.headline .logo {
  font-family: "Rozha One", sans-serif;
  font-size: 6.5vw;
  color: #FEFFE9;
  margin: 0;
}

.headline .p2 {
  font-size: 2vw;
  color: #FEFFE9;
  margin: 0;
}

.text-items .p3 {
  font-size: 2.0vw;
  font-weight: 500;
  color: #FEFFE9;
  margin-bottom: 4vh;
}

.animated-button {
  position: relative;
  display: flex;
  align-items: center;
  align-self: flex-start;
  padding: 12px 36px;
  border: 2px solid transparent;
  border-radius: 100px;
  background-color: #454E42;
  color: #ffffff;
  font-size: 16px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  text-decoration: none;
}

.animated-button .text {
  position: relative;
  z-index: 1;
  transform: translateX(-12px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button svg {
  position: absolute;
  width: 24px;
  fill: #ffffff;
  z-index: 9;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button .arr-1 { right: 16px; }
.animated-button .arr-2 { left: -25%; }

.animated-button .circle {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 20px; 
  height: 20px;
  background-color: #FEFFE9;
  border-radius: 50%;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

/* Hover & Active 상태 */
.animated-button:hover {
  box-shadow: 0 0 0 12px transparent;
  color: #454E42;
  border-radius: 12px;
}

.animated-button:hover .arr-1 { right: -25%; }
.animated-button:hover .arr-2 { left: 16px; }
.animated-button:hover .text { transform: translateX(12px); }
.animated-button:hover svg { fill: #454E42; }
.animated-button:hover .circle {
  width: 220px; height: 220px;
  opacity: 1;
}

.animated-button:active {
  transform: scale(0.95);
  box-shadow: 0 0 0 4px #B8BC7F;
}

/* 두 번째 섹션 */
.section2 {
  background: #C0C7BE;
  position: relative;
  overflow: visible; 
}

.second-header {
  position: absolute;
  top: 23vw;
  left: 50vw;
  transform: translate(-50%, -100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
}

.second-header .header-text {
  font-size: 3.5vw;
  font-weight: 700;
  margin-bottom: 1.5vw;
}

.second-header .header-text2 {
  font-size: 4vw;
  font-weight: 700; 
}

.second-image {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%);
  width: 35vw;
  height: 90vh;
  border-radius: 30vw;
  overflow: hidden;
  z-index: 1;
}

.second-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 세 번째 섹션 */
.section3 { 
  background: #C0C7BE;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5vh 2vw; 
}

.sec3-container {
  max-width: 800px;
  width: 90%;
  text-align: center;
  margin-top: 35vh;
}

.sec3-container p {
  margin: 0;
  padding: 0;
  line-height: 1.4;
}

.sec3p1{
  margin: 0;
  line-height: 1;
  font-size: 1.8vw;
  font-weight: 200;
  color: #1a1a1a;
}

.sec3p2 {
  margin-top: 4vh;
}

.sec3p2 p {
  font-size: 1.4vw;
  font-weight: 100;
  color: #1a1a1a;
}

/* 네 번째 섹션 */
.section4 { 
  position: relative;
  background: #ffffff;
  padding-bottom: 50px;
}

.page-wrapper {
  padding: 128px 0;
  height: 800px;
  width: 1200px;
  display: flex;
  justify-content: left;
  flex-direction: column;
}

.menu-container {
  width: 100;
  display: flex;
  gap: 2vw;
  justify-content: flex-start;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 40px;
  /* border-radius: 8px; */
  /* background-color: #C0C7BE; */
  font-size: 20px;
  font-weight: 300;
  cursor: pointer;
  transition: background-color 0.3s;
  color: #000000;
}

.menu-item.active {
  background-color: #818B7E;
  color: white;
  font-weight: 300;
}

.menu-item:hover {
  background-color: #c1cabe;
  color: #444444;
  transform: translateY(-1px);
}

.menu-line {
  width: 100vw;
  margin-top: 24px;
  border-bottom: 3px solid #C0C7BE;
}

/* 새로운 book-display 레이아웃 */
.book-display {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 5vw;
  width: 100;
  height: 43vh;
  position: relative;
  margin-top: 52px;
  background-color: rgba(211, 211, 211, 0.1);
}

/* 책 이미지 컨테이너 */
.book-image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  order: 2;
}

/* 메인 책 카드 */
.book-card {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.cover {
  width: 28vh;
  height: 40vh;
  object-fit: cover;
  margin: 1.3vh 2vw;
  /* border-radius: 12px; */
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-panel {
  flex: 0 0 25vw;
  order: 1;
  padding: 2vw;
  box-sizing: border-box;
  border-radius: 12px;
  align-self: flex-end;
}

.info-panel .title { 
  font-size: 1.3em; 
  margin: 0 0 0.5em; 
  font-weight: 600;
  color: #333;
}

.info-panel .author { 
  margin: 0 0 1em; 
  color: #666; 
  font-size: 1em;
}

.info-panel .desc { 
  font-size: 0.8em; 
  line-height: 1.4; 
  color: #444; 
  margin-bottom: 1.5em;
}

button {
  position: relative;
  display: inline-block;
  cursor: pointer;
  outline: none;
  border: 0;
  vertical-align: middle;
  text-decoration: none;
  background: transparent;
  padding: 0;
  font-size: inherit;
  font-family: inherit;
}

button.learn-more {
  width: 11rem;
  height: auto;
}

button.learn-more .circle {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: relative;
  display: block;
  margin: 0;
  width: 2.5rem;
  height: 2.5rem;
  background: #282936;
  border-radius: 1.625rem;
}

button.learn-more .circle .icon {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
  background: #fff;
}

button.learn-more .circle .icon.arrow {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  left: calc((2rem - 1rem) / 2);
  width: 1rem;
  height: 0.125rem;
  background: none;
}

button.learn-more .circle .icon.arrow::before {
  position: absolute;
  content: "";
  top: -0.29rem;
  right: 0.0625rem;
  width: 0.625rem;
  height: 0.625rem;
  border-top: 0.125rem solid #fff;
  border-right: 0.125rem solid #fff;
  transform: rotate(45deg);
}

button.learn-more .button-text {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 0.5rem 0;
  margin: 0 0 0 2.5rem;
  color: #282936;
  font-weight: 600;
  line-height: 1.6;
  text-align: center;
  text-transform: uppercase;
}

button.learn-more:hover .circle {
  width: 100%;
}

button.learn-more:hover .circle .icon.arrow {
  background: #fff;
  transform: translate(1rem, 0);
}

button.learn-more:hover .button-text {
  color: #fff;
}

.no-book {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.2em;
  color: #666;
}


.section5 { 
  background: #818B7E; 
  height: 300px;
}

.outro {
  display: flex;
  justify-content: space-between;
  width: 84%;
  height: 24%;
}

.outro-left {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.outro-right {
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.outro-left h3{
  color: #FEFFE9;
  margin: 0;
}

.outro-left p {
  color: #ffffff;
  font-weight: 300;
  margin: 0;
}

.outro-right a {
  color: #C0C7BE;
  text-decoration: none;
}

.outro-right a:hover {
  color: #282936;
}
</style>