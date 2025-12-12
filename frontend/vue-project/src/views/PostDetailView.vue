<template>
  <div class="post-detail-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>포스트를 불러오는 중...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-message">
      <h2>오류가 발생했습니다</h2>
      <p>{{ error }}</p>
      <button @click="fetchPost" class="retry-btn">다시 시도</button>
    </div>

    <!-- Post Content -->
    <div v-else-if="post" class="post-content">

      <!-- Action Buttons -->
      <div class="action-buttons">
        <template v-if="canEditPost">
          <button @click="goToPostEdit" class="edit-btn">수정</button>
          <button @click="deletePost" class="delete-btn">삭제</button>
        </template>
        <button @click="goToPostCreate" class="list-btn">포스트 작성하기</button>
      </div>

      <!-- Book Information -->
      <div v-if="post.book" class="book-info">
        <div class="book-info-header" @click="toggleBookInfo">
          <h3>📚 작성된 도서 정보</h3>
          <button class="toggle-btn">
            {{ showBookInfo ?  '▲' : '▼' }}
          </button>
        </div>
        <div v-show="showBookInfo" class="book-card">
          <div class="book-details">
            <h4>{{ post.book.title }}</h4>
            <p class="book-author">저자: {{ post.book.author }}</p>
            <p class="book-pub-date">출간일: {{ formatBookDate(post.book.pub_date) }}</p>
          </div>
          <button @click="goToBookDetail" class="book-detail-btn">
            도서 상세보기
          </button>
        </div>
      </div>
      <!-- Post Header -->
      <div class="post-header">
        <div class="post-meta">
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
        </div>
        <h1 class="post-title">{{ post.title }}</h1>


        <!-- Post Body -->
        <div class="post-body">
          <div class="post-content-text" v-html="formatContent(post.content)"></div>
        </div>
      </div>

      <!-- Comment Section -->
      <div class="comment-section">
        <h3>💬 댓글 ({{ post.comments?.length || 0 }}개)</h3>
        
        <!-- Comment Form -->
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 작성해주세요..."
            rows="4"
            :disabled="submittingComment"
          ></textarea>
          <button 
            @click="submitComment" 
            :disabled="!newComment.trim() || submittingComment"
            class="submit-comment-btn"
          >
            {{ submittingComment ? '작성 중...' : '댓글 작성' }}
          </button>
        </div>

        <!-- Comments List -->
        <div class="comments-list">
          <div v-if="!post.comments || post.comments.length === 0" class="no-comments">
            아직 댓글이 없습니다. 첫 번째 댓글을 작성해보세요!
          </div>
          <div v-else>
            <div 
              v-for="comment in post.comments" 
              :key="comment.id" 
              class="comment-item"
            >
              <div class="comment-header">
                <!-- 본인 작성 댓글 -->
                <span
                class="comment-user"
                v-if="post.current_user && comment.user === post.current_user.id"
                >{{ post.current_user.name }}</span>
                <!-- 타인 작성 댓글 -->
                <span
                  class="comment-user"
                  v-else
                >***</span>
                <div class="comment-actions">
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                  <button 
                    v-if="post.current_user && comment.user === post.current_user.id"
                    @click="deleteComment(comment.id)"
                    class="delete-comment-btn"
                  >
                    삭제
                  </button>
                </div>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'PostDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const post = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const newComment = ref('')
    const submittingComment = ref(false)
    const showBookInfo = ref(false)

    // 포스트 상세 정보 가져오기
    const API_BASE = import.meta.env.VITE_API_BASE_URL

    const fetchPost = async () => {
      try {
        loading.value = true
        error.value = null
        
        const postId = route.params.id
        const response = await axios.get(`${API_BASE}/api/v1/posts/${postId}/`)

        post.value = response.data
      } catch (err) {
        error.value = err.response?.data?.message || '포스트를 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    // Submit comment
    const submitComment = async () => {
      if (!newComment.value.trim()) return
      
      try {
        submittingComment.value = true
        const postId = route.params.id
        const response = await axios.post(`${API_BASE}/api/v1/posts/${postId}/comments/`, {
          content: newComment.value
        })
        
        // Add new comment to the list
        if (!post.value.comments) {
          post.value.comments = []
        }
        post.value.comments.push(response.data)
        newComment.value = ''
      } catch (err) {
        alert('댓글 작성에 실패했습니다.')
      } finally {
        submittingComment.value = false
      }
    }

    // Delete post
    const deletePost = async () => {
      if (!confirm('정말 이 포스트를 삭제하시겠습니까?')) return
      
      try {
        const postId = route.params.id
        await axios.delete(`${API_BASE}/api/v1/posts/${postId}/`)
        alert('포스트가 삭제되었습니다.')
        router.push(`/books/${post.value.book.id}`)
      } catch (err) {
        alert('포스트 삭제에 실패했습니다.')
      }
    }

    // Delete comment
    const deleteComment = async (commentId) => {
      if (!confirm('정말 이 댓글을 삭제하시겠습니까?')) return
      
      try {
        const postId = route.params.id
        await axios.delete(`${API_BASE}/api/v1/posts/${postId}/comments/${commentId}/`)
        // Remove comment from list
        post.value.comments = post.value.comments.filter(comment => comment.id !== commentId)
      } catch (err) {
        alert('댓글 삭제에 실패했습니다.')
      }
    }

    // Toggle book info visibility
    const toggleBookInfo = () => {
      showBookInfo.value = !showBookInfo.value
    }

    // Navigation functions
    const goToBookDetail = () => {
      if (post.value?.book?.id) {
        router.push(`/books/${post.value.book.id}`)
      }
    }

    const goToPostEdit = () => {
      router.push(`/posts/${route.params.id}/update`)
    }

    const goToPostCreate = () => {
      router.push('/posts')
    }

    // Computed properties
    const canEditPost = computed(() => {
      return post.value?.user === post.value?.current_user?.id || false
    })

    // Utility functions
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatBookDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatContent = (content) => {
      if (!content) return ''
      return content.replace(/\n/g, '<br>')
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      post,
      loading,
      error,
      newComment,
      submittingComment,
      showBookInfo,
      canEditPost,
      fetchPost,
      submitComment,
      deletePost,
      deleteComment,
      toggleBookInfo,
      goToBookDetail,
      goToPostEdit,
      goToPostCreate,
      formatDate,
      formatBookDate,
      formatContent
    }
  }
}
</script>

