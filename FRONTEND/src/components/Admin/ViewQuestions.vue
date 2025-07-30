<!-- src/components/ViewQuestions.vue -->
<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">📄 Questions for Quiz #{{ quizId }}</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else>
      <div v-if="questions.length === 0" class="text-muted text-center">
        No questions found for this quiz.
      </div>

      <div v-else class="list-group">
        <div
          v-for="question in questions"
          :key="question.id"
          class="list-group-item d-flex justify-content-between align-items-start"
        >
          <div>
            <h6>{{ question.question_statement }}</h6>
            <ul class="mb-1">
              <li>1. {{ question.option1 }}</li>
              <li>2. {{ question.option2 }}</li>
              <li>3. {{ question.option3 }}</li>
              <li>4. {{ question.option4 }}</li>
            </ul>
            <strong>Correct Option:</strong> {{ question.correct_option }}
          </div>
          <button
            class="btn btn-sm btn-outline-primary"
            @click="goToManageQuestion(question.id)"
          >
            🛠️ Manage Question
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const quizId = route.params.quizId
const questionId = route.params.questionId
const questions = ref([])
const loading = ref(true)

const fetchQuestions = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(
      `http://127.0.0.1:5000/admin/quizzes/${quizId}/questions`,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    questions.value = response.data
  } catch (error) {
    console.error('Error fetching questions:', error)
  } finally {
    loading.value = false
  }
}

const goToManageQuestion = (questionId) => {
  router.push(`/manage-questions/${questionId}/${quizId}`)

}

onMounted(fetchQuestions)
</script>

<style scoped>
.list-group-item {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  margin-bottom: 10px;
}
</style>
