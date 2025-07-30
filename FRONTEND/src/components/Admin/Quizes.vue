<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">📝 Quizzes</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else>
      <div v-for="subject in subjects" :key="subject.id" :ref="'subject-' + subject.id" class="card shadow mb-4">
        <div class="card-header bg-primary text-white fw-bold">
          {{ subject.name }}
        </div>
        <div class="card-body">
          <div v-if="subject.chapters.length === 0" class="text-muted">
            No Chapters/Quizzes available for this subject.
          </div>

          <div v-for="chapter in subject.chapters" :key="chapter.id" class="mb-3">
            <h5>📘 Chapter: {{ chapter.name }}</h5>

            <div v-if="!chapter.quizzes || chapter.quizzes.length === 0" class="text-muted ms-3">
              No Quizzes in this Chapter.
            </div>

            <div v-else>
              <div
                v-for="quiz in chapter.quizzes"
                :key="quiz.id"
                :ref="'quiz-' + quiz.id"
                :data-quiz-id="quiz.id"
                class="border p-2 mb-2 rounded ms-3"
              >

                <p><strong>Quiz ID:</strong> {{ quiz.id }}</p>
                <p><strong>Date:</strong> {{ quiz.date_of_quiz }}</p>
                <p><strong>Time Duration:</strong> {{ quiz.time_duration }} mins</p>
                <p><strong>Remarks:</strong> {{ quiz.remarks || 'None' }}</p>

                <div class="d-flex gap-2">
                  <button @click="editQuiz(quiz.id)" class="btn btn-sm btn-outline-primary">✏️ Manage Quiz</button>
                  <button @click="goToAddQuestion(quiz.id)" class="btn btn-sm btn-outline-success">➕ Add Question</button>
                  <button @click="viewQuestions(quiz.id)" class="btn btn-sm btn-outline-info">👁️ View Questions</button>
                </div>
              </div>
            </div>

            <div class="text-end">
              <button @click="goToAddQuiz(chapter.id)" class="btn btn-sm btn-success mt-2">
                ➕ Add Quiz to this Chapter
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watchEffect } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const subjects = ref([])
const loading = ref(true)

const fetchQuizzes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:5000/api/subjects', {
      headers: { Authorization: `Bearer ${token}` }
    })
    subjects.value = response.data
  } catch (err) {
    console.error('Error fetching quizzes:', err)
  } finally {
    loading.value = false
  }
}

const goToAddQuestion = (quizId) => router.push(`/add-question/${quizId}`)
const viewQuestions = (quizId) => router.push(`/view-questions/${quizId}`)
const editQuiz = (quizId) => router.push(`/manage-quiz/${quizId}`)
const goToAddQuiz = (chapterId) => router.push(`/add-quiz/${chapterId}`)

const scrollToElement = (refName) => {
  setTimeout(() => {
    const el = document.querySelector(`[ref="${refName}"]`)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('border', 'border-success')
      setTimeout(() => el.classList.remove('border', 'border-success'), 1500)
    }
  }, 300)
}

// 👇 Watch for route query (search-based navigation like ?focus=Quiz:4)
watchEffect(() => {
  const focus = route.query.focus
  if (focus) {
    if (focus.startsWith('Quiz:')) {
      const quizId = focus.split(':')[1]
      scrollToElement('quiz-' + quizId)
    } else if (focus.startsWith('Subject:')) {
      const subjectId = focus.split(':')[1]
      scrollToElement('subject-' + subjectId)
    }
  }
})

onMounted(fetchQuizzes)
</script>

<style scoped>
.card-header {
  font-size: 1.25rem;
  background: linear-gradient(135deg, #1e90ff, #00bfff);
  color: white;
}
.border-success {
  box-shadow: 0 0 10px 3px #28a74599;
  transition: box-shadow 0.3s ease;
}
</style>
