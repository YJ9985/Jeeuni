<template>
  <div class="post-create-container">
    <div class="post-create-wrapper">

      <h1 class="post-create-title">포스트 작성</h1>
      <!-- 도서 선택 섹션 -->
      <div class="book-selector">
        <h3>도서 선택</h3>
        <!-- 0-1, 0-2: 도서 선택 상태 표시 -->
        <div class="selected-book-display">
          <div v-if="!selectedBook" class="no-book-selected">
            <div class="book-placeholder">
              <i class="book-icon">📚</i>
              <p>도서 정보 없음</p>
            </div>
          </div>
          <div v-else class="selected-book-info">
            <img v-if="selectedBook.cover" :src="selectedBook.cover" :alt="selectedBook.title" class="book-cover">
            <div class="book-details">
              <h4>{{ selectedBook.title }}</h4>
              <p>{{ selectedBook.author }}</p>
              <small>ID: {{ selectedBook.id }}</small>
            </div>
          </div>
          <button @click="openSearchModal" class="search-button">
            도서 검색
          </button>
        </div>
      </div>
  
      <!-- 포스트 작성 폼 -->
      <div class="post-form">
        <h3>포스트 작성</h3>
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            id="title"
            v-model="postData.title" 
            type="text" 
            placeholder="포스트 제목을 입력하세요"
            class="form-input"
          >
        </div>
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content"
            v-model="postData.content" 
            placeholder="포스트 내용을 입력하세요"
            rows="4"
            class="form-textarea"
          ></textarea>
        </div>
      </div>
  
      <!-- 하단 버튼 -->
      <div class="form-actions">
        <button @click="cancelPost" class="cancel-btn">취소</button>
        <button @click="submitPost" :disabled="!canSubmit" class="submit-btn">등록</button>
      </div>
  
      <!-- 도서 검색 모달 -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>도서 검색</h3>
            <button @click="closeModal" class="close-button">&times;</button>
          </div>
          
          <div class="modal-body">
            <!-- 검색 방법 선택 탭 -->
            <div class="search-tabs">
              <button 
                @click="activeTab = 'text'" 
                :class="{ active: activeTab === 'text' }"
                class="tab-button"
              >
                텍스트 검색
              </button>
              <button 
                @click="activeTab = 'image'" 
                :class="{ active: activeTab === 'image' }"
                class="tab-button"
              >
                이미지 검색
              </button>
            </div>
  
            <!-- 텍스트 검색 탭 -->
            <div v-if="activeTab === 'text'" class="tab-content">
              <!-- 1. 검색 입력 폼 -->
              <div class="search-form">
                <input 
                  v-model="searchQuery" 
                  @keyup.enter="searchInternalBooks"
                  placeholder="도서명 또는 저자명을 입력하세요"
                  class="search-input"
                >
                <button @click="searchInternalBooks" :disabled="isLoading" class="search-submit-button">
                  검색
                </button>
              </div>
            </div>
  
            <!-- 이미지 검색 탭 -->
            <div v-if="activeTab === 'image'" class="tab-content">
              <div class="image-search-section">
                <!-- 이미지 업로드 -->
                <div class="image-upload">
                  <input 
                    ref="imageInput"
                    type="file" 
                    accept="image/*" 
                    @change="handleImageUpload"
                    style="display: none"
                  >
                  <button @click="$refs.imageInput.click()" class="upload-button">
                    📷 이미지 업로드
                  </button>
                </div>
  
                <!-- 업로드된 이미지 미리보기 -->
                <div v-if="uploadedImage" class="image-preview">
                  <img :src="uploadedImage" alt="업로드된 이미지" class="preview-image">
                </div>
  
                <!-- 텍스트 추출 결과 -->
                <div v-if="textOptions.length > 0" class="text-options">
                  <h4>추출된 텍스트 (원하는 텍스트를 순서대로 선택하세요)</h4>
                  <div class="options-grid">
                    <div 
                      v-for="(option, index) in textOptions" 
                      :key="index"
                      @click="toggleTextOption(option)"
                      :class="{ 
                        selected: selectedTextOptions.includes(option),
                        'order-badge': selectedTextOptions.includes(option)
                      }"
                      class="text-option"
                    >
                      {{ option }}
                      <span v-if="selectedTextOptions.includes(option)" class="order-number">
                        {{ selectedTextOptions.indexOf(option) + 1 }}
                      </span>
                    </div>
                  </div>
                  
                  <!-- 선택된 검색어 미리보기 -->
                  <div v-if="selectedTextOptions.length > 0" class="search-preview">
                    <p><strong>검색어:</strong> "{{ selectedTextOptions.join(' ') }}"</p>
                    <button @click="searchWithImageText" :disabled="isLoading" class="search-with-image-button">
                      이 검색어로 검색
                    </button>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- 로딩 상태 -->
            <div v-if="isLoading" class="loading">
              <div class="spinner"></div>
              <p>{{ loadingMessage }}</p>
            </div>
  
            <!-- 2-1. DB 내부 검색 결과 -->
            <div v-if="showInternalResults && !isLoading" class="search-results">
              <h4>검색 결과</h4>
              <div v-if="internalBooks.length === 0" class="no-results">
                검색 결과가 없습니다.
              </div>
              <div v-else class="books-list">
                <div 
                  v-for="book in internalBooks" 
                  :key="book.id"
                  @click="selectBook(book)"
                  class="book-item"
                  :class="{ selected: tempSelectedBook?.id === book.id }"
                >
                  <img v-if="book.cover" :src="book.cover" :alt="book.title" class="book-thumbnail">
                  <div class="book-info">
                    <h5>{{ book.title }}</h5>
                    <p>{{ book.author }}</p>
                  </div>
                </div>
              </div>
              
              <!-- 2-2. 외부 검색 버튼 -->
              <div class="external-search-trigger">
                <p>원하시는 도서가 없나요?</p>
                <button @click="searchExternalBooks" :disabled="isLoading" class="external-search-button">
                  외부 검색
                </button>
              </div>
            </div>
  
            <!-- 3-1. 외부 검색 결과 -->
            <div v-if="showExternalResults && !isLoading" class="search-results">
              <h4>외부 도서 검색 결과</h4>
              <div v-if="externalBooks.length === 0" class="no-results">
                외부 검색 결과가 없습니다.
              </div>
              <div v-else class="books-list">
                <div 
                  v-for="(book, index) in externalBooks" 
                  :key="index"
                  @click="selectExternalBook(book)"
                  class="book-item"
                  :class="{ selected: tempSelectedBook?.title === book.title && tempSelectedBook?.author === book.author }"
                >
                  <img v-if="book.cover" :src="book.cover" :alt="book.title" class="book-thumbnail">
                  <div class="book-info">
                    <h5>{{ book.title }}</h5>
                    <p>{{ book.author }}</p>
                    <small v-if="book.publisher">{{ book.publisher }}</small>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- 3-2. 카테고리 선택 (외부 검색 도서용) -->
            <div v-if="showCategorySelection" class="category-selection">
              <h4>카테고리 선택</h4>
              <div class="selected-book-preview">
                <img v-if="tempSelectedBook.cover" :src="tempSelectedBook.cover" :alt="tempSelectedBook.title" class="preview-cover">
                <div class="preview-info">
                  <h5>{{ tempSelectedBook.title }}</h5>
                  <p>{{ tempSelectedBook.author }}</p>
                </div>
              </div>
              <select v-model="selectedCategoryId" class="category-select">
                <option value="">카테고리를 선택하세요</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
              <button 
                @click="saveExternalBook" 
                :disabled="!selectedCategoryId || isSaving"
                class="save-book-button"
              >
                {{ isSaving ? '저장 중...' : 'DB에 저장' }}
              </button>
            </div>
          </div>
  
          <!-- 4, 5. 최종 선택 확인 -->
          <div v-if="tempSelectedBook && !showCategorySelection" class="modal-footer">
            <div class="final-selection">
              <div class="final-book-info">
                <img v-if="tempSelectedBook.cover" :src="tempSelectedBook.cover" :alt="tempSelectedBook.title" class="final-cover">
                <div class="final-details">
                  <h5>{{ tempSelectedBook.title }}</h5>
                  <p>{{ tempSelectedBook.author }}</p>
                </div>
              </div>
              <div class="action-buttons">
                <button @click="cancelSelection" class="cancel-button">취소</button>
                <button @click="confirmSelection" class="confirm-button">등록</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'
