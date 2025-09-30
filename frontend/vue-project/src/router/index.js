import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import KakaoCallbackView  from '@/views/KakaoCallbackView.vue'
import HomeView from '@/views/HomeView.vue'
import BookListView from '@/views/BookListView.vue'
import TestRecommendView from '@/views/TestRecommendView.vue'
import PostCreateView from '@/views/PostCreateView.vue'
import TestLiteracyView from '@/views/TestLiteracyView.vue'
import TestResultView from '@/views/TestResultView.vue'
import BookRecommendView from '@/views/BookRecommendView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import PostDetailView from '@/views/PostDetailView.vue'
import PostUpdateView from '@/views/PostUpdateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    {
      path: '/accounts/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/accounts/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/accounts/kakao/login/callback',
      name: 'KakaoCallback',
      component: () => import('@/views/KakaoCallbackView.vue')
    },
    {
      path: '/books',
      name: 'BookListView',
      component: BookListView
    },
    {
      path: '/test',
      name: 'TestRecommendView',
      component: TestRecommendView
    },
    {
      path: '/posts',
      name: 'PostCreateView',
      component: PostCreateView
    },
    {
      path: '/test/literacy',
      name: 'TestLiteracy',
      component: TestLiteracyView
    },
    {
      path: '/test/literacy/result',
      name: 'TestResult',
      component: TestResultView
    },
    {
      path: '/books/recommend',
      name: 'BookRecommend',
      component: BookRecommendView
    },
    {
      path: '/books/:id',
      name: 'BookDetailView',
      component: BookDetailView
    },
    {
      path: '/posts/:id',
      name: 'PostDetailView',
      component: PostDetailView
    },
    {
      path: '/posts/:id/update',
      name: 'PostUpdateView',
      component: PostUpdateView
    }
  ],
})

export default router
