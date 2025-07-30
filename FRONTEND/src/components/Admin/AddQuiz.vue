<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">➕ Add New Quiz</h2>

    <div v-if="error" class="alert alert-danger text-center">
      {{ error }}
    </div>

    <div v-if="successMessage" class="alert alert-success text-center">
      {{ successMessage }}
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <form @submit.prevent="submitQuiz" v-else class="card p-4 shadow">
      <div class="mb-3">
        <label for="chapter" class="form-label">Select Chapter</label>
        <select v-model="formData.chapter_id" class="form-select" required>
          <option disabled value="">-- Select Chapter --</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }} ({{ chapter.subject_name }})
          </option>
        </select>
      </div>

      <div class="mb-3">
    <label for="date_of_quiz" class="form-label">Date of Quiz</label>
    <input
      v-model="formData.date_of_quiz"
      type="date"
      class="form-control"
      :min="minDate"
      required
    />
  </div>
      <div class="mb-3">
        <label for="time_duration" class="form-label">Time Duration (in minutes)</label>
        <input
          v-model="formData.time_duration"
          type="number"
          min="1"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="remarks" class="form-label">Remarks (Optional)</label>
        <textarea
          v-model="formData.remarks"
          class="form-control"
          rows="3"
        ></textarea>
      </div>

      <div class="d-flex justify-content-between">
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Saving...' : 'Save' }}
        </button>
        <button type="button" class="btn btn-secondary" @click="cancel">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const chapters = ref([])
const formData = ref({
  chapter_id: '',
  date_of_quiz: '',
  time_duration: '',
  remarks: ''
})

const error = ref('')
const successMessage = ref('')
const loading = ref(true)
const isSubmitting = ref(false)

const router = useRouter()

const fetchChapters = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login.'
    router.push('/login')
    return
  }

  try {
    const response = await axios.get('http://127.0.0.1:5000/api/subjects', {
      headers: { Authorization: `Bearer ${token}` }
    })
    chapters.value = response.data.flatMap(subject =>
      subject.chapters.map(ch => ({
        id: ch.id,
        name: ch.name,
        subject_name: subject.name
      }))
    )
  } catch (err) {
    error.value = 'Failed to load chapters.'
  } finally {
    loading.value = false
  }
}

const submitQuiz = async () => {
  error.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login.'
    router.push('/login')
    return
  }

  try {
    await axios.post(`http://127.0.0.1:5000/admin/chapters/${formData.value.chapter_id}/quizzes`, formData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    successMessage.value = 'Quiz added successfully!'
    setTimeout(() => router.push('/quiz'), 600)
  } catch (err) {
    error.value = 'Error adding quiz.'
  } finally {
    isSubmitting.value = false
  }
}

const cancel = () => {
  router.push('/manage-quiz')
}

onMounted(fetchChapters)
const minDate = ref('')

onMounted(() => {
  const today = new Date()
  const yyyy = today.getFullYear()
  const mm = String(today.getMonth() + 1).padStart(2, '0')
  const dd = String(today.getDate()).padStart(2, '0')
  minDate.value = `${yyyy}-${mm}-${dd}`
})

</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
