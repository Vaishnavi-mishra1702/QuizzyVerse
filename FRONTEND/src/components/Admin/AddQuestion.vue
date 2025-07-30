<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">➕ Add Question</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <form v-else @submit.prevent="submitQuestion">
      <div class="mb-3">
        <label class="form-label">Chapter</label>
        <select v-model="form.chapter_id" class="form-select" required>
          <option value="" disabled>Select Chapter</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Quiz</label>
        <select v-model="form.quiz_id" class="form-select" required>
          <option value="" disabled>Select Quiz</option>
          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
            Quiz ID: {{ quiz.id }} | Date: {{ quiz.date_of_quiz }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Question Statement</label>
        <textarea v-model="form.statement" class="form-control" rows="3" required></textarea>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <input v-model="form.option1" type="text" class="form-control" placeholder="Option 1" required />
        </div>
        <div class="col-md-6">
          <input v-model="form.option2" type="text" class="form-control" placeholder="Option 2" required />
        </div>
        <div class="col-md-6">
          <input v-model="form.option3" type="text" class="form-control" placeholder="Option 3" required />
        </div>
        <div class="col-md-6">
          <input v-model="form.option4" type="text" class="form-control" placeholder="Option 4" required />
        </div>
      </div>

      <div class="mb-4">
        <input v-model="form.correct_option" type="text" class="form-control" placeholder="Correct Option (e.g. Option 1)" required />
      </div>

      <div class="d-flex justify-content-end gap-3">
        <button type="submit" class="btn btn-success">💾 Save</button>
        <button type="button" @click="resetForm" class="btn btn-secondary">🗑️ Clear</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
// import { useRoute } from 'vue-router'
import { useRoute, useRouter } from 'vue-router'


const router = useRouter()

const route = useRoute()
const quizIdFromURL = route.params.quizId || null

const loading = ref(true)
const chapters = ref([])
const quizzes = ref([])

const form = ref({
  chapter_id: '',
  quiz_id: quizIdFromURL || '',
  statement: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option: ''
})

const fetchChaptersAndQuizzes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://127.0.0.1:5000/api/subjects`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    let allChapters = []
    let allQuizzes = []

    response.data.forEach(subject => {
      subject.chapters.forEach(chapter => {
        allChapters.push({
          id: chapter.id,
          name: chapter.name
        })

        chapter.quizzes?.forEach(quiz => {
          allQuizzes.push({
            id: quiz.id,
            date_of_quiz: quiz.date_of_quiz
          })
        })
      })
    })

    chapters.value = allChapters
    quizzes.value = allQuizzes
  } catch (err) {
    console.error('Error fetching data:', err)
  } finally {
    loading.value = false
  }
}


const submitQuestion = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(
      `http://127.0.0.1:5000/admin/quizzes/${form.value.quiz_id}/questions`,
      {
        question_statement: form.value.statement,
        option1: form.value.option1,
        option2: form.value.option2,
        option3: form.value.option3,
        option4: form.value.option4,
        correct_option: form.value.correct_option
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )

    alert('✅ Question added successfully!')
    resetForm()
    router.push('/quiz')
  } catch (err) {
    console.error('Error saving question:', err)
    alert('❌ Failed to save question.')
  }
}


const resetForm = () => {
  form.value = {
    chapter_id: '',
    quiz_id: quizIdFromURL || '',
    statement: '',
    option1: '',
    option2: '',
    option3: '',
    option4: '',
    correct_option: ''
  }
}

onMounted(fetchChaptersAndQuizzes)
</script>

<style scoped>
label {
  font-weight: 600;
}
</style>
