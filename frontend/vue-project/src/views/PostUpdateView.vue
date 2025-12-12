<template>
  <div class="post-create-container">
    <div class="post-create-wrapper">
      <h1 class="post-create-title">포스트 수정</h1>


        <!-- 도서 선택 섹션 -->
        <div class="book-selector">
        <h3>도서 정보</h3>
        <div class="selected-book-display">
            <div v-if="postData?.selectedBook" class="selected-book-info">
              <img v-if="postData?.selectedBook.cover" :src="postData?.selectedBook.cover" :alt="postData?.selectedBook.title" class="book-cover">
              <div class="book-details">
                  <h4>{{ postData?.selectedBook.title }}</h4>
                  <p>{{ postData?.selectedBook.author }}</p>
                  <small>ID: {{ postData?.selectedBook.id }}</small>
              </div>
            </div>

            <button class="search-button" disabled>
            도서 검색
            </button>
          </div>
        </div>

      <div class="post-form">
        <h3>포스트 수정</h3>
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
            rows="8"
            class="form-textarea"
          ></textarea>
        </div>
      </div>

      <div class="form-actions">
        <button @click="cancelUpdate" class="cancel-btn">취소</button>
        <button @click="updatePost" :disabled="!canSubmit" class="submit-btn">수정</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'PostUpdateView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const postId = route.params.id

    const API_BASE = import.meta.env.VITE_API_BASE_URL

    const postData = reactive({
      title: '',
      content: '',
      selectedBook: ''
    })

    const isLoading = ref(false)

    const canSubmit = computed(() => {
      return postData.title.trim() && postData.content.trim()
    })

    const fetchPost = async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/v1/posts/${postId}/`)
        postData.title = response.data.title
        postData.content = response.data.content
        console.log(response.data.book)
        postData.selectedBook = response.data?.book
      } catch (error) {
        console.error('포스트 불러오기 실패:', error)
        alert('포스트 정보를 불러오는 중 오류가 발생했습니다.')
        router.push('/')
      }
    }

    const updatePost = async () => {
      if (!canSubmit.value) return

      try {
        const response = await axios.put(`${API_BASE}/api/v1/posts/${postId}/`, {
          title: postData.title,
          content: postData.content
        })
        alert('포스트가 성공적으로 수정되었습니다!')
        router.push(`/posts/${postId}`)
      } catch (error) {
        console.error('포스트 수정 실패:', error)
        alert('포스트 수정 중 오류가 발생했습니다.')
      }
    }

    const cancelUpdate = () => {
      if (confirm('수정을 취소하시겠습니까? 변경 내용이 저장되지 않습니다.')) {
        router.back()
      }
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      postData,
      canSubmit,
      updatePost,
      cancelUpdate
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

.search-button:disabled {
  background: #9ca3af;
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
  min-height: 200px;
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
}
</style>