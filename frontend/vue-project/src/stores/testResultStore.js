import { defineStore } from 'pinia'

export const useTestResultStore = defineStore('testResultStore', {
  state: () => ({
    result: null,
    answersMap: {}
  }),
  actions: {
    setResult(data) {
      this.result = data
    },
    setAnswersMap(data) {
      this.answersMap = data
    }
  },
  persist: true,
})