<style scoped>
.post-detail-container {
  padding-top: 92px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
}

.loading-spinner {
  text-align: center;
  padding: 4rem 1rem;
}

.spinner {
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

.error-message {
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

.post-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 128px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.post-header {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.post-meta {
  margin-bottom: 1rem;
}

.post-date {
  font-size: 14px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: inline-block;
}

.post-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
  margin: 0;
  padding-left: 1rem;
}

.book-info {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.book-info-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.book-info-header:hover {
  background: #f9fafb;
}

.book-info-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.3s;
}

.toggle-btn:hover {
  background: #f3f4f6;
}

.book-card {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  background: #f9fafb;
}

.book-details h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.book-author,
.book-pub-date {
  font-size: 16px;
  color: #6b7280;
  margin: 0.25rem 0;
}

.book-detail-btn {
  padding: 0.75rem 1.25rem;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.book-detail-btn:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.post-body {
  background: white;
  border-top: 1px solid #e5e7eb;
  margin-top: 1rem;
  padding: 2rem 1rem;
}

.post-content-text {
  color: #4b5563;
  line-height: 1.8;
  font-size: 20px;
}

.post-content-text p {
  margin-bottom: 1rem;
}

.post-content-text h1,
.post-content-text h2,
.post-content-text h3 {
  color: #1f2937;
  margin: 1.5rem 0 1rem 0;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  justify-content: right;
  flex-wrap: wrap;
}

.edit-btn,
.delete-btn,
.list-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.edit-btn {
  background: #3488d6;
  color: white;
}

.edit-btn:hover {
  background: #0f4980;
  transform: translateY(-1px);
}

.delete-btn {
  background: #dc2626;
  color: white;
}

.delete-btn:hover {
  background: #b91c1c;
  transform: translateY(-1px);
}

.list-btn {
  background: #397203;
  color: white;
}

.list-btn:hover {
  background: #1b5c07;
  transform: translateY(-1px);
}

.comment-section {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.comment-section h3 {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.comment-form {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.comment-form textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 1rem;
  font-size: 16px;
  resize: vertical;
  min-height: 100px;
  margin-bottom: 1rem;
  transition: border-color 0.3s;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #397203;
  box-shadow: 0 0 0 3px rgba(57, 114, 3, 0.1);
}

.comment-form textarea:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.submit-comment-btn {
  padding: 0.75rem 1.5rem;
  background: #397203;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-comment-btn:hover:not(:disabled) {
  background: #1b5c07;
  transform: translateY(-1px);
}

.submit-comment-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.comments-list {
  padding: 1.5rem 2rem 2rem;
}

.no-comments {
  text-align: center;
  color: #6b7280;
  font-style: italic;
  padding: 2rem 1rem;
}

.comment-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  white-space: pre-line;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.comment-user {
  font-weight: 700;
  color: #374151;
  font-size: 16px;
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.comment-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.delete-comment-btn {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.3s;
}

.delete-comment-btn:hover {
  background: #fee2e2;
}

.comment-content {
  color: #4b5563;
  line-height: 1.6;
  font-size: 16px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .post-detail-container {
    padding-top: 100px;
  }
  
  .post-content {
    padding: 1rem;
  }
  
  .post-header,
  .post-body,
  .book-info,
  .comment-section {
    padding: 1.5rem;
  }
  
  .post-title {
    font-size: 1.5rem;
  }
  
  .book-card {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
    gap: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .edit-btn,
  .delete-btn,
  .list-btn {
    width: 100%;
    justify-content: center;
  }
  
  .comment-section h3,
  .comment-form {
    padding: 1rem;
  }
  
  .comments-list {
    padding: 1rem;
  }
  
  .comment-item {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .post-content {
    gap: 1rem;
  }
  
  .post-header,
  .post-body,
  .book-info {
    padding: 1rem;
  }
  
  .post-title {
    font-size: 1.25rem;
  }
  
  .book-info-header {
    padding: 1rem;
  }
  
  .book-card {
    padding: 1rem;
  }
  
  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .comment-actions {
    align-self: flex-end;
  }
}
</style>