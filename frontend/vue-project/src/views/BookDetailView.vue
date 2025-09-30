<template>
  <div class="book-detail-container">
    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>도서 정보를 불러오는 중...</p>
    </div>

    <!-- 오류 상태 -->
    <div v-else-if="error" class="error-container">
      <h2>오류가 발생했습니다</h2>
      <p>{{ error }}</p>
      <button @click="fetchBookDetail" class="retry-btn">다시 시도</button>
    </div>

    <!-- 도서 상세 정보 -->
    <div v-else-if="book" class="book-content">
      <!-- 도서 정보 섹션 -->
      <div class="book-info-section">
        <div class="book-cover">
          <img 
            :src="book.cover || '/default-book-cover.jpg'" 
            :alt="book.title"
            @error="handleImageError"
          />
        </div>
        
        <div class="book-details">
          <div class="book-header">
            <h1 class="book-title">{{ book.title }}</h1>
            <span v-if="book.category" class="book-category">{{ book.category.name }}</span>
          </div>
          
          <div class="book-meta">
            <div class="meta-item">
              <span class="meta-label">저자</span>
              <span class="meta-value">{{ book.author }}</span>
            </div>
            
            <div class="meta-item" v-if="book.pub_date">
              <span class="meta-label">출간일</span>
              <span class="meta-value">{{ formatDate(book.pub_date) }}</span>
            </div>
          </div>
          
          <div class="book-description" v-if="book.description">
            <h3>도서 소개</h3>
            <p>{{ book.description }}</p>
          </div>
        </div>
      </div>

      <!-- 포스트 섹션 -->
      <div class="posts-section">
        <div class="posts-header">
          <h2>관련 포스트</h2>
          <div class="posts-actions">
            <button @click="togglePostsVisibility" class="toggle-posts-btn">
              {{ showPosts ? '포스트 숨기기' : '포스트 보기' }}
              <span class="post-count">({{ book.posts.length }})</span>
            </button>
            <button @click="createNewPost" class="create-post-btn">
              포스트 작성하기
            </button>
          </div>
        </div>

        <!-- 포스트 목록 -->
        <div v-show="showPosts" class="posts-content">
          <div v-if="book.posts.length === 0" class="no-posts">
            <p>아직 작성된 포스트가 없습니다.</p>
            <p>첫 번째 포스트를 작성해보세요!</p>
          </div>

          <div v-else class="posts-grid">
            <article 
              v-for="post in book.posts" 
              :key="post.id"
              class="post-card"
              @click="goToPost(post.id)"
            >
              <div class="post-header">
                <h3 class="post-title">{{ post.title }}</h3>
              </div>
              
              <div class="post-content">
                <p>{{ truncateContent(post.content) }}</p>
              </div>
              
              <div class="post-footer">
                <span class="post-date">{{ formatDate(post.created_at) }} 작성</span>
                <span class="read-more">자세히 보기 →</span>
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'BookDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const book = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const showPosts = ref(false)

    // 도서 상세 정보 가져오기
    const API_BASE = 'http://127.0.0.1:8000/api/v1'

    const fetchBookDetail = async () => {
      try {
        loading.value = true
        error.value = null
        
        const bookId = route.params.id
        const response = await axios.get(`${API_BASE}/books/${bookId}/`)
        
        book.value = response.data
      } catch (err) {
        error.value = err.response?.data?.message || '도서 정보를 불러오는데 실패했습니다.'
        console.error('Error fetching book detail:', err)
      } finally {
        loading.value = false
      }
    }

    // 날짜 포맷팅
    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 컨텐츠 요약
    const truncateContent = (content, maxLength = 100) => {
      if (!content) return ''
      
      if (content.length <= maxLength) {
        return content
      }
      
      return content.slice(0, maxLength) + '...'
    }

    // 이미지 오류 처리
    const handleImageError = (event) => {
      event.target.src = '/default-book-cover.jpg'
    }

    // 포스트 표시/숨김 토글
    const togglePostsVisibility = () => {
      showPosts.value = !showPosts.value
    }

    // 포스트로 이동
    const goToPost = (postId) => {
      router.push(`/posts/${postId}`)
    }

    // 새 포스트 작성
    const createNewPost = () => {
      router.push('/posts')
    }

    onMounted(() => {
      fetchBookDetail()
    })

    return {
      book,
      loading,
      error,
      showPosts,
      fetchBookDetail,
      formatDate,
      truncateContent,
      handleImageError,
      togglePostsVisibility,
      goToPost,
      createNewPost
    }
  }
}
</script>

<style scoped>
.book-detail-container {
  padding-top: 92px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
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

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #b91c1c;
}

.book-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.book-info-section {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  padding: 2rem;
  display: flex;
  gap: 2rem;
}

.book-cover {
  flex-shrink: 0;
  width: 200px;
  height: 280px;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.book-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
}

.book-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
  flex: 1;
  min-width: 200px;
}

.book-category {
  padding: 0.5rem 1rem;
  background: #B8BC7F;
  color: white;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 500;
  white-space: nowrap;
}

.book-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.meta-label {
  font-weight: 600;
  color: #374151;
  min-width: 60px;
}

.meta-value {
  color: #6b7280;
}

.book-description {
  border-top: 1px solid #e5e7eb;
  padding-top: 1.5rem;
}

.book-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.book-description p {
  color: #4b5563;
  line-height: 1.7;
}

.posts-section {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.posts-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.posts-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.posts-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.toggle-posts-btn {
  padding: 0.75rem 1.25rem;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 32px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toggle-posts-btn:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.post-count {
  font-size: 14px;
  opacity: 0.8;
  letter-spacing: 2px;
}

.create-post-btn {
  padding: 0.75rem 1.25rem;
  background: #397203;
  color: white;
  border: none;
  border-radius: 32px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.create-post-btn:hover {
  background: #1b5c07;
  transform: translateY(-1px);
}

.posts-content {
  padding: 1.5rem 2rem 2rem;
}

.no-posts {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.no-posts p {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.post-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #d1d5db;
}

.post-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #397203, #458f00);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.post-card:hover::before {
  transform: scaleX(1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.post-title {
  font-size: 22px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.4;
  flex: 1;
}

.post-date {
  font-size: 14px;
  color: #9ca3af;
}

.post-content {
  margin-bottom: 1rem;
}

.post-content p {
  color: #4b5563;
  line-height: 1.6;
  font-size: 16px;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.read-more {
  font-size: 14px;
  color: #397203;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.post-card:hover .read-more {
  opacity: 1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .book-detail-container {
    padding-top: 100px;
  }
  
  .book-content {
    padding: 1rem;
  }
  
  .book-info-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.5rem;
  }
  
  .book-cover {
    width: 160px;
    height: 220px;
  }
  
  .book-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .book-title {
    font-size: 1.5rem;
    min-width: auto;
  }
  
  .posts-header {
    flex-direction: column;
    align-items: stretch;
    padding: 1rem;
  }
  
  .posts-actions {
    justify-content: center;
  }
  
  .posts-content {
    padding: 1rem;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .post-card {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .book-info-section {
    padding: 1rem;
  }
  
  .book-cover {
    width: 140px;
    height: 190px;
  }
  
  .book-title {
    font-size: 1.25rem;
  }
  
  .posts-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .toggle-posts-btn,
  .create-post-btn {
    width: 100%;
    justify-content: center;
  }
  
  .post-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .post-date {
    align-self: flex-start;
  }
}
</style>