import router from '@/router'

export default {
  name: 'PostCreatePage',
  emits: ['post-created', 'post-cancelled'],
  setup(props, { emit }) {
    // 포스트 데이터
    const postData = reactive({
      title: '',
      content: ''
    })

    // 기존 도서 검색 상태
    const selectedBook = ref(null)
    const showModal = ref(false)
    const searchQuery = ref('')
    const isLoading = ref(false)
    const isSaving = ref(false)
    const loadingMessage = ref('검색 중...')
    
    // 검색 결과 상태
    const showInternalResults = ref(false)
    const showExternalResults = ref(false)
    const showCategorySelection = ref(false)
    const internalBooks = ref([])
    const externalBooks = ref([])
    
    // 선택된 도서 관리
    const tempSelectedBook = ref(null)
    const selectedCategoryId = ref('')
    const categories = ref([])

    // 새로운 이미지 검색 상태
    const activeTab = ref('text')
    const uploadedImage = ref(null)
    const textOptions = ref([])
    const selectedTextOptions = ref([])

    // API 기본 설정 및 인증 토큰
    const API_BASE = import.meta.env.VITE_API_BASE_URL
    
    // Axios 인터셉터로 인증 토큰 추가
    const setupAxiosInterceptors = () => {
      axios.interceptors.request.use(
        (config) => {
          const token = localStorage.getItem('auth_token') || localStorage.getItem('access_token')
          if (token) {
            config.headers.Authorization = `Bearer ${token}`
          }
          return config
        },
        (error) => {
          return Promise.reject(error)
        }
      )

      // 응답 인터셉터로 토큰 만료 처리
      axios.interceptors.response.use(
        (response) => response,
        (error) => {
          if (error.response?.status === 401) {
            // 토큰 만료 시 로그인 페이지로 리다이렉트
            localStorage.removeItem('auth_token')
            localStorage.removeItem('access_token')
            window.location.href = '/accounts/login'
          }
          return Promise.reject(error)
        }
      )
    }

    // 폼 제출 가능 여부
    const canSubmit = computed(() => {
      return postData.title.trim() && postData.content.trim() && selectedBook.value
    })

    // 카테고리 목록 가져오기
    const fetchCategories = async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/v1/categories/`)
        categories.value = response.data
      } catch (error) {
        console.error('카테고리 로딩 실패:', error)
      }
    }

    // 이미지 업로드 및 텍스트 추출
    const handleImageUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      // 이미지 미리보기
      const reader = new FileReader()
      reader.onload = (e) => {
        uploadedImage.value = e.target.result
      }
      reader.readAsDataURL(file)

      // 텍스트 추출을 위한 API 호출
      const formData = new FormData()
      formData.append('image', file)

      isLoading.value = true
      loadingMessage.value = '이미지에서 텍스트 추출 중...'
      
      try {
        const response = await axios.post(`${API_BASE}/api/v1/posts/create/books/upload/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        textOptions.value = response.data.options
        selectedTextOptions.value = []
      } catch (error) {
        console.error('텍스트 추출 실패:', error)
        alert('이미지에서 텍스트를 추출할 수 없습니다.')
      } finally {
        isLoading.value = false
      }
    }

    // 텍스트 옵션 선택/해제
    const toggleTextOption = (option) => {
      const index = selectedTextOptions.value.indexOf(option)
      if (index > -1) {
        selectedTextOptions.value.splice(index, 1)
      } else {
        selectedTextOptions.value.push(option)
      }
    }

    // 이미지에서 추출한 텍스트로 검색
    const searchWithImageText = () => {
      if (selectedTextOptions.value.length === 0) return
      
      searchQuery.value = selectedTextOptions.value.join(' ')
      activeTab.value = 'text'
      searchInternalBooks()
    }

    // 모달 열기/닫기
    const openSearchModal = () => {
      showModal.value = true
      resetSearchState()
    }

    const closeModal = () => {
      showModal.value = false
      resetSearchState()
    }

    const resetSearchState = () => {
      showInternalResults.value = false
      showExternalResults.value = false
      showCategorySelection.value = false
      tempSelectedBook.value = null
      selectedCategoryId.value = ''
      internalBooks.value = []
      externalBooks.value = []
      activeTab.value = 'text'
      uploadedImage.value = null
      textOptions.value = []
      selectedTextOptions.value = []
      loadingMessage.value = '검색 중...'
    }

    // 1. DB 내부 도서 검색
    const searchInternalBooks = async () => {
      if (!searchQuery.value.trim()) return
      
      isLoading.value = true
      loadingMessage.value = '도서 검색 중...'
      try {
        const response = await axios.get(`${API_BASE}/api/v1/posts/create/books/search/`, {
          params: { q: searchQuery.value }
        })
        internalBooks.value = response.data
        showInternalResults.value = true
        showExternalResults.value = false
        showCategorySelection.value = false
      } catch (error) {
        if (error.response?.status === 404) {
          internalBooks.value = []
          showInternalResults.value = true
        } else {
          console.error('내부 검색 실패:', error)
          alert('검색 중 오류가 발생했습니다.')
        }
      } finally {
        isLoading.value = false
      }
    }

    // 2-2. 외부 도서 검색
    const searchExternalBooks = async () => {
      if (!searchQuery.value.trim()) return
      
      isLoading.value = true
      loadingMessage.value = '외부 도서 검색 중...'
      try {
        const response = await axios.get(`${API_BASE}/api/v1/posts/create/books/library/`, {
          params: { q: searchQuery.value }
        })
        
        // 검색 결과 처리
        if (response.data && response.data.result) {
          externalBooks.value = response.data.result
        } else {
          externalBooks.value = [] // 결과가 없으면 빈 배열로 설정
        }
        externalBooks.value = response.data.result
        showExternalResults.value = true
        showInternalResults.value = false
        showCategorySelection.value = false
      } catch (error) {
        console.error('외부 검색 실패:', error)
        alert('외부 검색 중 오류가 발생했습니다.')
      } finally {
        isLoading.value = false
      }
    }

    // 내부 도서 선택
    const selectBook = (book) => {
      tempSelectedBook.value = book
    }

    // 외부 도서 선택
    const selectExternalBook = (book) => {
      tempSelectedBook.value = book
      showCategorySelection.value = true
      showExternalResults.value = false
    }

    // 3-2. 외부 도서 DB에 저장
    const saveExternalBook = async () => {
      if (!selectedCategoryId.value || !tempSelectedBook.value) return
      
      isSaving.value = true
      try {
        const bookData = {
          title: tempSelectedBook.value.title,
          author: tempSelectedBook.value.author,
          cover: tempSelectedBook.value.cover,
          description: tempSelectedBook.value.description,
          pub_date: tempSelectedBook.value.pub_date,
          category: selectedCategoryId.value
        }
        
        const response = await axios.post(`${API_BASE}/api/v1/posts/create/books/library/add/`, bookData)
        console.log('API 응답:', response.data);
        
        if (response.data && response.data.id) {
          tempSelectedBook.value = { ...tempSelectedBook.value, id: response.data.id }
          console.log('ID가 추가된 tempSelectedBook:', tempSelectedBook.value);
        } else {
          console.error('ID를 찾을 수 없습니다');
        }
        showCategorySelection.value = false
      } catch (error) {
        console.error('도서 저장 실패:', error)
        alert('도서 저장 중 오류가 발생했습니다.')
      } finally {
        isSaving.value = false
      }
    }

    // 5-1. 선택 취소
    const cancelSelection = () => {
      closeModal()
    }

    // 5-2, 6. 선택 확인 및 등록
    const confirmSelection = () => {
      selectedBook.value = tempSelectedBook.value
      closeModal()
    }

    // 포스트 관련 함수들
    const cancelPost = () => {
      if (confirm('작성 중인 내용이 사라집니다. 정말 취소하시겠습니까?')) {
        emit('post-cancelled')
        router.push({name: 'HomeView'})
      }
    }

    const submitPost = async () => {
      if (!canSubmit.value) return

      try {
        const postPayload = {
          title: postData.title,
          content: postData.content,
          book_pk: selectedBook.value.id
        }

        const response = await axios.post(`${API_BASE}/api/v1/posts/create/`, postPayload)
        
        alert('포스트가 성공적으로 등록되었습니다!')
        emit('post-created', response.data)
        router.push(`posts/${response.data.id}`)
      } catch (error) {
        console.error('포스트 등록 실패:', error)
        alert('포스트 등록 중 오류가 발생했습니다.')
      }
    }

    // 컴포넌트 마운트 시 초기화
    onMounted(() => {
      setupAxiosInterceptors()
      fetchCategories()
    })

    return {
      // 포스트 데이터
      postData,
      canSubmit,
      
      // 기존 도서 검색 상태
      selectedBook,
      showModal,
      searchQuery,
      isLoading,
      isSaving,
      loadingMessage,
      showInternalResults,
      showExternalResults,
      showCategorySelection,
      internalBooks,
      externalBooks,
      tempSelectedBook,
      selectedCategoryId,
      categories,
      
      // 이미지 검색 상태
      activeTab,
      uploadedImage,
      textOptions,
      selectedTextOptions,
      
      // 함수들
      openSearchModal,
      closeModal,
      searchInternalBooks,
      searchExternalBooks,
      selectBook,
      selectExternalBook,
      saveExternalBook,
      cancelSelection,
      confirmSelection,
      handleImageUpload,
      toggleTextOption,
      searchWithImageText,
      cancelPost,
      submitPost
    }
  }
}
</script>

