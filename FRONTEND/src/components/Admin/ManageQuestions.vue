<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">✏️ Edit Question</h2>

    <div v-if="error" class="alert alert-danger text-center">{{ error }}</div>
    <div v-if="successMessage" class="alert alert-success text-center">{{ successMessage }}</div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <form v-if="!loading" @submit.prevent="updateQuestion" class="card p-4 shadow">
      <div class="mb-3">
        <label class="form-label">Question Statement</label>
        <textarea
          v-model="formData.question_statement"
          class="form-control"
          required
        ></textarea>
      </div>

      <div class="mb-3" v-for="i in 4" :key="i">
        <label class="form-label">Option {{ i }}</label>
        <input
          v-model="formData[`option${i}`]"
          type="text"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Correct Option (1-4)</label>
        <input
          v-model="formData.correct_option"
          type="number"
          min="1"
          max="4"
          class="form-control"
          required
        />
      </div>

      <div class="d-flex justify-content-between">
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Updating...' : 'Update' }}
        </button>
        <button type="button" class="btn btn-danger" @click="deleteQuestion" :disabled="isSubmitting">
          Delete
        </button>
        <button type="button" class="btn btn-secondary" @click="cancelEdit">
            Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const questionId = route.params.questionId
const quizId = route.params.quizId

const formData = ref({
  question_statement: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option: 1
})

const error = ref('')
const successMessage = ref('')
const loading = ref(true)
const isSubmitting = ref(false)

const fetchQuestion = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://127.0.0.1:5000/admin/questions/${questionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    Object.assign(formData.value, response.data)
  } catch (err) {
    error.value = 'Failed to load question.'
  } finally {
    loading.value = false
  }
}

const updateQuestion = async () => {
  isSubmitting.value = true
  error.value = ''
  successMessage.value = ''

  try {
    const token = localStorage.getItem('token')
    await axios.put(`http://127.0.0.1:5000/admin/questions/${questionId}`, formData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    successMessage.value = 'Question updated successfully!'
    setTimeout(() => router.push(`/view-questions/${quizId}`), 600)
  } catch (err) {
    error.value = 'Error updating question.'
  } finally {
    isSubmitting.value = false
  }
}
const cancelEdit = () => {
  router.push(`/view-questions/${quizId}`)
}


const deleteQuestion = async () => {
  const confirmDelete = confirm('Are you sure you want to delete this question?')
  if (!confirmDelete) return

  isSubmitting.value = true

  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:5000/admin/questions/${questionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    successMessage.value = 'Question deleted.'
    setTimeout(() => router.push(`/view-questions/${quizId}`), 600)
  } catch (err) {
    error.value = 'Error deleting question.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(fetchQuestion)
</script>

<style scoped>
.container {
  max-width: 700px;
}
</style>
