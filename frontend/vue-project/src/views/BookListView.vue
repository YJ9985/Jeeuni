<template>
  <div class="book-list-container">
    <!-- 검색 섹션 -->
    <div class="search-section">
      <div class="search-wrapper">
        <div class="search-box">
          <input
            v-model="searchQuery"
            @keyup.enter="searchBooks"
            type="text"
            placeholder="도서명 또는 저자명으로 검색..."
            class="search-input"
          />
          <button @click="searchBooks" class="search-button">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </button>
        </div>
        <button @click="clearSearch" class="clear-button" v-if="isSearchActive">
          전체 목록 보기
        </button>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>도서를 검색 중입니다...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="clearSearch" class="retry-button">다시 시도</button>
    </div>

    <!-- 도서 목록 -->
    <div v-else class="books-grid">
      <div v-if="books.length === 0 && !loading" class="no-books">
        <p v-if="isSearchActive">검색 결과가 없습니다.</p>
        <p v-else>등록된 도서가 없습니다.</p>
      </div>
      
      <div
        v-for="book in books"
        :key="book.id"
        @click="goToBookDetail(book.id)"
        class="book-card"
      >
        <div class="book-content">
          <div class="book-cover">
            <img
              v-if="book.cover"
              :src="book.cover"
              :alt="book.title"
              class="cover-image"
              @error="handleImageError"
            />
            <div v-else class="no-cover">
              <svg class="book-icon" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
              </svg>
            </div>
          </div>
          
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            <p v-if="book.description" class="book-description">
              {{ truncateDescription(book.description) }}
            </p>
            <p v-if="book.pub_date" class="book-date">
              출간일: {{ formatDate(book.pub_date) }}
            </p>
          </div>
        </div>
        
        <div class="book-overlay">
          <span class="view-detail">자세히 보기</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'BookListView',
  setup() {
    const router = useRouter()
    const books = ref([])
    const searchQuery = ref('')
    const loading = ref(false)
    const error = ref('')
    const isSearchActive = ref(false)

    const API_BASE = 'http://127.0.0.1:8000/api/v1'

    // API 호출 함수
    const searchBooks = async () => {
      if (!searchQuery.value.trim()) {
        error.value = '검색어를 입력하세요'
        return
      }

      loading.value = true
      error.value = ''
      
      try {
        const response = await axios.get(`${API_BASE}/posts/create/books/search/`, {
          params: { q: searchQuery.value }
        })
        books.value = response.data
        isSearchActive.value = true
      } catch (err) {
        if (err.response?.status === 404) {
          books.value = []
          error.value = '검색 결과가 없습니다'
        } else if (err.response?.status === 400) {
          error.value = err.response.data.error || '검색어를 입력하세요'
        } else {
          error.value = '검색 중 오류가 발생했습니다'
        }
      } finally {
        loading.value = false
      }
    }

    // 전체 도서 목록 조회
    const fetchBooks = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await axios.get(`${API_BASE}/books/`)
        books.value = response.data
        
      } catch (err) {
        error.value = '도서 목록을 불러오는 중 오류가 발생했습니다'
      } finally {
        loading.value = false
      }
    }

    // 검색 초기화
    const clearSearch = () => {
      searchQuery.value = ''
      isSearchActive.value = false
      error.value = ''
      fetchBooks()
    }

    // 도서 상세 페이지로 이동
    const goToBookDetail = (bookId) => {
      router.push({ name: 'BookDetailView', params: { id: bookId } })
    }

    // 이미지 에러 처리
    const handleImageError = (event) => {
      event.target.style.display = 'none'
    }

    // 설명 텍스트 자르기
    const truncateDescription = (description) => {
      if (!description) return ''
      return description.length > 50 ? description.substring(0, 50) + '...' : description
    }

    // 날짜 포맷팅
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR')
    }

    onMounted(() => {
      // 컴포넌트 마운트 시 전체 목록 로드 (필요시)
      fetchBooks()
    })

    return {
      books,
      searchQuery,
      loading,
      error,
      isSearchActive,
      searchBooks,
      clearSearch,
      goToBookDetail,
      handleImageError,
      truncateDescription,
      formatDate
    }
  }
}
</script>

<style scoped>
.book-list-container {
  padding-top: 92px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
}

.search-section {
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.search-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
  display: flex;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  outline: none;
  font-size: 1rem;
  background: white;
}

.search-button {
  padding: 1rem 1.5rem;
  background: #397203;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background: #1b5c07;
}

.search-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.clear-button {
  padding: 0.75rem 1.5rem;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.clear-button:hover {
  background: #4b5563;
}

.loading-container {
  text-align: center;
  padding: 4rem 1rem;
}

.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #458f00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 4rem 1rem;
  color: #dc2626;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background: #b91c1c;
}

.books-grid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.no-books {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 1rem;
  color: #6b7280;
  font-size: 1.125rem;
}

.book-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  min-height: 180px;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.book-content {
  display: flex;
  padding: 1.5rem;
  gap: 1.5rem;
  align-items: flex-start;
}

.book-cover {
  flex-shrink: 0;
  width: 90px;
  height: 120px;
  background: #f3f4f6;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.book-card:hover .cover-image {
  transform: scale(1.05);
}

.no-cover {
  color: #9ca3af;
}

.book-icon {
  width: 2.5rem;
  height: 2.5rem;
}

.book-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.book-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.book-author {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.book-description {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.book-date {
  color: #9ca3af;
  font-size: 0.75rem;
}

.book-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(38, 41, 33, 0.8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
  pointer-events: none;
}

.book-card:hover .book-overlay {
  opacity: 1;
}

.view-detail {
  font-weight: 600;
  font-size: 1rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .book-list-container {
    padding-top: 100px;
  }
  
  .search-wrapper {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .book-content {
    padding: 1rem;
    gap: 1rem;
  }
  
  .book-cover {
    width: 70px;
    height: 95px;
  }
}

@media (max-width: 480px) {
  .books-grid {
    grid-template-columns: 1fr;
  }
  
  .book-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .book-cover {
    width: 90px;
    height: 120px;
  }
}
</style>