<style scoped>
.post-create-container {
  padding-top: 92px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
}

.post-create-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px 128px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.post-create-title {
  font-size: 40px;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  margin: 0;
  padding: 32px 0;
}

/* 도서 선택 섹션 */
.book-selector {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.book-selector h3 {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.book-selector h3::before {
  content: "📚";
  font-size: 24px;
}

.selected-book-display {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  background: #f9fafb;
  transition: all 0.3s ease;
}

.selected-book-display:hover {
  border-color: #397203;
  background: #f0f9e8;
}

.no-book-selected {
  flex: 1;
}

.book-placeholder {
  text-align: center;
  /* padding: 32px; */
  color: #6b7280;
}

.book-icon {
  font-size: 24px;
  display: block;
  margin-bottom: 8px;
}

.book-placeholder p {
  font-size: 16px;
  margin: 0;
}

.selected-book-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 20px;
}

.book-cover {
  width: 80px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.book-details h4 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.book-details p {
  font-size: 16px;
  color: #6b7280;
  margin: 4px 0;
}

.book-details small {
  font-size: 14px;
  color: #9ca3af;
}

.search-button {
  padding: 12px 24px;
  background: #397203;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-button:hover {
  background: #1b5c07;
  transform: translateY(-1px);
}

/* 포스트 작성 폼 */
.post-form {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.post-form h3 {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.post-form h3::before {
  content: "✍️";
  font-size: 24px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.form-input,
.form-textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 16px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #397203;
  box-shadow: 0 0 0 3px rgba(57, 114, 3, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 160px;
  line-height: 1.6;
}

/* 하단 버튼 */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.cancel-btn,
.submit-btn {
  padding: 16px 32px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 120px;
}

.cancel-btn {
  background: #6b7280;
  color: white;
}

.cancel-btn:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.submit-btn {
  background: #397203;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #1b5c07;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

/* 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 32px;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 32px;
}

/* 검색 탭 */
.search-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.tab-button {
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.3s ease;
}

.tab-button.active {
  color: #397203;
  border-bottom-color: #397203;
}

.tab-button:hover {
  color: #374151;
}

.tab-content {
  margin-bottom: 32px;
}

/* 검색 폼 */
.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #397203;
  box-shadow: 0 0 0 3px rgba(57, 114, 3, 0.1);
}

.search-submit-button {
  padding: 12px 24px;
  background: #397203;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-submit-button:hover:not(:disabled) {
  background: #1b5c07;
}

.search-submit-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 이미지 검색 */
.image-search-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.image-upload {
  text-align: center;
}

.upload-button {
  padding: 16px 32px;
  background: #3488d6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.upload-button:hover {
  background: #0f4980;
}

.image-preview {
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.text-options h4 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.text-option {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  position: relative;
  font-size: 14px;
}

.text-option:hover {
  border-color: #397203;
  background: #f0f9e8;
}

.text-option.selected {
  border-color: #397203;
  background: #397203;
  color: white;
}

.order-number {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.search-preview {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}

.search-preview p {
  margin: 0 0 12px 0;
  font-size: 16px;
}

.search-with-image-button {
  padding: 12px 24px;
  background: #397203;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.search-with-image-button:hover:not(:disabled) {
  background: #1b5c07;
}

.search-with-image-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 로딩 */
.loading {
  text-align: center;
  padding: 48px 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #397203;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

/* 검색 결과 */
.search-results {
  margin-top: 32px;
}

.search-results h4 {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 24px 0;
}

.no-results {
  text-align: center;
  color: #6b7280;
  /* font-style: italic; */
  padding: 48px 16px;
  font-size: 16px;
}

.books-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.book-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.book-item:hover {
  border-color: #397203;
  background: #f0f9e8;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.book-item.selected {
  border-color: #397203;
  background: #f0f9e8;
  box-shadow: 0 0 0 3px rgba(57, 114, 3, 0.1);
}

.book-thumbnail {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.book-info {
  flex: 1;
}

.book-info h5 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.book-info p {
  font-size: 14px;
  color: #6b7280;
  margin: 2px 0;
}

.book-info small {
  font-size: 12px;
  color: #9ca3af;
}

/* 외부 검색 */
.external-search-trigger {
  text-align: center;
  padding: 32px;
  border-top: 1px solid #e5e7eb;
}

.external-search-trigger p {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 16px 0;
}

.external-search-button {
  padding: 12px 24px;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.external-search-button:hover:not(:disabled) {
  background: #4b5563;
}

.external-search-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 카테고리 선택 */
.category-selection {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-top: 24px;
}

.category-selection h4 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 16px 0;
}

.selected-book-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 16px;
}

.preview-cover {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.preview-info h5 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.preview-info p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.category-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 16px;
  background: white;
}

.category-select:focus {
  outline: none;
  border-color: #397203;
  box-shadow: 0 0 0 3px rgba(57, 114, 3, 0.1);
}

.save-book-button {
  width: 100%;
  padding: 12px 24px;
  background: #397203;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.save-book-button:hover:not(:disabled) {
  background: #1b5c07;
}

.save-book-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 모달 푸터 */
.modal-footer {
  position: sticky;
  bottom: 0;
  z-index: 10;
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px 32px;
}

/* .modal-footer {
  display: flex;
  justify-content: space-between;
} */

.final-selection {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.final-book-info {
  display: flex;
  align-items: center;
  gap: 16px;
  /* flex: 1; */
}

.final-cover {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.final-details h5 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.final-details p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.cancel-button,
.confirm-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 100px;
}

.cancel-button {
  background: #6b7280;
  color: white;
}

.cancel-button:hover {
  background: #4b5563;
}

.confirm-button {
  background: #397203;
  color: white;
}

.confirm-button:hover {
  background: #1b5c07;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .post-create-container {
    padding-top: 100px;
  }
  
  .post-create-wrapper {
    padding: 0 16px 64px;
    gap: 24px;
  }
  
  .post-create-title {
    font-size: 28px;
    padding: 24px 0;
  }
  
  .book-selector,
  .post-form {
    padding: 24px;
  }
  
  .selected-book-display {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .selected-book-info {
    flex-direction: column;
    text-align: center;
  }
  
  .search-button {
    width: 100%;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-btn,
  .submit-btn {
    width: 100%;
  }
  
  .modal-overlay {
    padding: 8px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 20px;
  }
  
  .search-form {
    flex-direction: column;
  }
  
  .search-input,
  .search-submit-button {
    width: 100%;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .final-selection {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .cancel-button,
  .confirm-button {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .post-create-wrapper {
    gap: 16px;
  }
  
  .post-create-title {
    font-size: 24px;
    padding: 16px 0;
  }
  
  .book-selector,
  .post-form {
    padding: 16px;
  }
  
  .selected-book-display {
    padding: 16px;
  }
  
  .book-placeholder {
    padding: 24px;
  }
  
  .book-icon {
    font-size: 36px;
    margin-bottom: 12px;
  }
  
  .modal-header h3 {
    font-size: 20px;
  }
  
  .close-button {
    font-size: 24px;
  }
  
  .search-tabs {
    flex-direction: column;
    gap: 0;
  }
  
  .tab-button {
    border-bottom: 1px solid #e5e7eb;
    border-radius: 0;
  }
  
  .tab-button.active {
    background: #f0f9e8;
    border-bottom-color: #397203;
  }
}
</style>